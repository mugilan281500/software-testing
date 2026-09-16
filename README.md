# 🏦 BankSecure API Guard — Intelligent Banking Security Platform

**Intelligent API Security & Functional Testing Framework with Real-Time Risk Monitoring, Behavioral Anomaly Detection, and Automated Threat Flagging for Banking Interfaces.**

---

## 🚀 QUICK START & RUN PROCEDURES

### Prerequisites
- **Python**: 3.10+ (Recommended Python 3.12)
- **Node.js**: v18+ & `npm`
- **Operating System**: Windows, macOS, or Linux

---

### Option A: Single-Command All-in-One Launcher (Recommended)
From the project root directory (`bank aplli`), run:
```bash
python run.py
```
**What this command does automatically:**
1. Seeds the SQLite database (`banksecure.db`) with target banking APIs, test cases, and initial baseline metrics.
2. Starts the **FastAPI Backend Server** at `http://localhost:8000`.
3. Starts the **Vite React Frontend Dashboard** at `http://localhost:3000`.
4. Opens your default web browser directly to the Security Dashboard.

---

### Option B: Windows Double-Click Launcher
Double-click [`start.bat`](file:///c:/Users/MUKILAN%20M/OneDrive/Desktop/bank%20aplli/start.bat) in the project root directory.

---

### Option C: Manual Multi-Terminal Execution

If you prefer to run and monitor the Backend and Frontend in separate terminal windows:

#### Terminal 1: Backend API Server
```bash
# Navigate to the backend directory
cd backend

# Install Python dependencies (first-time setup)
pip install -r requirements.txt

# Seed the database with initial banking test data
python -m app.seed

# Launch FastAPI with Uvicorn
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
*Backend API Swagger Documentation will be accessible at: [http://localhost:8000/docs](http://localhost:8000/docs)*

#### Terminal 2: Frontend React Dashboard
```bash
# Navigate to the frontend directory
cd frontend

# Install Node modules (first-time setup)
npm install

# Launch Vite development server
npm run dev
```
*Web Application UI will be accessible at: [http://localhost:3000](http://localhost:3000)*

---

### 🔧 Troubleshooting & Port Conflicts
- **Port 8000 occupied**: Stop any running Uvicorn or Python process using port 8000, or kill Python tasks in Task Manager.
- **Port 3000 occupied**: Vite will automatically fallback to 3001 if port 3000 is in use.
- **Missing Dependencies**: Ensure `pip install -r backend/requirements.txt` and `npm install` inside `frontend` have completed successfully.

---

## 💡 What This Application Does

**BankSecure API Guard** is an enterprise-grade security and automated testing platform tailored specifically for open banking and core financial REST APIs. It bridges the gap between **functional API testing** and **real-time cybersecurity monitoring**:

1. **Automated Vulnerability Scanning**: Executes multi-vector security tests (IDOR, Broken Auth, Rate-Limit Bypass, SQL Injection, Negative Amount Transfers, Payload Tampering).
2. **Interactive Vulnerability Sandbox**: Features a live banking sandbox with toggleable vulnerability switches to safely test, simulate, and demonstrate real-world cyber exploits in a controlled environment.
3. **Dynamic Risk Scoring (0–100)**: Quantifies the security health of the banking ecosystem in real-time based on test failure severity, CVSS scores, threat flag activity, and transaction anomalies.
4. **Behavioral Anomaly & Fraud Detection**: Establishes baseline request profiles and alerts security teams to rapid transaction velocity spikes, negative transfer attempts, or unauthorized access attempts.
5. **Incident Correlation & Threat Flagging**: Automatically groups related findings into active incident tickets for security analyst triage (`OPEN`, `INVESTIGATING`, `RESOLVED`).
6. **Executive PDF & Audit Reporting**: Generates downloadable PDF reports with executive summaries, CVSS score distributions, and complete remediation recommendations.

---

## 🏛️ System Architecture Flowchart

```
                    🏦 BANKING CLIENT / TESTER
                              │
                              ▼
                      ┌─────────────────┐
                      │    USER INPUT    │
                      │─────────────────│
                      │ API URL          │
                      │ HTTP Method      │
                      │ Headers          │
                      │ Authentication   │
                      │ Parameters       │
                      │ Request Payload  │
                      │ Expected Result  │
                      └────────┬────────┘
                               │
                               ▼
                      INPUT VALIDATION
                               │
                               ▼
                        API ANALYSIS
                               │
                               ▼
               ┌──────────────────────────────┐
               │     API TESTING FRAMEWORK    │
               │                              │
               │ 🔐 Authentication Testing    │
               │ 🛡 Authorization Testing     │
               │ ⚙ Functional Testing         │
               │ 🔒 Security Testing           │
               │ ❌ Negative Testing           │
               │ 🏦 Business Logic Testing     │
               │ 📦 Payload Validation         │
               │ 🚦 Rate-Limit Testing         │
               │ ⚡ Performance Testing        │
               │ 🔍 Response Validation        │
               └──────────────┬───────────────┘
                              │
                              ▼
                        🏦 BANKING API
                              │
                              ▼
                     DATABASE / SERVICES
                              │
                              ▼
                        API RESPONSE
                              │
                              ▼
                     RESPONSE VALIDATION
                              │
                              ▼
                       RESULT ANALYZER
                              │
                              ▼
                     🧠 RISK ENGINE
                              │
                              ▼
                      RISK SCORE 0–100
                              │
                              ▼
                   🧠 ANOMALY DETECTION
                              │
                              ▼
                   🚩 AUTOMATIC FLAGGING
                              │
                              ▼
                   🔍 INCIDENT CORRELATION
                              │
                              ▼
                      🚨 ALERT ENGINE
                              │
                              ▼
                  📊 SECURITY DASHBOARD
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
         Risk Monitor    API Security     Active Flags
              │           Posture              │
              ▼               ▼               ▼
         Risk Trend     Security Score     Investigation
              │               │               │
              └───────────────┼───────────────┘
                              │
                              ▼
                        👨💻 FIX / REMEDIATE
                              │
                              ▼
                     🔄 REGRESSION TEST
                              │
                     ┌────────┴────────┐
                     ▼                 ▼
                  PASSED             FAILED
                     │                 │
                     ▼                 ▼
               RISK REDUCED       FLAG REOPENED
                     │
                     ▼
               BEFORE vs AFTER
                     │
                     ▼
                 📄 REPORT
                     │
                     ▼
                📋 AUDIT LOG
```

---

## 🌟 Complete Feature Inventory

| Module | Features & Capabilities |
| --- | --- |
| **1. Security Command Center** | Dynamic Risk Score (0-100), Security Score dial gauge, Risk Trend graph, Risk Distribution pie chart, API health vector bars, active threat flags, anomaly feed. |
| **2. API Inventory** | Register, view, edit, and delete target banking endpoints (`/transfer`, `/balance`, `/payment`, `/beneficiary`, `/withdraw`, `/deposit`, `/admin/users`). |
| **3. Test Execution Center** | Multi-vector automated test suite runner, progress bar, real-time log terminal, plus **Custom User Input API Tester** allowing URL, headers, auth token, params, payload, and status code assertions. |
| **4. Mock Banking Sandbox** | Live switches to toggle intentional vulnerabilities (IDOR, Expired Token, Negative Transfer, Rate Limit Bypass, Header Removal) + live **Fund Transfer Simulator**. |
| **5. Vulnerabilities & Findings** | Repository of identified flaws, CVSS v3.1 scores, evidence log, and actionable remediation advice with status workflows (`OPEN`, `INVESTIGATING`, `RESOLVED`). |
| **6. Threat Flags** | Automatic incident correlation and analyst triage workflow. |
| **7. Risk & Anomaly Engine** | Behavioral baseline profiling, request velocity spike detection, and anomalous transaction pattern monitoring. |
| **8. Security Reports** | Executive ReportLab PDF document generator alongside CSV and JSON data exports. |
| **9. Structured Audit Trail** | Immutable JSON audit log tracking user actions, risk calculations, and test runs. |
| **10. CI/CD Security Gate** | Pre-configured GitHub Actions workflow (`.github/workflows/security-gate.yml`) to fail automated builds on critical security flaws. |

---

## 🛠️ Technology Stack

- **Backend Framework**: Python 3.12, FastAPI, Uvicorn
- **ORM & Database**: SQLAlchemy, SQLite (`banksecure.db`)
- **Data Validation & Auth**: Pydantic v2, PyJWT, Passlib / Bcrypt
- **Testing & HTTP Client**: HTTPX, Asyncio
- **PDF Generation**: ReportLab
- **Frontend Framework**: React 18, TypeScript, Vite
- **Styling & UI Components**: Tailwind CSS, Lucide React Icons
- **Data Visualization**: Recharts
- **HTTP & Routing**: Axios, React Router v6

---

## 🔗 Live Service Endpoints

- **Web Dashboard UI**: [http://localhost:3000](http://localhost:3000)
- **FastAPI Interactive Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
