# 🎓 BankSecure API Guard — Complete Presentation & Explanation Guide

This guide is designed to help you **understand, explain, and demonstrate** the **BankSecure API Guard** project to professors, evaluators, interviewers, or technical team members.

---

## 📌 1. The 30-Second Elevator Pitch

> *"BankSecure API Guard is an intelligent security and functional testing platform built for modern banking and financial APIs. It combines automated vulnerability scanning, real-time behavioral anomaly detection, dynamic risk scoring (0-100), and an interactive sandbox environment to identify security flaws before they can be exploited by hackers in live banking systems."*

---

## 🎯 2. What Problem Does This Project Solve?

Modern banks expose thousands of REST API endpoints for online banking, mobile apps, and third-party fintech integrations (Open Banking). However:
1. **Traditional functional tools (like Postman or Swagger UI)** test if APIs work when inputs are correct, but fail to detect authorization bugs, race conditions, or fraud logic.
2. **Traditional Security Scanners** are generic and don't understand banking business logic (e.g., transferring `-$500` to gain funds, or accessing another customer's account via IDOR).
3. **Security Analysts** are overwhelmed by disconnected alerts without a unified risk score or automated incident correlation.

**BankSecure API Guard solves this by providing a unified platform tailored specifically to banking logic and security posture.**

---

## 🔬 3. Key Security Techniques & Algorithms Used

### 🛡️ A. Multi-Vector Security & Functional Testing Engine
The testing engine sends controlled malicious payloads to API endpoints to verify resilience against OWASP API Security Top 10 vulnerabilities:
- **BOLA / IDOR (Broken Object Level Authorization)**: Tries accessing account balance or transfers using User A's token with User B's Account ID.
- **BFLA (Broken Function Level Authorization)**: Attempts standard user tokens on administrative endpoints like `/admin/users`.
- **Business Logic Flaws**: Sends negative transfer amounts (`-$100`), extreme values, or malformed transaction payloads to detect balance corruption.
- **Broken Authentication**: Uses expired JWT tokens, missing Authorization headers, or weak signatures.
- **Rate-Limiting & Velocity Bypass**: Fires rapid bursts of requests to verify HTTP 429 Too Many Requests enforcement.

### 🧠 B. Dynamic Risk Engine (Score 0–100)
Rather than simple pass/fail metrics, the system calculates a real-time **Security Risk Score (0-100)**:
$$\text{Risk Score} = \min\left(100, \sum \text{Severity Weights} + \text{Anomaly Multiplier} + \text{Active Flag Penalties}\right)$$
- **0–25 (Low Risk / Green)**: System is secure, high test pass rate.
- **26–60 (Medium Risk / Yellow)**: Warnings, minor authorization flaws detected.
- **61–100 (Critical Risk / Red)**: Critical vulnerabilities present (IDOR, auth bypass, active fraud anomalies).

### 📈 C. Behavioral Baseline & Anomaly Detection Engine
- **Rolling Baseline Window**: Records historical averages of request frequency, transaction amounts, and IP/User-Agent patterns.
- **Velocity Spike Detection**: Flags sudden surges in transfer attempts or balance inquiries.
- **Fraud Monitoring**: Identifies anomalous transactions (e.g. transfers exceeding 3x customer average or rapid multi-account balance checks).

### 🧪 D. Vulnerability Simulation & Sandbox
The project includes a **Live Mock Banking Sandbox** with interactive switches:
- Enables toggling vulnerabilities (IDOR, Expired Token, Negative Transfer, Rate Limit Bypass) on demand.
- Allows real-time demonstration: toggle a flaw, run tests or simulator, observe the Risk Score spike, and see Threat Flags trigger instantly.

### 🚩 E. Automated Incident Correlation Engine
- Converts raw test failures and anomaly triggers into structured **Threat Flags** with assigned CVSS v3.1 scores.
- Enables analyst triage workflows (`OPEN` ➔ `INVESTIGATING` ➔ `RESOLVED`) with immutable audit logging.

---

## 🏗️ 4. Technology Stack & Architecture

- **Backend (Python 3.12 / FastAPI)**: Asynchronous REST API server providing high-speed endpoint handling, Pydantic validation, and SQLAlchemy ORM.
- **Frontend (React 18 + TypeScript + Vite)**: Modern dashboard with dark mode UI, smooth CSS transitions, dynamic charts (Recharts), and responsive state management.
- **Database (SQLite + SQLAlchemy)**: Lightweight embedded relational database tracking endpoints, test cases, findings, threat flags, and transaction histories.
- **Report Generation (ReportLab)**: Generates executive-ready PDF security reports with CVSS score breakdowns and remediation guidance.

---

## 🎬 5. Step-by-Step Live Demonstration Guide

Follow these steps during a presentation to impress your audience:

### Step 1: Show the Security Command Center (Dashboard)
- Open `http://localhost:3000`.
- Highlight the **Dynamic Risk Score Dial Gauge**, **Security Posture Score**, **Risk Trend Graph**, and **Active Threat Flags**.

### Step 2: Navigate to the Mock Banking Sandbox
- Go to the **Sandbox Page**.
- Show the live **Fund Transfer Simulator**.
- Toggle an intentional vulnerability switch (e.g., **IDOR Vulnerability** or **Negative Transfer Vulnerability**).

### Step 3: Run the Test Execution Suite
- Navigate to **Test Suite / Execution Center**.
- Click **Run All Security & Functional Tests**.
- Watch the live test logs scroll in real-time as tests fail on the toggled vulnerabilities.

### Step 4: Show the Incident Triage & Threat Flags
- Return to **Threat Flags & Incidents**.
- Point out how the system correlated the test failures into an actionable ticket with CVSS scores and remediation steps.
- Click **Resolve** after toggling the flaw off in the sandbox to demonstrate regression testing and risk score reduction!

### Step 5: Export Executive Security Report
- Navigate to **Reports**.
- Click **Generate PDF Report** to download the professional executive summary.

---

## ❓ 6. Common Questions & Answers for Viva / Interviews

**Q1: Why did you choose FastAPI over Flask or Django?**
> *Answer*: FastAPI provides asynchronous I/O capabilities (`async/await`) essential for high-velocity API testing and request simulation, automatic OpenAPI documentation, and built-in Pydantic data validation.

**Q2: How does the system handle authorization testing without real bank credentials?**
> *Answer*: It utilizes JWT (JSON Web Tokens) with custom scopes and mock account IDs to simulate multi-tenant authorization policies safely in a controlled environment.

**Q3: What makes this different from generic vulnerability scanners like OWASP ZAP?**
> *Answer*: Generic scanners don't understand domain-specific banking logic, such as negative balance transfers or banking velocity limits. BankSecure API Guard incorporates financial business logic rules into its testing matrix.
