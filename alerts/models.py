from django.db import models
from ingest.models import IngestionJob


class Event(models.Model):
    job = models.ForeignKey(IngestionJob, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    user = models.CharField(max_length=150)
    src_ip = models.CharField(max_length=45)
    action = models.CharField(max_length=10)  # SUCCESS / FAIL


class Alert(models.Model):
    job = models.ForeignKey(IngestionJob, on_delete=models.CASCADE)
    rule_name = models.CharField(max_length=100)
    severity = models.IntegerField(default=0)  # 0-100
    entity_type = models.CharField(max_length=10)  # IP or USER
    entity_value = models.CharField(max_length=150)
    window_start = models.DateTimeField()
    window_end = models.DateTimeField()
    reason = models.TextField()

    mitre_tactic = models.CharField(max_length=100, blank=True, default="")
    mitre_technique_id = models.CharField(max_length=50, blank=True, default="")
    mitre_technique_name = models.CharField(max_length=200, blank=True, default="")

    
    created_at = models.DateTimeField(auto_now_add=True)
    


