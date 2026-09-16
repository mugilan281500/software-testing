import os
import json
import csv
import datetime
from sqlalchemy.orm import Session
from app.models import TestRun, TestResult, Finding, ThreatFlag, SecurityReport, MockTransaction, SecurityIncident, SecurityAlert, AuditLog, ApiTarget

REPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "generated_reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

class ReportService:
    @staticmethod
    def generate_report(db: Session, title: str, report_format: str = "PDF", created_by: str = "ADMIN") -> SecurityReport:
        report_code = f"REP-{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        latest_run = db.query(TestRun).order_by(TestRun.id.desc()).first()
        
        overall_risk = latest_run.overall_risk_score if latest_run else 25.0
        sec_score = latest_run.security_score if latest_run else 75.0
        
        file_name = f"{report_code}.{report_format.lower()}"
        file_path = os.path.join(REPORTS_DIR, file_name)

        if report_format.upper() == "JSON":
            ReportService._generate_json(db, file_path, title, latest_run)
        elif report_format.upper() == "CSV":
            ReportService._generate_csv(db, file_path, latest_run)
        elif report_format.upper() == "HTML":
            ReportService._generate_html(db, file_path, title, latest_run)
        else:
            ReportService._generate_pdf(db, file_path, title, latest_run)

        report = SecurityReport(
            report_code=report_code,
            title=title,
            format=report_format.upper(),
            file_name=file_name,
            file_path=file_path,
            risk_score=overall_risk,
            security_score=sec_score,
            created_by=created_by
        )
        db.add(report)
        db.commit()
        db.refresh(report)
        return report

    @staticmethod
    def _generate_html(db: Session, file_path: str, title: str, latest_run: TestRun):
        findings = db.query(Finding).all()
        incidents = db.query(SecurityIncident).all()
        txs = db.query(MockTransaction).all()
        alerts = db.query(SecurityAlert).all()
        apis = db.query(ApiTarget).all()

        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>BankSecure Audit Report - {title}</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #0f172a; color: #f8fafc; padding: 30px; }}
        h1 {{ color: #38bdf8; border-bottom: 2px solid #334155; padding-bottom: 10px; }}
        .metric-card {{ background: #1e293b; padding: 20px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #334155; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
        th, td {{ padding: 12px; border: 1px solid #334155; text-align: left; }}
        th {{ background: #334155; color: #38bdf8; }}
        tr:nth-child(even) {{ background: #1e293b; }}
        .badge-critical {{ background: #ef4444; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold; }}
        .badge-high {{ background: #f97316; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold; }}
        .badge-medium {{ background: #eab308; color: black; padding: 4px 8px; border-radius: 4px; font-weight: bold; }}
        .badge-low {{ background: #22c55e; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold; }}
    </style>
</head>
<body>
    <h1>🏦 BankSecure API Guard — Comprehensive Security Report</h1>
    <p><b>Report Title:</b> {title} | <b>Generated:</b> {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
    
    <div class="metric-card">
        <h2>Executive Summary</h2>
        <p><b>Overall Security Score:</b> {latest_run.security_score if latest_run else 85.0} / 100</p>
        <p><b>Overall Risk Index:</b> {latest_run.overall_risk_score if latest_run else 15.0} / 100</p>
        <p><b>Total APIs Inventory:</b> {len(apis)} endpoints monitored</p>
        <p><b>Total Transactions Monitored:</b> {len(txs)} manual & synthetic transactions</p>
        <p><b>Security Incidents Correlated:</b> {len(incidents)} consolidated incidents</p>
    </div>

    <div class="metric-card">
        <h2>Security Findings Summary</h2>
        <table>
            <tr><th>Code</th><th>Title</th><th>Category</th><th>Severity</th><th>Risk Score</th><th>Status</th><th>Endpoint</th></tr>
            {"".join(f"<tr><td>{f.finding_code}</td><td>{f.title}</td><td>{f.category}</td><td><span class='badge-{f.severity.lower()}'>{f.severity}</span></td><td>{f.risk_score}</td><td>{f.status}</td><td>{f.api_endpoint}</td></tr>" for f in findings)}
        </table>
    </div>

    <div class="metric-card">
        <h2>Transaction Monitoring Live Log</h2>
        <table>
            <tr><th>Transaction ID</th><th>Sender</th><th>Receiver</th><th>Amount</th><th>Risk</th><th>Level</th><th>Decision</th></tr>
            {"".join(f"<tr><td>{tx.transaction_id}</td><td>{tx.sender_account}</td><td>{tx.receiver_account}</td><td>₹{tx.amount:,.2f}</td><td>{tx.risk_score}</td><td><span class='badge-{tx.risk_level.lower()}'>{tx.risk_level}</span></td><td>{tx.decision}</td></tr>" for tx in txs[:10])}
        </table>
    </div>
</body>
</html>
"""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)

    @staticmethod
    def _generate_json(db: Session, file_path: str, title: str, latest_run: TestRun):
        findings = db.query(Finding).all()
        flags = db.query(ThreatFlag).all()
        incidents = db.query(SecurityIncident).all()
        data = {
            "title": title,
            "generated_at": datetime.datetime.utcnow().isoformat(),
            "latest_run": {
                "run_number": latest_run.run_number if latest_run else "N/A",
                "overall_risk_score": latest_run.overall_risk_score if latest_run else 0,
                "security_score": latest_run.security_score if latest_run else 100,
                "total_tests": latest_run.total_tests if latest_run else 0,
                "passed": latest_run.passed if latest_run else 0,
                "failed": latest_run.failed if latest_run else 0,
            },
            "incidents_count": len(incidents),
            "findings_count": len(findings),
            "findings": [
                {
                    "code": f.finding_code,
                    "title": f.title,
                    "category": f.category,
                    "severity": f.severity,
                    "status": f.status,
                    "endpoint": f.api_endpoint,
                    "risk_score": f.risk_score,
                    "recommendation": f.recommendation
                } for f in findings
            ],
            "flags_count": len(flags),
            "flags": [
                {
                    "code": flg.flag_code,
                    "title": flg.title,
                    "endpoint": flg.api_endpoint,
                    "severity": flg.severity,
                    "status": flg.status,
                    "risk_score": flg.risk_score
                } for flg in flags
            ]
        }
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def _generate_csv(db: Session, file_path: str, latest_run: TestRun):
        findings = db.query(Finding).all()
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Finding Code", "Title", "Category", "Severity", "Risk Score", "Status", "Endpoint", "Recommendation"])
            for f_item in findings:
                writer.writerow([
                    f_item.finding_code,
                    f_item.title,
                    f_item.category,
                    f_item.severity,
                    f_item.risk_score,
                    f_item.status,
                    f_item.api_endpoint,
                    f_item.recommendation
                ])

    @staticmethod
    def _generate_pdf(db: Session, file_path: str, title: str, latest_run: TestRun):
        findings = db.query(Finding).all()
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib import colors

            doc = SimpleDocTemplate(file_path, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []

            title_style = ParagraphStyle(
                'DocTitle',
                parent=styles['Heading1'],
                fontSize=20,
                textColor=colors.HexColor('#0F172A'),
                spaceAfter=12
            )
            story.append(Paragraph(f"BANKSECURE SECURITY REPORT: {title}", title_style))
            story.append(Paragraph(f"Generated: {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}", styles['Normal']))
            story.append(Spacer(1, 12))

            risk_val = latest_run.overall_risk_score if latest_run else 0.0
            sec_val = latest_run.security_score if latest_run else 100.0
            summary_text = f"<b>Overall Security Score:</b> {sec_val}/100 &nbsp;&nbsp;|&nbsp;&nbsp; <b>Risk Index:</b> {risk_val}/100"
            story.append(Paragraph(summary_text, styles['Heading2']))
            story.append(Spacer(1, 12))

            table_data = [["Finding ID", "Category", "Severity", "Endpoint", "Risk"]]
            for f in findings[:10]:
                table_data.append([f.finding_code, f.category, f.severity, f.api_endpoint, str(f.risk_score)])

            t = Table(table_data)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E293B')),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0,0), (-1,0), 6),
                ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#F8FAFC')),
                ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
            ]))
            story.append(t)
            doc.build(story)
        except Exception:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"=== BANKSECURE SECURITY REPORT: {title} ===\n")
                f.write(f"Generated: {datetime.datetime.utcnow()}\n")
                f.write(f"Overall Security Score: {latest_run.security_score if latest_run else 100}/100\n")
                f.write(f"Overall Risk Score: {latest_run.overall_risk_score if latest_run else 0}/100\n\n")
                f.write("FINDINGS:\n")
                for f in findings:
                    f.write(f"- [{f.severity}] {f.finding_code} ({f.category}): {f.title} on {f.api_endpoint}\n")

