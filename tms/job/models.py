from django.db import models

from . import managers
from ..core import constants
from ..account.models import StaffProfile
from ..vehicle.models import Vehicle
from ..order.models import OrderProductDeliver


class Job(models.Model):
    """
    Job model
    """
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE
    )

    driver = models.ForeignKey(
        StaffProfile,
        on_delete=models.CASCADE,
        related_name='jobs_as_primary'
    )

    escort = models.ForeignKey(
        StaffProfile,
        on_delete=models.CASCADE,
        related_name='jobs_as_escort',
    )

    progress = models.CharField(
        max_length=2,
        choices=constants.JOB_PROGRESS,
        default=constants.JOB_PROGRESS_NOT_STARTED
    )

    started_at = models.DateTimeField(
        null=True,
        blank=True
    )

    arrived_at_loading_station = models.DateTimeField(
        null=True,
        blank=True
    )

    arrived_at_quality_station = models.DateTimeField(
        null=True,
        blank=True
    )

    finished_at = models.DateTimeField(
        null=True,
        blank=True
    )

    missions = models.ManyToManyField(
        OrderProductDeliver,
        through='Mission'
    )

    objects = models.Manager()
    pendings = managers.PendingJobManager()
    inprogress = managers.InProgressJobManager()
    completeds = managers.CompleteJobManager()


class Mission(models.Model):

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )

    mission = models.ForeignKey(
        OrderProductDeliver,
        on_delete=models.CASCADE
    )

    arrived_at_unloading_station = models.DateTimeField(
        null=True,
        blank=True
    )

    loading_weight = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    unloading_weight = models.PositiveIntegerField(
        null=True,
        blank=True
    )