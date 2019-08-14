from rest_framework import status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response

from ..core import constants as c
from ..core.serializers import ChoiceSerializer
from ..core.views import TMSViewSet
from . import models as m
from . import serializers as s


class JWTAPIView(APIView):
    """
    Base API View that various JWT interactions inherit from.
    """
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data.get('user') or request.user
            token = serializer.validated_data.get('token')
            return Response({
                'token': token,
                'user': s.AuthSerializer(user).data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObtainJWTAPIView(JWTAPIView):
    """
    API View that receives a POST with username and password and user role
    Returns a JSON Web Token with user data
    """
    serializer_class = s.ObtainJWTSerializer


class VerifyJWTAPIView(JWTAPIView):
    """
    API View that checks the veracity of a token, returning the token and
    user data if it is valid.
    """
    serializer_class = s.VerifyJWTSerializer


class UserViewSet(TMSViewSet):
    """
    Viewset for User
    """
    queryset = m.User.objects.all()
    serializer_class = s.UserSerializer

    @action(detail=False, url_path="roles")
    def get_user_roles(self, request):
        serializer = ChoiceSerializer(
            [{'value': x, 'text': y} for (x, y) in c.USER_ROLE],
            many=True
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    @action(detail=False, url_path="member-roles")
    def get_member_roles(self, request):
        serializer = ChoiceSerializer(
            [
                {'value': x, 'text': y} for (x, y) in c.USER_ROLE
                if x != c.USER_ROLE_CUSTOMER
            ],
            many=True
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    @action(detail=False, url_path='company-members/short')
    def get_short_company_members(self, request):
        serializer = s.ShortCompanyMemberSerializer(
            m.User.companymembers.all(),
            many=True
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    @action(detail=False, url_path='staffs/short')
    def get_short_staff_users(self, request):
        serializer = s.ShortUserSerializer(
            m.User.staffs.all(),
            many=True
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    @action(detail=False, url_path='drivers/short')
    def get_short_driver_users(self, request):
        serializer = s.ShortUserSerializer(
            m.User.drivers.all(),
            many=True
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    @action(detail=False, url_path='escorts/short')
    def get_short_escort_users(self, request):
        serializer = s.ShortUserSerializer(
            m.User.escorts.all(),
            many=True
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    @action(detail=False, url_path='customers/short')
    def get_short_customer_users(self, request):
        serializer = s.ShortUserSerializer(
            m.User.customers.all(),
            many=True
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class UserPermissionViewSet(TMSViewSet):

    queryset = m.UserPermission.objects.all()
    serializer_class = s.UserPermissionSerializer
    short_serializer_class = s.ShortUserPermissionSerializer

    def create(self, request):
        data = request.data
        permission_data = request.data.pop('permissions')
        permissions = []
        for key, actions in permission_data.items():
            for action_name in actions:
                obj, created = m.Permission.objects.get_or_create(
                    page=key,
                    action=action_name
                )
                permissions.append(obj.id)

        data['permissions'] = permissions
        serializer = s.UserPermissionSerializer(
            data=data
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        instance = self.get_object()
        data = request.data
        permission_data = request.data.pop('permissions')
        permissions = []
        for key, actions in permission_data.items():
            for action_name in actions:
                obj, created = m.Permission.objects.get_or_create(
                    page=key,
                    action=action_name
                )
                permissions.append(obj.id)

        data['permissions'] = permissions
        serializer = s.UserPermissionSerializer(
            instance, data=data, partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
