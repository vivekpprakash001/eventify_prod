from django.db import models

class EventType(models.Model):
    event_type = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.event_type

    class Meta:
        db_table = 'master_data_event_type'
