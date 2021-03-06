from django.db import models

from ..core import constants as c

from . import managers

# models
# from ..core.models import ApprovedModel
from ..account.models import User
from ..hr.models import Department
from ..info.models import OtherCostType, TicketType
from ..vehicle.models import Vehicle


# class ParkingRequest(ApprovedModel):

#     job = models.ForeignKey(
#         Job,
#         on_delete=models.SET_NULL,
#         null=True
#     )

#     vehicle = models.ForeignKey(
#         Vehicle,
#         on_delete=models.CASCADE,
#         related_name='parking_requests'
#     )

#     driver = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='parking_requests_as_driver'
#     )

#     escort = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='parking_requests_as_escort'
#     )

#     place = models.CharField(
#         max_length=100
#     )


# class DriverChangeRequest(ApprovedModel):

#     job = models.ForeignKey(
#         Job,
#         on_delete=models.CASCADE
#     )

#     old_driver = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='driver_change_requests'
#     )

#     new_driver = models.ForeignKey(
#         User,
#         on_delete=models.SET_NULL,
#         null=True,
#         related_name='driver_change_assigned'
#     )

#     change_time = models.DateTimeField(
#         null=True,
#         blank=True
#     )

#     change_place = models.CharField(
#         max_length=100,
#         null=True,
#         blank=True
#     )

#     class Meta:
#         ordering = ['approved', '-approved_time', '-request_time']
#         unique_together = ['job', 'old_driver']


# class EscortChangeRequest(ApprovedModel):

#     job = models.ForeignKey(
#         Job,
#         on_delete=models.CASCADE
#     )

#     old_escort = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='escort_change_requests'
#     )

#     new_escort = models.ForeignKey(
#         User,
#         on_delete=models.SET_NULL,
#         null=True,
#         related_name='escort_change_assigned'
#     )

#     change_time = models.DateTimeField(
#         null=True,
#         blank=True
#     )

#     change_place = models.CharField(
#         max_length=100,
#         null=True,
#         blank=True
#     )

#     class Meta:
#         ordering = ['approved', '-approved_time', '-request_time']
#         unique_together = ['job', 'old_escort']


class BasicRequest(models.Model):

    requester = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='my_requests'
    )

    request_type = models.PositiveIntegerField(
        choices=c.REQUEST_TYPE,
        default=c.REQUEST_TYPE_REST
    )

    request_time = models.DateTimeField(
        auto_now_add=True
    )

    approved = models.BooleanField(
        null=True,
        blank=True
    )

    approved_time = models.DateTimeField(
        null=True,
        blank=True
    )

    is_cancelled = models.BooleanField(
        default=False
    )

    cancelled_time = models.DateTimeField(
        null=True,
        blank=True,
    )

    description = models.TextField(
        null=True,
        blank=True
    )

    approvers = models.ManyToManyField(
        User,
        through='RequestApprover',
        through_fields=('request', 'approver'),
        related_name='request_as_approver'
    )

    ccs = models.ManyToManyField(
        User,
        through='RequestCC',
        through_fields=('request', 'cc'),
        related_name='request_as_cc'
    )

    objects = models.Manager()
    active_requests = managers.ActiveRequestsManager()
    cancelled_requests = managers.CancelledRequestsManager()
    approved_requests = managers.ApprovedRequestsManager()
    unapproved_requests = managers.UnApprovedRequestsManager()

    @property
    def approvers_count(self):
        return self.approvers.all().count()

    @property
    def status(self):
        if self.is_cancelled:
            return '取消审批'

        if self.approved is None:
            return '审批中'
        elif self.approved is True:
            return '审批完成'
        elif self.approved is False:
            return '审批拒绝'

    class Meta:
        ordering = ['approved', '-approved_time', '-request_time']


class RequestApprover(models.Model):

    request = models.ForeignKey(
        BasicRequest,
        on_delete=models.CASCADE
    )

    approver_type = models.CharField(
        max_length=1,
        choices=c.APPROVER_TYPE,
        default=c.APPROVER_TYPE_MEMBER
    )

    approver = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    approved = models.BooleanField(
        null=True, blank=True
    )

    approved_time = models.DateTimeField(
        null=True, blank=True
    )

    step = models.PositiveIntegerField(
        default=0
    )

    description = models.TextField(
        null=True, blank=True
    )

    class Meta:
        ordering = [
            'request',
            'step',
        ]


class RequestCC(models.Model):

    request = models.ForeignKey(
        BasicRequest,
        on_delete=models.CASCADE
    )

    cc_type = models.CharField(
        max_length=1,
        choices=c.CC_TYPE,
        default=c.CC_TYPE_MEMBER
    )

    cc = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    is_read = models.BooleanField(
        default=False
    )

    read_time = models.DateTimeField(
        auto_now=True
    )


class RequestDocument(models.Model):

    request = models.ForeignKey(
        BasicRequest,
        on_delete=models.CASCADE,
        related_name='images'
    )

    document = models.ImageField()


class RestRequest(models.Model):

    request = models.OneToOneField(
        BasicRequest,
        on_delete=models.CASCADE,
        related_name='rest_request'
    )

    category = models.CharField(
        max_length=1,
        choices=c.REST_REQUEST_CATEGORY,
        default=c.REST_REQUEST_ILL
    )

    from_date = models.DateField()

    to_date = models.DateField()


class VehicleRepairRequest(models.Model):

    request = models.OneToOneField(
        BasicRequest,
        on_delete=models.CASCADE,
        related_name='vehicle_repair_request'
    )

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE
    )

    category = models.CharField(
        max_length=1,
        choices=c.VEHICLE_REPAIR_REQUEST_CATEGORY,
        default=c.VEHICLE_REPAIR_REQUEST_CATEGORY_BRAKE
    )


class SelfDrivingPaymentRequest(models.Model):

    request = models.OneToOneField(
        BasicRequest,
        on_delete=models.CASCADE,
        related_name='self_driving_request'
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        related_name='self_driving_requests'
    )

    plate_num = models.CharField(
        max_length=100
    )

    line = models.CharField(
        max_length=100
    )

    mileage = models.DecimalField(
        default=0,
        max_digits=10,
        decimal_places=2
    )

    amount = models.DecimalField(
        default=0,
        max_digits=10,
        decimal_places=2
    )


class InvoicePaymentRequest(models.Model):

    request = models.OneToOneField(
        BasicRequest,
        on_delete=models.CASCADE,
        related_name='invoice_payment_request'
    )

    other_cost_type = models.ForeignKey(
        OtherCostType,
        on_delete=models.SET_NULL,
        null=True
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True
    )

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.SET_NULL,
        null=True
    )

    paid_on = models.DateField()

    amount = models.DecimalField(
        default=0,
        max_digits=10,
        decimal_places=2
    )

    ticket_type = models.ForeignKey(
        TicketType,
        on_delete=models.SET_NULL,
        null=True
    )
