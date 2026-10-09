# 🏦 BankSecure API Guard — Intelligent Banking Security Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Frontend-React%2018%20%7C%20TypeScript-61DAFB.svg?logo=react&logoColor=black)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Bundler-Vite-646CFF.svg?logo=vite&logoColor=white)](https://vitejs.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Styling-Tailwind%20CSS-38B2AC.svg?logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57.svg?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Enterprise-grade API Security & Functional Testing Framework with Real-Time Risk Monitoring, Behavioral Anomaly Detection, Interactive Sandbox, and Automated Threat Flagging for Banking & Financial Services.**

---

## 📑 Table of Contents

- [Overview](#-overview)
- [System Architecture](#️-system-architecture)
- [Core Features & Capabilities](#-core-features--capabilities)
- [Project Structure](#-project-structure)
- [Quick Start Guide](#-quick-start-guide)
  - [Prerequisites](#prerequisites)
  - [Method 1: One-Command All-in-One Launcher (Recommended)](#method-1-one-command-all-in-one-launcher-recommended)
  - [Method 2: Windows Batch Launcher](#method-2-windows-batch-launcher)
  - [Method 3: Manual Execution (Two Terminals)](#method-3-manual-execution-two-terminals)
- [Security Testing Vectors](#-security-testing-vectors)
- [Dashboard & Modules](#-dashboard--modules)
- [Live Endpoints & Swagger API Docs](#-live-endpoints--swagger-api-docs)
- [License & Authors](#-license--authors)

---

## 💡 Overview

**BankSecure API Guard** is an end-to-end automated testing and cyber posture monitoring platform engineered specifically for Open Banking and Core Financial REST APIs.

Modern banking applications handle high-frequency, mission-critical transactions that are targeted by malicious actors using Broken Object Level Authorization (BOLA/IDOR), token expiration bypasses, and transaction velocity fraud. **BankSecure API Guard** bridges the critical gap between functional QA testing and real-time security operations center (SOC) monitoring.

### Key Highlights
- 🛡️ **Automated Vulnerability Scanner**: Executes multi-vector penetration test cases against live banking endpoints.
- 🧪 **Interactive Mock Banking Sandbox**: Toggleable vulnerability switches to simulate real-world exploits in an isolated environment.
- 📊 **Dynamic Risk Engine (0–100)**: Calculates posture scores based on test failure severity, CVSS scores, threat flag activity, and transaction anomalies.
- 🚩 **Incident Correlation & Threat Flagging**: Automatically groups security findings into actionable incident tickets (`OPEN`, `INVESTIGATING`, `RESOLVED`).
- 📄 **Executive Audit & PDF Reporting**: Instant generation of audit logs, CSV exports, and downloadable PDF security reports.

---

## 🏛️ System Architecture

```text
                    🏦 BANKING CLIENT / TEST ENGINEER
                               │
                               ▼
                       ┌─────────────────┐
                       │    USER INPUT    │
                       │─────────────────│
                       │ Target API URL  │
                       │ HTTP Method     │
                       │ Headers & Auth  │
                       │ Request Payload │
                       │ Assertions      │
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

## 🌟 Core Features & Capabilities

| Module | Features & Capabilities |
| :--- | :--- |
| **1. Security Command Center** | Real-time Risk Score dial (0–100), Security Posture Score, historical risk trend graph, risk severity distribution charts, API health vector bars, active threat flags, and live anomaly feed. |
| **2. Target API Inventory** | Register, inspect, edit, and organize target banking endpoints (`/transfer`, `/balance`, `/payment`, `/beneficiary`, `/withdraw`, `/deposit`, `/admin/users`). |
| **3. Test Execution Center** | Automated runner across 10 distinct testing vectors with live logging, progress tracking, and custom interactive API request builder. |
| **4. Mock Banking Sandbox** | Live switches to toggle intentional vulnerabilities (IDOR, Expired Token, Negative Transfer, Rate Limit Bypass, Header Tampering) + real-time Fund Transfer Simulator. |
| **5. Vulnerabilities & Findings** | Granular vulnerability records with CVSS v3.1 scoring, HTTP request/response evidence, and step-by-step remediation guidance. |
| **6. Threat Flags & Incidents** | Automatic incident correlation and lifecycle triage workflow (`OPEN`, `INVESTIGATING`, `RESOLVED`). |
| **7. Risk & Anomaly Engine** | Baseline behavioral profiling, velocity spike detection, and anomalous transaction pattern recognition. |
| **8. Executive Reports** | ReportLab PDF generator compiling executive summaries, CVSS distribution charts, finding logs, and CSV/JSON data exports. |
| **9. Structured Audit Trail** | Immutable log tracking every user action, test execution, risk calculation, and triage decision. |

---

## 📁 Project Structure

```text
bank-appli/
├── backend/
│   ├── app/
│   │   ├── api/                  # API routers (endpoints, test cases, findings, reports)
│   │   ├── services/             # Core business logic (risk engine, scanner, anomalies)
│   │   ├── auth_utils.py         # JWT and password hashing utilities
│   │   ├── database.py           # SQLAlchemy database session setup
│   │   ├── models.py             # Database models (Endpoints, Tests, Findings, Logs)
│   │   ├── schemas.py            # Pydantic v2 validation schemas
│   │   ├── seed.py               # Pre-configured banking test data seeder
│   │   └── main.py               # FastAPI application entry point
│   ├── banksecure.db             # SQLite local database
│   └── requirements.txt          # Python backend dependencies
├── frontend/
│   ├── src/
│   │   ├── components/           # Reusable UI components (Sidebar, Navbar, Metrics)
│   │   ├── pages/                # Dashboard views (Dashboard, Sandbox, Execution, etc.)
│   │   ├── services/             # Axios API client integrations
│   │   ├── App.tsx               # Main application routing
│   │   └── main.tsx              # React DOM initialization
│   ├── index.html                # Vite HTML template
│   ├── package.json              # Frontend dependencies and scripts
│   ├── tailwind.config.js        # Tailwind CSS styling configuration
│   └── vite.config.ts            # Vite build configuration
├── run.py                        # Single-command unified backend + frontend runner
├── start.bat                     # Windows batch script launcher
├── PROJECT_EXPLANATION.md        # Comprehensive technical architecture documentation
├── .gitignore                    # Git exclusions
└── README.md                     # Project documentation
```

---

## 🚀 Quick Start Guide

### Prerequisites
- **Python**: 3.10 or higher (Python 3.12 recommended)
- **Node.js**: v18 or higher & `npm`
- **Git**

---

### Method 1: One-Command All-in-One Launcher (Recommended)

From the project root directory, run:

```bash
python run.py
```

**What this script does automatically:**
1. Validates and initializes the SQLite database with default banking data.
2. Starts the **FastAPI Backend Server** on `http://localhost:8000`.
3. Starts the **Vite React Frontend** on `http://localhost:3000`.
4. Automatically opens your default web browser to the dashboard.

---

### Method 2: Windows Batch Launcher

Double-click the [`start.bat`](start.bat) file located in the root directory.

---

### Method 3: Manual Execution (Two Terminals)

If you prefer to run the Backend and Frontend independently in separate terminals:

#### Terminal 1 — Backend (FastAPI)
```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Seed the database with initial banking test endpoints and mock data
python -m app.seed

# Start the development server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
*Backend Swagger Docs will be available at: [http://localhost:8000/docs](http://localhost:8000/docs)*

#### Terminal 2 — Frontend (React + Vite)
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the Vite development server
npm run dev
```
*Frontend application UI will be available at: [http://localhost:3000](http://localhost:3000)*

---

## 🔍 Security Testing Vectors

BankSecure API Guard runs specialized test cases across the following security categories:

1. **Broken Object Level Authorization (BOLA / IDOR)**: Validates that unauthorized users cannot view or manipulate other users' accounts or transactions.
2. **Broken User Authentication**: Tests for missing, expired, malformed, or weak JWT tokens and session headers.
3. **Broken Object Property Level Authorization**: Detects mass assignment and parameter tampering in transfer payloads.
4. **Unrestricted Resource Consumption**: Tests rate-limiting controls and resource exhaustion resistance under burst traffic.
5. **Broken Function Level Authorization (BFLA)**: Validates that standard customer accounts cannot access administrative endpoints (`/admin/*`).
6. **Negative & Edge-Case Testing**: Submits negative transaction amounts, zero values, extreme bounds, and inverted currency exchanges.
7. **SQL / NoSQL Injection**: Injects test payloads into query parameters and JSON fields to verify parameterized querying.
8. **Server-Side Request Forgery (SSRF) & Webhook Tampering**: Tests callback URLs and external redirect parameters.
9. **Security Misconfiguration**: Flags permissive CORS configurations, verbose error stack traces, and unencrypted transport.
10. **Data Validation & Type Confusion**: Enforces strict schema validation for missing required fields and improper types.

---

## 🖥️ Dashboard & Modules

- **Dashboard**: High-level overview of overall risk, open flags, and test pass/fail ratios.
- **API Inventory**: Catalog of banking endpoints with risk ratings and methods.
- **Test Execution**: Interactive test runner with real-time logs and custom parameter tester.
- **Mock Bank Sandbox**: Live interactive sandbox to enable/disable security flaws and simulate transfers.
- **Security Findings**: Triage list of discovered vulnerabilities with remediation steps.
- **Incident Management**: Incident grouping and team assignment.
- **Reports**: Generate executive PDF reports, CSV data dumps, and JSON logs.
- **Audit Logs**: Immutable timeline of all system and tester actions.

---

## 🔗 Live Endpoints & Swagger API Docs

When running locally:
- 🌐 **Web Dashboard UI**: [http://localhost:3000](http://localhost:3000)
- 📖 **FastAPI Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- 📑 **FastAPI ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 📄 License & Authors

This project is licensed under the MIT License. Developed for automated API security assessment and educational testing.
