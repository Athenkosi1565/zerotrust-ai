ZeroTrust AI - Identity Security Investigation Platform

ZeroTrust AI is a full-stack, modular identity security analytics and threat detection platform. It ingests identity event streams (such as sign-ins and authentication attempts), persists them in a secure relational database, applies automated detection engineering rules, and surfaces security findings via a modern, real-time web dashboard.

🏗️ Architecture & Tech Stack

Backend: Python, FastAPI, SQLAlchemy, SQLite, Pydantic

Frontend: Next.js (App Router), TypeScript, Tailwind CSS

Detection Engineering: Rule-based identity analytics engine (e.g., Brute-force & Failed Sign-in detection)

📁 Project Structure

zerotrust-ai/
├── backend/
│   ├── app/
│   │   ├── api/routes.py          # FastAPI endpoints (/events, /findings, /analyze)
│   │   ├── core/config.py         # Application configuration
│   │   └── main.py                # FastAPI entrypoint with CORS middleware
│   ├── data/
│   │   └── identity_events.json   # Synthetic identity event logs
│   ├── db/
│   │   ├── database.py            # SQLite session management
│   │   └── models.py              # SQLAlchemy ORM database models
│   ├── rules/
│   │   └── failed_signins.py      # Detection rule logic (ID-001)
│   └── services/
│       └── db_service.py          # Database operations & data parsing services
└── frontend/
    ├── src/
    │   ├── app/page.tsx           # Main Next.js dashboard view
    │   ├── components/            # UI Components (SummaryCards, FindingsTable, EventTimeline)
    │   └── lib/api.ts             # API client services
    └── .env.local                 # Frontend environment configurations


🚀 Getting Started & Installation

Follow these instructions to run the full-stack application locally.

1. Clone or Open the Project

Open your workspace root folder (zerotrust-ai) in VS Code.

2. Start the Backend (FastAPI)

Open a terminal in VS Code and activate your Python virtual environment:

# Windows PowerShell
& .venv\Scripts\Activate.ps1


Run the FastAPI development server using Uvicorn:

python -m uvicorn app.main:app --app-dir backend --reload


The backend API will be available at http://localhost:8000. Interactive API docs can be viewed at http://localhost:8000/docs.

3. Start the Frontend (Next.js Dashboard)

Open a second terminal in VS Code and navigate to the frontend directory:

cd frontend


Run the Next.js development server:

npm run dev


The frontend dashboard will be available at http://localhost:3001 (or http://localhost:3000).

🛡️ Core Features

Automated Event Ingestion: Loads structured identity events from JSON datasets and normalizes timestamps into timezone-aware datetime objects for secure SQL storage.

Detection Engineering Rules: Evaluates sliding windows of user activity to detect suspicious patterns, such as multiple failed authentication attempts (ID-001).

Interactive Security Dashboard: Displays live summary cards, investigation findings table with severity badges, and a chronological event stream timeline.

CORS & API Security: Seamlessly connects client-side Next.js applications with backend FastAPI services under strict origin policies.
