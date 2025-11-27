from django.contrib import admin
from .models import EventType

@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('id','event_type')
    search_fields = ('event_type',)
