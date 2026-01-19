from django.shortcuts import render
from django.utils.dateparse import parse_datetime
import pandas as pd

from ingest.models import IngestionJob
from alerts.models import Event


def upload_logs(request):
    message = None

    if request.method == "POST" and request.FILES.get("logfile"):
        file = request.FILES["logfile"]

        # 1) Create a job
        job = IngestionJob.objects.create(filename=file.name, status="PENDING")

        # 2) Read CSV using pandas
        df = pd.read_csv(file)

        # 3) Validate required columns
        required_cols = {"timestamp", "user", "src_ip", "action"}
        if not required_cols.issubset(df.columns):
            job.status = "FAILED"
            job.save()
            message = f"CSV must contain columns: {required_cols}"
            return render(request, "ingest/upload.html", {"message": message})

        # 4) Insert events
        events_to_create = []
        for _, row in df.iterrows():
            ts = parse_datetime(str(row["timestamp"]))

            # If timestamp doesn't parse, skip
            if ts is None:
                continue

            events_to_create.append(
                Event(
                    job=job,
                    timestamp=ts,
                    user=str(row["user"]),
                    src_ip=str(row["src_ip"]),
                    action=str(row["action"]).upper(),
                )
            )

        Event.objects.bulk_create(events_to_create)

        # 5) Update job stats
        job.total_events = len(events_to_create)
        job.status = "DONE"
        job.save()

        message = f"Uploaded {job.total_events} events successfully!"

    return render(request, "ingest/upload.html", {"message": message})

