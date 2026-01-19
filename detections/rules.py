from .mitre import get_mitre_mapping

from datetime import timedelta
from django.utils import timezone

from alerts.models import Event, Alert


def detect_bruteforce(job, fail_threshold=10, window_minutes=5):
    """
    Brute Force Detection (Beginner version):
    If an IP has >= fail_threshold failed logins in the uploaded job,
    we create a SOC alert for that IP.
    """

    # Get all failed events for this job
    failed_events = Event.objects.filter(job=job, action="FAIL")

    # Count number of FAIL events per IP
    ip_fail_counts = {}

    for event in failed_events:
        ip_fail_counts[event.src_ip] = ip_fail_counts.get(event.src_ip, 0) + 1

    created_alerts = 0

    # Create alerts for suspicious IPs
    for ip, fail_count in ip_fail_counts.items():
        if fail_count >= fail_threshold:
            rule_name = "Brute Force Login Attempts"
            mitre = get_mitre_mapping(rule_name)
            Alert.objects.create(
                job=job,
                rule_name=rule_name,
                severity=80,
                entity_type="IP",
                entity_value=ip,
                window_start=timezone.now() - timedelta(minutes=window_minutes),
                window_end=timezone.now(),
                reason=f"{fail_count} failed login attempts from IP {ip}",
                mitre_tactic=mitre["tactic"],
                mitre_technique_id=mitre["technique_id"],
                mitre_technique_name=mitre["technique_name"],
)
            created_alerts += 1

    return created_alerts
