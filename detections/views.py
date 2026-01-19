from django.shortcuts import render
from ingest.models import IngestionJob
from .rules import detect_bruteforce


def run_detections(request):
    message = None

    # Get the latest uploaded job
    job = IngestionJob.objects.order_by("-created_at").first()

    if not job:
        message = "No CSV uploaded yet. Please upload a CSV first."
        return render(request, "detections/run.html", {"message": message})

    if request.method == "POST":
        created = detect_bruteforce(job)
        message = f"Detection complete. Created {created} brute force alert(s)."

    return render(request, "detections/run.html", {"job": job, "message": message})
