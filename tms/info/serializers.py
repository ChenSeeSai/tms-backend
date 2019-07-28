from django.shortcuts import get_object_or_404

from rest_framework import serializers
from ..core import constants as c

# models
from . import models as m
from ..hr.models import CustomerProfile

# serializers
from ..core.serializers import TMSChoiceField
from ..hr.serializers import ShortCustomerProfileSerializer


class ShortProductDisplaySerializer(serializers.ModelSerializer):

    class Meta:
        model = m.Product
        fields = (
            'name',
        )


class ShortProductSerializer(serializers.ModelSerializer):
    """
    Serializer for short data of Product
    """
    weight_measure_unit = TMSChoiceField(choices=c.PRODUCT_WEIGHT_MEASURE_UNIT)

    class Meta:
        model = m.Product
        fields = (
            'id', 'name', 'price', 'weight_measure_unit'
        )


class ShortProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = m.ProductCategory
        fields = (
            'id', 'name'
        )


class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = m.ProductCategory
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Product
    """
    category = ProductCategorySerializer(read_only=True)
    weight_measure_unit = TMSChoiceField(choices=c.PRODUCT_WEIGHT_MEASURE_UNIT)

    class Meta:
        model = m.Product
        fields = '__all__'

    def create(self, validated_data):
        category_data = self.context.get('category')
        if category_data is None:
            raise serializers.ValidationError({
                'category': 'Category data is missing'
            })
        try:
            category = m.ProductCategory.objects.get(
                id=category_data.get('id', None)
            )
        except m.ProductCategory.DoesNotExist:
            raise serializers.ValidationError({
                'category': 'Such category does not exist'
            })

        return m.Product.objects.create(
            category=category,
            **validated_data
        )

    def update(self, instance, validated_data):
        category_data = self.context.get('category')
        if category_data is None:
            raise serializers.ValidationError({
                'category': 'Category data is missing'
            })
        try:
            category = m.ProductCategory.objects.get(
                id=category_data.get('id', None)
            )
        except m.ProductCategory.DoesNotExist:
            raise serializers.ValidationError({
                'category': 'Such category does not exist'
            })

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.category = category
        instance.save()
        return instance

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['price_display'] =\
            str(instance.price) + '元 / ' +\
            str(instance.unit_weight) +\
            str(instance.get_weight_measure_unit_display())

        return ret


class ShortStationSerializer(serializers.ModelSerializer):
    """
    Serializer for short data of Loading Station
    """
    class Meta:
        model = m.Station
        fields = (
            'id', 'name', 'contact', 'mobile', 'address'
        )


class ShortStationPointSerializer(serializers.ModelSerializer):

    lnglat = serializers.SerializerMethodField()

    class Meta:
        model = m.Station
        fields = (
            'lnglat',
        )

    def get_lnglat(self, obj):
        return [obj.longitude, obj.latitude]


class StationPointSerializer(serializers.ModelSerializer):

    lnglat = serializers.SerializerMethodField()

    class Meta:
        model = m.Station
        fields = (
            'id', 'name', 'station_type', 'lnglat',
        )

    def get_lnglat(self, obj):
        return [obj.longitude, obj.latitude]


class StationSerializer(serializers.ModelSerializer):
    """
    Serializer for Station
    """
    products = ShortProductSerializer(many=True, read_only=True)
    customer = ShortCustomerProfileSerializer(read_only=True)
    working_time_measure_unit = TMSChoiceField(
        choices=c.TIME_MEASURE_UNIT, required=False
    )
    average_time_measure_unit = TMSChoiceField(
        choices=c.TIME_MEASURE_UNIT, required=False
    )
    price_vary_duration_unit = TMSChoiceField(
        choices=c.PRICE_VARY_DURATION_UNIT, required=False
    )

    class Meta:
        model = m.Station
        fields = '__all__'

    def create(self, validated_data):
        products = self.context.get('products', None)
        customer = self.context.get('customer', None)
        station_type = validated_data.get('station_type', None)

        # validation if the station name exists already
        name = validated_data.get('name', None)
        if m.Station.objects.filter(
            station_type=station_type, name=name
        ).exists():
            raise serializers.ValidationError({
                'name': 'Already existts'
            })

        if station_type == c.STATION_TYPE_LOADING_STATION and products is None:
            raise serializers.ValidationError({
                'product': 'Product data is missing'
            })

        if station_type == c.STATION_TYPE_UNLOADING_STATION\
           and customer is None:
            raise serializers.ValidationError({
                'customer': 'Customer data is missing'
            })

        if customer is not None:
            try:
                customer = CustomerProfile.objects.get(
                    id=customer.get('id', None)
                )
            except CustomerProfile.DoesNotExist:
                customer = None

        station = m.Station.objects.create(
            **validated_data,
            customer=customer
        )

        if station_type == c.STATION_TYPE_LOADING_STATION:
            for product in products:
                product = get_object_or_404(
                    m.Product, id=product.get('id', None)
                )
                station.products.add(product)

        return station

    def update(self, instance, validated_data):
        products = self.context.get('products', None)
        customer = self.context.get('customer', None)
        station_type = validated_data.get('station_type', None)

        # validation if the station name exists already
        name = validated_data.get('name', None)
        if m.Station.objects.exclude(id=instance.id).filter(
            station_type=station_type, name=name
        ).exists():
            raise serializers.ValidationError({
                'name': 'Already existts'
            })

        if station_type == c.STATION_TYPE_LOADING_STATION and products is None:
            raise serializers.ValidationError({
                'product': 'Product data is missing'
            })

        if station_type == c.STATION_TYPE_UNLOADING_STATION\
           and customer is None:
            raise serializers.ValidationError({
                'customer': 'Customer data is missing'
            })

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if customer is not None:
            try:
                customer = CustomerProfile.objects.get(
                    id=customer.get('id', None)
                )
            except CustomerProfile.DoesNotExist:
                customer = None

        instance.customer = customer

        if station_type == c.STATION_TYPE_LOADING_STATION:
            instance.products.clear()
            for product in products:
                product = get_object_or_404(
                    m.Product, id=product.get('id', None)
                )
                instance.products.add(product)

        instance.save()
        return instance


class WorkStationSerializer(serializers.ModelSerializer):
    """
    Serializer for Loading Station, Unloading Station, Quality Station
    """
    products = ShortProductSerializer(many=True, read_only=True)
    customer = ShortCustomerProfileSerializer(read_only=True)

    class Meta:
        model = m.Station
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        ret['working_time_display'] =\
            str(instance.price) + '元/' +\
            str(instance.working_time) +\
            str(instance.get_working_time_measure_unit_display())

        ret['average_time_display'] =\
            str(instance.average_time) +\
            str(instance.get_average_time_measure_unit_display())

        return ret


class OilStationSerializer(serializers.ModelSerializer):
    """
    Serializer for Oil Station
    """
    class Meta:
        model = m.Station
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['price_vary_display'] = str(instance.price_vary_duration) +\
            '个' + str(instance.get_price_vary_duration_unit_display())

        return ret


class BlackDotSerializer(serializers.ModelSerializer):

    class Meta:
        model = m.Station
        fields = (
            'id', 'name', 'longitude', 'latitude', 'radius'
        )


class ShortRouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = m.Route
        fields = (
            'id', 'name'
        )


class RouteSerializer(serializers.ModelSerializer):

    # policy = TMSChoiceField(choices=c.ROUTE_PLANNING_POLICY)

    class Meta:
        model = m.Route
        fields = '__all__'


class PathStationNameField(serializers.ListField):

    def to_representation(self, value):
        paths = m.Station.workstations.filter(id__in=value)
        paths = dict([(point.id, point) for point in paths])

        serializer = StationPointSerializer(
            [paths[id] for id in value],
            many=True
        )
        return serializer.data


class RouteDataViewSerializer(serializers.ModelSerializer):

    path = PathStationNameField()
    # policy = TMSChoiceField(choices=c.ROUTE_PLANNING_POLICY)

    class Meta:
        model = m.Route
        fields = '__all__'


class PathLngLatField(serializers.ListField):

    def to_representation(self, value):
        paths = m.Station.objects.filter(id__in=value)
        paths = dict([(point.id, point) for point in paths])

        serializer = ShortStationPointSerializer(
            [paths[id] for id in value],
            many=True
        )
        return serializer.data


class RoutePointSerializer(serializers.ModelSerializer):

    path = PathLngLatField()

    class Meta:
        model = m.Route
        fields = (
            'id', 'path'
        )
