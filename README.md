# SOC-EDR System

## Overview

SOC-EDR (Security Operations Center - Endpoint Detection and Response) is a security monitoring platform designed to collect endpoint events, detect suspicious activities, manage alerts, and assist analysts during investigations.

The system consists of multiple modules developed as part of the  project.

---

## Project Modules

- **Backend** (FastAPI)
  - Event Management
  - Alert Management
  - Dashboard Statistics

- **Frontend** (WinUI/Desktop Application)
  - Dashboard
  - Alert Management
  - Investigation Interface

- **Detection Engine**
  - Sysmon Log Processing
  - Sigma Rule Matching
  - MITRE ATT&CK Mapping

- **AI Module** *(Planned)*
  - Alert Explanation
  - Investigation Recommendations

---

## Technology Stack

- Python
- FastAPI
- SQLite
- WinUI
- Sysmon
- Sigma Rules

---

## Repository Structure

```text
SOC-EDR-SYSTEM/
├── backend/
├── frontend/
├── detection/
└── README.md
```

---

## Running the Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## Documentation

Backend API documentation is available in:

```
backend/API_DOCUMENTATION.md
```

---
