from django.http import HttpResponse
from reportlab.pdfgen import canvas

from django.shortcuts import render, get_object_or_404
from .models import Alert


def alert_list(request):
    alerts = Alert.objects.order_by("-created_at")
    return render(request, "alerts/alert_list.html", {"alerts": alerts})


def alert_detail(request, alert_id):
    alert = get_object_or_404(Alert, id=alert_id)
    return render(request, "alerts/alert_detail.html", {"alert": alert})
def alert_pdf(request, alert_id):
    alert = get_object_or_404(Alert, id=alert_id)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="alert_{alert.id}.pdf"'

    p = canvas.Canvas(response)
    y = 800

    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, "SOC Incident Report")
    y -= 30

    # Body
    p.setFont("Helvetica", 12)
    lines = [
        f"Alert ID: {alert.id}",
        f"Rule: {alert.rule_name}",
        f"Severity: {alert.severity}",
        f"Entity: {alert.entity_type}: {alert.entity_value}",
        f"Reason: {alert.reason}",
        f"Window: {alert.window_start} -> {alert.window_end}",
        "",
        "MITRE ATT&CK Mapping:",
        f"Tactic: {alert.mitre_tactic}",
        f"Technique: {alert.mitre_technique_id} - {alert.mitre_technique_name}",
        "",
        "Recommended Action:",
        "1) Verify source IP reputation",
        "2) Check if the user account is compromised",
        "3) Consider blocking IP / enforcing MFA",
    ]

    for line in lines:
        p.drawString(50, y, line)
        y -= 18
        if y < 80:
            p.showPage()
            y = 800
            p.setFont("Helvetica", 12)

    p.showPage()
    p.save()
    return response
