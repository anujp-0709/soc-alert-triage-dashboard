from typing import Optional
from ninja import NinjaAPI
from alerts.models import Alert

api = NinjaAPI(title="SOC Alert Triage API")


@api.get("/alerts")
def list_alerts(
    request,
    severity: Optional[int] = None,
    entity_type: Optional[str] = None,
    entity_value: Optional[str] = None,
    rule_name: Optional[str] = None,
    job_id: Optional[int] = None,
    limit: int = 100,
):
    qs = Alert.objects.all().order_by("-created_at")

    if severity is not None:
        qs = qs.filter(severity=severity)

    if entity_type:
        qs = qs.filter(entity_type__iexact=entity_type)

    if entity_value:
        qs = qs.filter(entity_value=entity_value)

    if rule_name:
        qs = qs.filter(rule_name__icontains=rule_name)

    if job_id is not None:
        qs = qs.filter(job_id=job_id)

    qs = qs[: min(limit, 500)]

    return [
        {
            "id": a.id,
            "rule_name": a.rule_name,
            "severity": a.severity,
            "entity_type": a.entity_type,
            "entity_value": a.entity_value,
            "reason": a.reason,
            "window_start": a.window_start.isoformat(),
            "window_end": a.window_end.isoformat(),
            "mitre_tactic": a.mitre_tactic,
            "mitre_technique_id": a.mitre_technique_id,
            "mitre_technique_name": a.mitre_technique_name,
            "created_at": a.created_at.isoformat(),
            "job_id": a.job_id,
        }
        for a in qs
    ]


@api.get("/alerts/{alert_id}")
def get_alert(request, alert_id: int):
    a = Alert.objects.get(id=alert_id)
    return {
        "id": a.id,
        "rule_name": a.rule_name,
        "severity": a.severity,
        "entity_type": a.entity_type,
        "entity_value": a.entity_value,
        "reason": a.reason,
        "window_start": a.window_start.isoformat(),
        "window_end": a.window_end.isoformat(),
        "mitre_tactic": a.mitre_tactic,
        "mitre_technique_id": a.mitre_technique_id,
        "mitre_technique_name": a.mitre_technique_name,
        "created_at": a.created_at.isoformat(),
    }
