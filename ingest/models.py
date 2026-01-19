from django.db import models

class IngestionJob(models.Model):
    filename = models.CharField(max_length=255)
    status = models.CharField(max_length=20, default="PENDING")
    total_events = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.filename}"
