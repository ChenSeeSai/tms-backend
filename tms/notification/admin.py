from django.contrib import admin
from . import models as m


@admin.register(m.Notification)
class NotificationAdmin(admin.ModelAdmin):
    pass


@admin.register(m.Event)
class EventAdmin(admin.ModelAdmin):
    pass


@admin.register(m.G7MQTTEvent)
class G7MQTTEventAdmin(admin.ModelAdmin):
    pass
