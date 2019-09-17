from datetime import datetime, timedelta
from pytz import timezone as tz
import requests

from django.conf import settings
from django.db import connection
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

# constants
from ..core import constants as c

# permissions
from ..core.permissions import (
    IsDriverOrEscortUser, IsCustomerUser, OrderPermission
)

# models
from . import models as m
from ..account.models import User
from ..info.models import Route, Station, Product
from ..vehicle.models import Vehicle

# serializers
from . import serializers as s
from ..vehicle.serializers import VehiclePositionSerializer

# views
from ..core.views import TMSViewSet

# other
from ..g7.interfaces import G7Interface


class OrderCartViewSet(TMSViewSet):

    queryset = m.OrderCart.objects.all()
    serializer_class = s.OrderCartSerializer
    permission_classes = [IsCustomerUser]

    def create(self, request):
        context = {
            'product': request.data.pop('product'),
            'customer': request.user.customer_profile
        }

        serializer = self.serializer_class(
            data=request.data, context=context
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, pk=None):
        serializer_instance = self.get_object()

        context = {
            'product': request.data.pop('product')
        }

        serializer = self.serializer_class(
            serializer_instance,
            data=request.data,
            context=context,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def list(self, request):
        page = self.paginate_queryset(
            self.get_queryset().all()
        )

        serializer = self.serializer_class(
            page,
            many=True
        )

        return self.get_paginated_response(serializer.data)


class OrderViewSet(TMSViewSet):
    """
    Order Viewset
    """
    queryset = m.Order.objects.all()
    serializer_class = s.OrderSerializer
    permission_classes = [OrderPermission]

    def create(self, request):

        context = {
            'products': request.data.pop('products')
        }
        data = request.data
        if request.user.role == c.USER_ROLE_CUSTOMER:
            data['customer'] = {
                'id': request.user.customer_profile.id
            }
            data['order_source'] = c.ORDER_SOURCE_CUSTOMER
        else:
            data['order_source'] = c.ORDER_SOURCE_INTERNAL

        serializer = s.OrderSerializer(
            data=data, context=context
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, pk=None):
        serializer_instance = self.get_object()
        if serializer_instance.status == c.ORDER_STATUS_COMPLETE:
            return Response(
                {
                    'msg': 'Already finished'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        data = request.data
        context = {
            'products': request.data.pop('products')
        }
        if request.user.role == c.USER_ROLE_CUSTOMER:
            data['customer'] = {
                'id': request.user.customer_profile.id
            }
            data['order_source'] = c.ORDER_SOURCE_CUSTOMER
        else:
            data['order_source'] = c.ORDER_SOURCE_INTERNAL

        serializer = s.OrderSerializer(
            serializer_instance,
            data=data,
            context=context,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def list(self, request):
        page = self.paginate_queryset(
            self.get_queryset().all()
        )

        serializer = self.serializer_class(
            page,
            many=True
        )

        return self.get_paginated_response(serializer.data)

    @action(detail=True, url_path='jobs')
    def get_jobs(self, request, pk=None):
        order = self.get_object()
        serializer = s.JobAdminSerializer(
            order.jobs.all(),
            many=True
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    @action(detail=True, url_path='vehicle-status')
    def get_vehicle_status(self, request, pk=None):
        """
        Get the vehicle status like job progress, next job client, branches
        when admin make arrangement
        """
        order = self.get_object()
        query_str = """
            select id, plate_num, total_load, branches[1] as branch1,
            branches[2] as branch2, branches[3] as branch3
            from vehicle_vehicle
        """
        with connection.cursor() as cursor:
            cursor.execute(query_str)
            columns = [col[0] for col in cursor.description]
            vehicles = [dict(zip(columns, row)) for row in cursor.fetchall()]

            # get the current location of all registered vehicles
            body = {
                'plate_nums': [vehicle['plate_num'] for vehicle in vehicles],
                'fields': ['loc']
            }
            try:
                data = G7Interface.call_g7_http_interface(
                    'BULK_VEHICLE_STATUS_INQUIRY',
                    body=body
                )

                origins = []
                index = 0

                for key, value in data.items():
                    if value['code'] == 0:
                        vehicles[index]['g7_error'] = False
                        origins.append(','.join([
                            str(value['data']['loc']['lng']),
                            str(value['data']['loc']['lat'])
                        ]))
                    else:
                        vehicles[index]['g7_error'] = True

                    index = index + 1
                    # calculate the distance between new order loading
                    # and current position
                    destination = [
                        str(order.loading_station.longitude),
                        str(order.loading_station.latitude)
                    ]
                    queries = {
                        'key': settings.MAP_WEB_SERVICE_API_KEY,
                        'origins': ('|').join(origins),
                        'destination': (',').join(destination)
                    }
                    r = requests.get(
                        'https://restapi.amap.com/v3/distance', params=queries
                    )
                    response = r.json()
                    results = response['results']
                    index = 0
                    for vehicle in vehicles:
                        if vehicle['g7_error']:
                            vehicle['distance'] = None
                            vehicle['duration'] = None
                        else:
                            vehicle['distance'] =\
                                int(results[index]['distance']) / 1000
                            vehicle['duration'] =\
                                int(results[index]['duration']) / 3600
                            index = index + 1
            except Exception:
                for vehicle in vehicles:
                    vehicle['g7_error'] = True
                    vehicle['distance'] = None
                    vehicle['duration'] = None

            serializer = s.VehicleStatusOrderSerializer(
                vehicles,
                many=True
            )
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

    @action(
        detail=False, methods=['get'], url_path='me',
        permission_classes=[IsCustomerUser]
    )
    def get_customer_orders(self, request):
        queryset = m.Order.objects.filter(
            customer=request.user.customer_profile
        )

        order_status = request.query_params.get('status', None)
        if order_status == c.ORDER_STATUS_PENDING:
            queryset = queryset.filter(status=order_status)
        elif order_status == c.ORDER_STATUS_INPROGRESS:
            queryset = queryset.filter(status=order_status)
        elif order_status == c.ORDER_STATUS_COMPLETE:
            queryset = queryset.filter(status=order_status)

        page = self.paginate_queryset(queryset)

        serializer = s.OrderCustomerAppSerializer(page, many=True)

        return self.get_paginated_response(serializer.data)

    @action(detail=True, url_path='position')
    def get_all_vehicle_positions(self, request, pk=None):
        """
        Get the current location of all in-progress order-job vehicles
        This api will be called at most once when customer click monitoring
        After then vehicle positioning data will be notified via web sockets
        """
        order = self.get_object()
        if order.status == c.ORDER_STATUS_COMPLETE:
            return Response(
                {'order': 'This order is already completed'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if order.status == c.ORDER_STATUS_PENDING:
            return Response(
                {'order': 'This order is still in pending'},
                status=status.HTTP_400_BAD_REQUEST
            )

        plate_nums = order.jobs.filter(progress__gt=1).values_list(
            'vehicle__plate_num', flat=True
        )
        if len(plate_nums) == 0:
            return Response(
                {'job': 'Not job started'},
                status=status.HTTP_400_BAD_REQUEST
            )
        body = {
            'plate_nums': list(plate_nums),
            'fields': ['loc']
        }
        data = G7Interface.call_g7_http_interface(
            'BULK_VEHICLE_STATUS_INQUIRY',
            body=body
        )
        ret = []
        for key, value in data.items():
            if value['code'] == 0:
                ret.append(value)

        serializer = VehiclePositionSerializer(
            ret, many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class OrderProductViewSet(viewsets.ModelViewSet):
    """
    OrderProduct Viewset
    """
    serializer_class = s.OrderProductSerializer

    def get_queryset(self):
        return m.OrderProduct.objects.filter(
            order_loading_station__id=self.kwargs['orderloadingstation_pk']
        )


class JobViewSet(TMSViewSet):

    queryset = m.Job.objects.all()
    serializer_class = s.JobSerializer

    def create(self, request):
        print(request.data)
        order = get_object_or_404(m.Order, id=request.data.pop('order', None))
        if order.status == c.ORDER_STATUS_COMPLETE:
            return Response(
                {
                    'msg': 'Already finished'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        order_products = []
        for order_product in order.orderproduct_set.all():
            order_products.append({
                'product': order_product.product,
                'left_weight': order_product.weight - order_product.delivered_weight
            })

        jobs_data = request.data.pop('jobs', None)
        if jobs_data is None:
            return Response(
                {'data': 'No data is provied'},
                status=status.HTTP_200_OK
            )

        # validation check, weight validation, route validation
        errors = {}
        job_index = 0

        for job_data in jobs_data:
            job_data['total_weight'] = 0
            # check if the loading, quality, unloading stations is in route
            route_data = job_data.get('route', None)
            if route_data is None:
                if job_index not in errors:
                    errors[job_index] = {}
                errors[job_index]['route'] = 'Missing Route'

            job_data['route'] = get_object_or_404(
                Route, id=route_data.get('id', None)
            )

            loading_station_data = job_data.pop('loading_station', None)
            if loading_station_data is None:
                if job_index not in errors:
                    errors[job_index] = {}
                errors[job_index]['loading_station'] = 'Missing data'

            loading_station = get_object_or_404(
                Station, id=loading_station_data.get('id', None)
            )

            if job_data['route'].loading_station != loading_station:
                if job_index not in errors:
                    errors[job_index] = {}
                if 'route' not in errors[job_index]:
                    errors[job_index]['route'] = []
                errors[job_index]['route'] = ['loading']

            quality_station_data = job_data.pop('quality_station', None)
            if quality_station_data is None:
                if job_index not in errors:
                    errors[job_index] = {}
                errors[job_index]['quality_station'] = 'Missing data'

            quality_station = get_object_or_404(
                Station, id=quality_station_data.get('id', None)
            )

            if not job_data['is_same_station']:
                if job_data['route'].stations[1] != quality_station:
                    if job_index not in errors:
                        errors[job_index] = {}
                    if 'route' not in errors[job_index]:
                        errors[job_index]['route'] = []
                    errors[job_index]['route'].append('quality')

            vehicle_data = job_data.get('vehicle', None)
            if vehicle_data is None:
                if job_index not in errors:
                    errors[job_index] = {}
                errors[job_index]['vehicle'] = 'Missing data'

            job_data['vehicle'] = get_object_or_404(
                Vehicle, id=vehicle_data.get('id', None)
            )

            driver_data = job_data.get('driver', None)
            if driver_data is None:
                if job_index not in errors:
                    errors[job_index] = {}
                errors[job_index]['driver'] = 'Missing data'

            job_data['driver'] = get_object_or_404(
                User, id=driver_data.get('id', None)
            )

            escort_data = job_data.get('escort', None)
            if escort_data is None:
                if job_index not in errors:
                    errors[job_index] = {}
                errors[job_index]['escort'] = 'Missing data'

            job_data['escort'] = get_object_or_404(
                User, id=escort_data.get('id', None)
            )

            branch_index = 0
            job_data['stations'] = []
            job_data['stations'].append({
                'station': loading_station,
                'due_time': job_data['due_time'],
                'products': []
            })
            job_data['stations'].append({
                'station': quality_station,
                'due_time': job_data['due_time'],
                'products': []
            })

            for branch_data in job_data['branches']:
                branch_id = int(branch_data.get('branch').get('id'))
                branch_mission_weight = float(
                    branch_data.get('mission_weight')
                )

                job_data['total_weight'] += branch_mission_weight

                # check if the branch mission weight exceed vehicle branch load
                if job_data['vehicle'].branches[branch_id] < float(branch_data.get('mission_weight')):
                    if job_index not in errors:
                        errors[job_index] = {}

                    if branch_id not in errors[job_index]:
                        errors[job_index][branch_index] = {}

                    errors[job_index][branch_index]['branch_over_weight'] =\
                        'mission weight exceed vehicle branch actual load'

                product_data = branch_data.pop('product', None)
                product = get_object_or_404(
                    Product, id=product_data.get('id', None)
                )

                for order_product in order_products:
                    if order_product['product'] == product:
                        order_product['left_weight'] -= branch_mission_weight

                for i in range(0, 2):
                    job_data['stations'][i]['products'].append({
                        'product': product,
                        'branch': branch_id,
                        'mission_weight': branch_mission_weight
                    })

                unloading_stations_data = branch_data.pop('unloading_stations')

                for unloading_station_data in unloading_stations_data:
                    station_data = unloading_station_data.get(
                        'unloading_station'
                    )
                    station = get_object_or_404(
                        Station, id=station_data.get('id', None)
                    )

                    if station not in job_data['route'].unloading_stations:
                        if job_index not in errors:
                            errors[job_index] = {}
                        if 'route' not in errors[job_index]:
                            errors[job_index]['route'] = []
                        errors[job_index]['route'].append('unloading')

                    due_time = unloading_station_data.get(
                        'due_time'
                    )
                    unloading_station_mission_weight = float(unloading_station_data.get('mission_weight', 0))
                    branch_mission_weight -= unloading_station_mission_weight
                    for unloading_station in job_data['stations'][2:]:
                        if unloading_station['station'] == station:
                            unloading_station['products'].append({
                                'product': product,
                                'branch': branch_id,
                                'mission_weight': unloading_station_mission_weight
                            })
                            break

                    else:
                        job_data['stations'].append({
                            'station': station,
                            'due_time': due_time,
                            'products': [{
                                'product': product,
                                'branch': branch_id,
                                'mission_weight': unloading_station_mission_weight
                            }]
                        })

                if branch_mission_weight != 0:
                    if job_index not in errors:
                        errors[job_index] = {}
                    if branch_index not in errors[job_index]:
                        errors[job_index][branch_index] = {}

                    errors[job_index][branch_index]['station_over_weight'] =\
                        'sum of unloading weights overweight branch missin weight'

                branch_index += 1

            job_index += 1

        product_index = 0
        for order_product in order_products:
            if order_product['left_weight'] < 0:
                if 'order' not in errors:
                    errors['order'] = {}
                errors['order'][product_index] = 'arrange weight exceed order weight'

        if errors:
            return Response(
                errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        for job_data in jobs_data:
            job = m.Job.objects.create(
                order=order,
                vehicle=job_data['vehicle'],
                driver=job_data['driver'],
                escort=job_data['escort'],
                route=job_data['route'],
                total_weight=job_data['total_weight'],
                is_same_station=job_data['is_same_station']
            )

            station_index = 0
            for station in job_data['stations']:
                if station_index < 2:
                    step = station_index
                    station_index += 1
                else:
                    step = job_data['route'].stations.index(station['station'])
                    if job_data['is_same_station']:
                        step += 1

                job_station = m.JobStation.objects.create(
                   job=job,
                   station=station['station'],
                   step=step,
                   due_time=station['due_time']
                )

                for job_station_product in station['products']:
                    m.JobStationProduct.objects.create(
                        job_station=job_station,
                        **job_station_product
                    )

        if jobs_data is not None:
            order.arrangement_status = c.TRUCK_ARRANGEMENT_STATUS_INPROGRESS
            order.save()

        return Response(
            {'msg': 'Ok'},
            status=status.HTTP_200_OK
        )

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    @action(detail=True, methods=['post'], url_path='upload-loading-check')
    def upload_loading_station_check(self, request, pk=None):
        job = self.get_object()
        images = request.data.pop('images')
        product = get_object_or_404(Product, id=request.data.get('product').get('id'))

        loading_check, created = m.LoadingStationProductCheck.objects.get_or_create(
            job=job, product=product
        )

        loading_check.weight = request.data.pop('weight')
        loading_check.save()

        loading_check.images.all().delete()

        for image in images:
            image['loading_station'] = loading_check.id
            serializer = s.LoadingStationDocumentSerializer(data=image)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response(s.LoadingStationProductCheckSerializer(loading_check).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='upload-quality-check')
    def upload_quality_check(self, request, pk=None):
        job = self.get_object()
        images = request.data.pop('images')
        branch = request.data.get('branch', 0)

        quality_check, created = m.QualityCheck.objects.get_or_create(
            job=job, branch=branch
        )
        quality_check.density = request.data.pop('density')
        quality_check.additive = request.data.pop('additive')
        quality_check.save()

        job_qualitystation = job.jobstation_set.all()[1]

        job_qualitystation_product = get_object_or_404(
            m.JobStationProduct, job_station=job_qualitystation, branch=branch
        )
        job_qualitystation_product.volume = request.data.pop('volume')
        job_qualitystation_product.man_hole = request.data.pop('man_hole')
        job_qualitystation_product.branch_hole = request.data.pop('branch_hole')

        for image in images:
            image['job_station_product'] = job_qualitystation_product.id
            serializer = s.JobStationProductDocumentSerializer(data=image)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response(
            {'msg': 'Successfully uploaded'},
            status=status.HTTP_200_OK
        )

    @action(detail=False, url_path='vehicles')
    def get_vehicle_jobs_by_time(self, request):
        """
        Query the job list depending on vehicle plate number and time
        This api endpoint is used in playback in frontend
        """
        plate_num = request.query_params.get('plate_num', None)
        from_date = request.query_params.get('from', None)
        to_date = request.query_params.get('to', None)

        if plate_num is None or from_date is None or to_date is None:
            return Response(
                {
                    'result': {
                        'code': '1',
                        'msg': 'Improperly configured parameters'
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        # jobs = m.Job.objects.filter(
        #     Q(vehicle__plate_num=plate_num) & Q(started_on__gte=from_date) &
        #     (Q(finished_on__lte=to_date) | Q(finished_on=None))
        # ).order_by('started_on')

        jobs = m.Job.objects.filter(
            Q(vehicle__plate_num=plate_num) & Q(started_on__gte=from_date) &
            Q(finished_on__lte=to_date)
        ).order_by('started_on')

        serializer = s.JobByVehicleSerializer(
            jobs, many=True
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    @action(detail=True, url_path='playback')
    def get_vehicle_playback_by_job(self, request, pk=None):
        job = self.get_object()

        start_time = timezone.localtime(job.started_on).strftime(
            '%Y-%m-%d %H:%M:%S'
        )
        finish_time = timezone.localtime(job.finished_on).strftime(
            '%Y-%m-%d %H:%M:%S'
        )
        results = {
            'total_distance': 0,
            'paths': [],
            'meta': []
        }
        while 1:
            queries = {
                'plate_num': job.vehicle.plate_num,
                'from': start_time,
                'to': finish_time,
                'timeInterval': '10'
            }
            try:
                data = G7Interface.call_g7_http_interface(
                    'VEHICLE_HISTORY_TRACK_QUERY',
                    queries=queries
                )
                for x in data:
                    results['paths'].append([x.pop('lng'), x.pop('lat')])
                    results['total_distance'] += round(x['distance'] / 100)
                    x['distance'] = round(
                        results['total_distance'] / 1000, 2
                    )
                    x['time'] = datetime.fromtimestamp(
                        int(x['time'])/1000, tz=tz('Asia/Shanghai')
                    ).strftime('%Y-%m-%d %H:%M:%S')

                results['meta'].extend(data)

                if len(data) == 1000:
                    start_time = datetime.strptime(
                        data[999]['time'], '%Y-%m-%d %H:%M:%S'
                    )
                    start_time = start_time + timedelta(seconds=1)
                    start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')

                else:
                    break
            except Exception:
                results = {
                    'result': {
                        'code': '1',
                        'msg': 'g7 error'
                    }
                }
                break

        if 'total_distance' in results:
            results['total_distance'] = round(
                results['total_distance'] / 1000, 2
            )

        return Response(
            results,
            status=status.HTTP_200_OK
        )

    @action(detail=False, url_path='mileage')
    def get_mileage(self, request):
        page = self.paginate_queryset(
            m.Job.objects.all()
        )

        serializer = s.JobMileageSerializer(page, many=True)

        return self.get_paginated_response(serializer.data)

    @action(detail=False, url_path='job-documents')
    def get_all_documents(self, request):
        page = self.paginate_queryset(
            m.Job.completed_jobs.all()
        )
        serializer = s.JobDocumentSerializer(
            page,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(detail=True, url_path='documents')
    def get_documents(self, request, pk=None):
        job = self.get_object()
        serializer = s.JobDocumentSerializer(
            job,
            context={'request': request}
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    @action(detail=False, url_path='time')
    def get_time(self, request):
        page = self.paginate_queryset(
            m.Job.completed_jobs.all(),
        )

        serializer = s.JobTimeDurationSerializer(page, many=True)

        return self.get_paginated_response(serializer.data)

    @action(detail=False, url_path='driving')
    def get_driving(self, request):
        pass

    @action(detail=False, url_path='previous', permission_classes=[IsDriverOrEscortUser])
    def previous_jobs(self, request):
        serializer = s.JobDoneSerializer(
            request.user.jobs_as_driver.filter(
                finished_on__lte=timezone.now()
            ),
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    @action(detail=False, url_path='done', permission_classes=[IsDriverOrEscortUser])
    def done_jobs(self, request):
        page = self.paginate_queryset(
            request.user.jobs_as_driver.filter(
                progress=c.JOB_PROGRESS_COMPLETE
            ).order_by('-finished_on')
        )

        serializer = s.JobDoneSerializer(
            page,
            many=True
        )
        return self.get_paginated_response(serializer.data)

    @action(detail=False, url_path='current', permission_classes=[IsDriverOrEscortUser])
    def progress_jobs(self, request):
        job = request.user.jobs_as_driver.filter(
            ~(Q(progress=c.JOB_PROGRESS_NOT_STARTED) |
                Q(progress=c.JOB_PROGRESS_COMPLETE))
        ).first()

        # if job is None:
        #     job = request.user.driver_profile.jobs.filter(
        #         progress=c.JOB_PROGRESS_NOT_STARTED
        #     ).first()

        if job is not None:
            ret = s.JobCurrentSerializer(job).data
        else:
            ret = {}

        return Response(
            ret,
            status=status.HTTP_200_OK
        )

    @action(detail=False, url_path='future', permission_classes=[IsDriverOrEscortUser])
    def future_jobs(self, request):
        page = self.paginate_queryset(
            request.user.jobs_as_driver.filter(
                progress=c.JOB_PROGRESS_NOT_STARTED
            )
        )

        serializer = s.JobCurrentSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, url_path='update-progress', permission_classes=[IsDriverOrEscortUser])
    def progress_update(self, request, pk=None):
        job = self.get_object()

        if request.user.jobs_as_driver.exclude(id=job.id).filter(
            progress__gt=1
        ).exists():
            return Response(
                {'error': 'Cannot proceed more than 2 jobs simultaneously'},
                status=status.HTTP_400_BAD_REQUEST
            )

        current_progress = job.progress
        if current_progress == c.JOB_PROGRESS_COMPLETE:
            return Response(
                {
                    'progress': 'This is already completed progress',
                    'last_progress_finished_on': job.finished_on
                },
                status=status.HTTP_200_OK
            )

        if current_progress == c.JOB_PROGRESS_NOT_STARTED:
            job.started_on = timezone.now()
            last_progress_finished_on = None

            # set the vehicle status to in-work
            job.vehicle.status = c.VEHICLE_STATUS_INWORK
            job.vehicle.save()

            # set the driver & escrot to in-work
            job.driver.profile.status = c.WORK_STATUS_DRIVING
            job.escort.profile.status = c.WORK_STATUS_DRIVING
            job.driver.profile.save()
            job.escort.profile.save()
        else:
            current_station = job.jobstation_set.filter(
                is_completed=False
            ).first()

            sub_progress =\
                (current_progress - c.JOB_PROGRESS_TO_LOADING_STATION) % 4
            if sub_progress == 0:
                current_station.arrived_station_on = timezone.now()
                current_station.save()
                if current_station.step == 0:
                    last_progress_finished_on = job.started_on
                else:
                    last_progress_finished_on =\
                        current_station.previous_station.departure_station_on
            elif sub_progress == 1:
                current_station.started_working_on = timezone.now()
                last_progress_finished_on = current_station.arrived_station_on
                current_station.save()
            elif sub_progress == 2:
                current_station.finished_working_on = timezone.now()
                last_progress_finished_on = current_station.started_working_on
                current_station.save()
            elif sub_progress == 3:
                current_station.departure_station_on = timezone.now()
                last_progress_finished_on = current_station.finished_working_on
                current_station.is_completed = True
                current_station.save()

                if not current_station.has_next_station:
                    job.progress = c.JOB_PROGRESS_COMPLETE
                    job.finished_on = timezone.now()

                    # update job empty mileage
                    loading_station_arrived_on =\
                        job.jobstation_set.get(step=0).arrived_station_on

                    queries = {
                        'plate_num':
                            job.vehicle.plate_num,
                        'from':
                            job.started_on.strftime('%Y-%m-%d %H:%M:%S'),
                        'to':
                            loading_station_arrived_on.strftime(
                                '%Y-%m-%d %H:%M:%S'
                            )
                    }
                    data = G7Interface.call_g7_http_interface(
                        'VEHICLE_GPS_TOTAL_MILEAGE_INQUIRY',
                        queries=queries
                    )
                    job.empty_mileage = data['total_mileage']

                    # update job heavy mileage
                    queries = {
                        'plate_num':
                            job.vehicle.plate_num,
                        'from':
                            loading_station_arrived_on.strftime(
                                '%Y-%m-%d %H:%M:%S'
                            ),
                        'to':
                            job.finished_on.strftime(
                                '%Y-%m-%d %H:%M:%S'
                            )
                    }
                    job.heavy_mileage = data['total_mileage']
                    job.total_mileage =\
                        job.empty_mileage + job.heavy_mileage
                    job.highway_mileage = 0
                    job.normalway_mileage = 0
                    job.save()
                    return Response(
                        {
                            'progress': c.JOB_PROGRESS_COMPLETE,
                            'last_progress_finished_on':
                            last_progress_finished_on
                        },
                        status=status.HTTP_200_OK
                    )
        job.progress = current_progress + 1
        job.save()

        return Response(
            {
                'progress': job.progress,
                'last_progress_finished_on': last_progress_finished_on,
            },
            status=status.HTTP_200_OK
        )

    @action(detail=True, url_path="test/station-efence")
    def test_station_efence(self, request, pk=None):
        """
        This api is only used for test purpose
        """
        from ..core.redis import r

        job = self.get_object()
        if job.progress <= 1:
            return Response(
                {
                    'msg':
                    'enter & exit event test is only enabled for in-progress'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        event = request.query_params.get('type', 'in')
        if event == 'in':
            r.set('station_delta_distance', 10)
        elif event == 'out':
            r.set('station_delta_distance', 1000)
        return Response(
            {'msg': 'success'},
            status=status.HTTP_200_OK
        )

    @action(detail=False, url_path="test/blackdot-efence")
    def test_black_dot_efence(self, request, pk=None):
        from ..core.redis import r

        event = request.query_params.get('type', 'in')
        if event == 'in':
            r.set('blackdot_delta_distance', 10)
        elif event == 'out':
            r.set('blackdot_delta_distance', 1000)
        return Response(
            {'msg': 'success'},
            status=status.HTTP_200_OK
        )


class JobStationViewSet(viewsets.ModelViewSet):

    serializer_class = s.JobStationSerializer

    def get_queryset(self):
        return m.JobStation.objects.filter(
            job__id=self.kwargs['job_pk']
        )


class JobStationProductViewSet(viewsets.ModelViewSet):

    serializer_class = s.JobStationProductSerializer

    def get_queryset(self):
        return m.JobStationProduct.objects.filter(
            job_station__id=self.kwargs['job_station_pk']
        )

    @action(
        detail=True, url_path='upload-product-document', methods=['post']
    )
    def upload_product_document(self, request, job_pk=None,
                                job_station_pk=None, pk=None):
        """
        for driver app;
        driver shoud upload the product document in each station
        this api end point is used to upload the product document weight
        weight is different from mission weight
        """
        instance = self.get_object()
        images = request.data.pop('images', [])
        instance.man_hole = request.data.pop('man_hole', '')
        instance.branch_hole = request.data.pop('branch_hole', '')
        instance.volume = request.data.pop('volume', 0)
        instance.save()

        for image in images:
            image['job_station_product'] = instance.id
            serializer = s.JobStationProductDocumentSerializer(data=image)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response(
            {'msg': 'Successfully uploaded'},
            status=status.HTTP_200_OK
        )


class JobReportViewSet(viewsets.ModelViewSet):

    queryset = m.JobReport.objects.all()
    serializer_class = s.DriverJobReportSerializer

    @action(detail=False, url_path='me')
    def me(self, request):
        page = self.paginate_queryset(
            request.user.report.all()
        )
        serializer = s.DriverJobReportSerializer(
            page,
            many=True
        )
        return self.get_paginated_response(serializer.data)

        return Response(
            request.user.report.all()
        )
        return request.user


class OrderReportViewSet(viewsets.ModelViewSet):

    queryset = m.OrderReport.objects.all()
    serializer_class = s.CustomerAppOrderReportSerializer

    @action(detail=False, url_path='me')
    def me(self, request):
        page = self.paginate_queryset(
            request.user.customer_profile.monthly_reports.all()
        )
        serializer = s.CustomerAppOrderReportSerializer(
            page,
            many=True
        )
        return self.get_paginated_response(serializer.data)


class VehicleUserBindViewSet(TMSViewSet):

    serializer_class = s.VehicleUserBindSerializer

    def get_queryset(self):
        return m.VehicleUserBind.binds_by_admin.all()
