"""
Main FastAPI Server for JobShield AI
Exposes verification endpoints for text messages, uploaded flyers, OSINT lookups,
and crowdsourced blacklist management. Also serves the frontend statically.
"""

import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional

from verifier import JobVerifierEngine
from vision_extractor import VisionExtractor
from osint_checker import OSINTChecker
from blacklist_db import blacklist_db

app = FastAPI(
    title="JobShield AI Enterprise Backend",
    description="Autonomous Multi-Layer Intelligence Engine for Local Job Scam Detection & Vacancy Verification",
    version="2.0.0"
)

# Enable CORS for browser frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Models
class VerifyTextRequest(BaseModel):
    text: str
    source_type: Optional[str] = "TEXT_MESSAGE"

class AuditDomainRequest(BaseModel):
    domain: str

class AuditEmailRequest(BaseModel):
    email: str
    company: Optional[str] = ""

class AuditAddressRequest(BaseModel):
    address: str

class ReportScamRequest(BaseModel):
    identifier: str
    scam_category: str
    demanded_amount: str
    reported_by: Optional[str] = "Student User"

# ==========================================
# REST API ROUTES
# ==========================================
@app.get("/api/health")
def health_check():
    return {
        "status": "online",
        "service": "JobShield AI Core",
        "modules_active": 6,
        "engine_version": "2.0.0",
        "cybercrime_portal_bridge": "https://cybercrime.gov.in/home"
    }

@app.post("/api/verify-text")
def verify_text(payload: VerifyTextRequest):
    """
    Module 2, 3, 4: Audits text payload for upfront fees, task scams, DNS age & email legitimacy.
    """
    if not payload.text or not payload.text.strip():
        raise HTTPException(status_code=400, detail="Text field cannot be empty.")
    return JobVerifierEngine.analyze(payload.text)

@app.post("/api/verify-image")
async def verify_image(file: UploadFile = File(...)):
    """
    Module 1: OCR ingestion from flyers/screenshots, followed by full security audit.
    """
    try:
        contents = await file.read()
        extracted_text = VisionExtractor.extract_from_image_bytes(contents, file.filename or "")
        analysis = JobVerifierEngine.analyze(extracted_text)
        analysis["raw_extracted_text"] = extracted_text
        analysis["filename"] = file.filename
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process image: {str(e)}")

@app.post("/api/audit-domain")
def audit_domain(payload: AuditDomainRequest):
    """
    Module 3: Live DNS and domain age audit.
    """
    if not payload.domain:
        raise HTTPException(status_code=400, detail="Domain cannot be empty.")
    return OSINTChecker.audit_domain_url(payload.domain)

@app.post("/api/audit-email")
def audit_email(payload: AuditEmailRequest):
    """
    Module 3: Free email spoofing and corporate HR integrity check.
    """
    if not payload.email:
        raise HTTPException(status_code=400, detail="Email cannot be empty.")
    return OSINTChecker.audit_email(payload.email, payload.company or "")

@app.post("/api/audit-address")
def audit_address(payload: AuditAddressRequest):
    """
    Module 3: Physical walk-in address and geo-verification.
    """
    if not payload.address:
        raise HTTPException(status_code=400, detail="Address cannot be empty.")
    return OSINTChecker.audit_physical_address(payload.address)

@app.get("/api/search-blacklist")
def search_blacklist(q: Optional[str] = ""):
    """
    Module 6: Search known scammer UPI IDs, phone numbers, or telegram handles.
    """
    return blacklist_db.search(q or "")

@app.post("/api/report-scam")
def report_scam(payload: ReportScamRequest):
    """
    Module 6: Crowdsource new scam reports to protect fellow students.
    """
    if not payload.identifier:
        raise HTTPException(status_code=400, detail="Identifier (phone, UPI, or handle) is required.")
    
    entry = blacklist_db.add_report(
        identifier=payload.identifier,
        scam_category=payload.scam_category,
        demanded_amount=payload.demanded_amount,
        reported_by=payload.reported_by or "Student User"
    )
    return {
        "message": "Report logged successfully into national registry.",
        "record": entry
    }

# ==========================================
# MOUNT FRONTEND STATIC ASSETS
# ==========================================
frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend")
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
