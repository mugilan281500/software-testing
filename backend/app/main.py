from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.seed import seed_database

# Import routers
from app.api.auth import router as auth_router
from app.api.apis import router as apis_router
from app.api.tests import router as tests_router
from app.api.findings import router as findings_router
from app.api.flags import router as flags_router
from app.api.dashboard import router as dashboard_router
from app.api.mock_bank import router as mock_bank_router
from app.api.reports import router as reports_router
from app.api.analytics import router as analytics_router
from app.api.transaction_monitoring import router as monitoring_router
from app.api.incidents import router as incidents_router
from app.api.rules import router as rules_router
from app.api.simulation_lab import router as simulation_router
from app.api.posture import router as posture_router

app = FastAPI(
    title="BankSecure API Guard",
    description="Intelligent API Security & Real-Time Suspicious Transaction Detection Framework for Banking Applications",
    version="2.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auto-initialize and seed DB on startup
@app.on_event("startup")
def startup_db():
    Base.metadata.create_all(bind=engine)
    seed_database()

# Include Routers
app.include_router(auth_router)
app.include_router(apis_router)
app.include_router(tests_router)
app.include_router(findings_router)
app.include_router(flags_router)
app.include_router(dashboard_router)
app.include_router(mock_bank_router)
app.include_router(reports_router)
app.include_router(analytics_router)
app.include_router(monitoring_router)
app.include_router(incidents_router)
app.include_router(rules_router)
app.include_router(simulation_router)
app.include_router(posture_router)

@app.get("/")
def root():
    return {
        "status": "ONLINE",
        "system": "BankSecure API Guard v2.0",
        "version": "2.0.0",
        "features": "Real-Time Transaction Security Monitoring & Multi-Factor Suspicious Activity Detection Engine",
        "docs": "/docs"
    }

