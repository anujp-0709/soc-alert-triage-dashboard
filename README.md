# SOC Alert Triage Dashboard (Django)

A mini SOC-style tool that ingests authentication logs, detects suspicious activity, creates triage-ready alerts, maps detections to MITRE ATT&CK, exports incident PDFs, and serves a REST API with interactive docs.

## Features
- Upload authentication log CSV → store events in DB
- Run detections (currently: Brute Force rule)
- Alerts list + alert detail views
- MITRE ATT&CK mapping (Credential Access / T1110 Brute Force)
- Export Incident Report PDF from alert detail
- API endpoints with Swagger docs (Django Ninja)

## Screenshots
Add screenshots here:
### Home
![Home](assets/home.png)
### Upload Logs
![Upload](assets/upload.png)
### Run Detections
![Run Detections](assets/run_detections.png)
### Alerts List
![Alerts List](assets/alerts_list.png)
### Alert Detail + MITRE
![Alert Detail](assets/alert_detail_mitre.png)
### API Docs
![API Docs](assets/api_docs.png)

## How to Run (Local)
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Mac/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
