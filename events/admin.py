from django.contrib import admin
from .models import Event, EventImages

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id','name','start_date','end_date','event_type','event_status')
    list_filter = ('event_status','event_type')
    search_fields = ('name','place','district')

@admin.register(EventImages)
class EventImagesAdmin(admin.ModelAdmin):
    list_display = ('id','event','is_primary')
