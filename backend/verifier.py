"""
Module 2 & 4: Heuristic Threat Engine, Dynamic Trust Scoring & Evidence Dossier Generator
Performs comprehensive multi-layered analysis on job postings, calculating a 0-100% Trust Index.
Detects modern employment fraud vectors: monetary extortion, remote desktop trojans, 
crypto/USDT Ponzi tasks, fake review tasks, coercive legal intimidation, and spoofed recruiter identities.
"""

import re
from datetime import datetime
from typing import Dict, Any, List
try:
    from blacklist_db import blacklist_db
    from osint_checker import OSINTChecker, MAJOR_CORPORATES
except ImportError:
    from backend.blacklist_db import blacklist_db
    from backend.osint_checker import OSINTChecker, MAJOR_CORPORATES

class JobVerifierEngine:
    # 1. Heuristic Patterns for Upfront Fee Extortion (Immediate Critical Penalty)
    FEE_PATTERNS = [
        r"(registration|entry|exam|interview|form|application)\s*(fee|charge|cost|amount)",
        r"(security|caution|refundable|mandatory)\s*(deposit|money|amount|fee)",
        r"(laptop|kit|id\s*card|training|processing|courier|uniform|dispatch|documentation)\s*(charge|fee|deposit|cost|amount)",
        r"(pay|send|transfer|deposit)\s*(?:rs\.?|inr|₹)?\s*(\d{2,5})",
        r"(upi|gpay|phonepe|paytm)\s*(?:id|transfer|qr|payment|handle)"
    ]

    # 2. Critical Financial Credential Harvesting (Severe Penalty)
    CREDENTIAL_THEFT_PATTERNS = [
        r"(otp|one\s*time\s*password|atm\s*pin|cvv|bank\s*password|netbanking|mpin)",
        r"(blank\s*cheque|cancelled\s*cheque\s*with\s*signature)",
        r"(debit|credit)\s*card\s*(number|photo|front\s*and\s*back)"
    ]

    # 3. Remote Desktop Trojan & Device Compromise Tools
    REMOTE_TROJAN_PATTERNS = [
        r"\b(anydesk|teamviewer|rustdesk|quicksupport|ultraviewer|zoho\s*assist)\b",
        r"\b(screen\s*share|share\s*screen|remote\s*access)\s*(app|code|permission)",
        r"\b(\.apk|download\s*our\s*app|install\s*apk)\b"
    ]

    # 4. Crypto / USDT / Prepaid Task Ponzi Schemes
    CRYPTO_PONZI_PATTERNS = [
        r"\b(usdt|crypto|tron|trx|bitcoin|binance|okx|trust\s*wallet)\b",
        r"(prepaid\s*task|recharge\s*task|merchant\s*order|deposit\s*to\s*unlock)",
        r"(earn\s*commission\s*on\s*(?:recharge|investment|crypto))"
    ]

    # 5. Unrealistic Compensation & Task Scams
    TASK_SCAM_PATTERNS = [
        r"(like|watch|subscribe)\s*(youtube|video|instagram|telegram|channels?)",
        r"(google\s*maps?|hotel|tripadvisor|restaurant|movie|app)\s*(review|rating|5\s*star|rate)",
        r"(earn|make)\s*(?:rs\.?|inr|₹)?\s*([2-9]\d{3,5})\s*(?:per|a|every)?\s*(day|daily|hour)",
        r"(data\s*entry|sms\s*sending|form\s*filling|captcha)\s*(without\s*typing|from\s*home|part\s*time|simple)",
        r"(simple|easy)\s*(mobile|phone)\s*(work|task|job)\s*(for\s*students)?"
    ]

    # 6. Artificial Urgency & Coercive Legal Threats
    URGENCY_PATTERNS = [
        r"(only|just)\s*(\d+)\s*(seats?|spots?|vacancies?)\s*left",
        r"(valid|expires|offer\s*ends)\s*(in|within)?\s*(\d+)?\s*(hours?|today|immediately)",
        r"immediate\s*(joining|selection|offer)\s*(without|no)\s*(interview|test|exam)",
        r"100%\s*(guaranteed|job\s*placement|refund)"
    ]

    # 7. Fake Legal Intimidation (common in fake typing / data entry frauds)
    LEGAL_THREAT_PATTERNS = [
        r"(legal\s*notice|court\s*case|police\s*complaint|fir\s*will\s*be\s*lodged|advocate)",
        r"(breach\s*of\s*contract|agreement\s*violation|pay\s*penalty|recover\s*damages)"
    ]

    # 8. Anonymous Contact Redirection
    ANONYMOUS_CHANNEL_PATTERNS = [
        r"(@[a-zA-Z0-9_]{4,32})",                # Telegram handle
        r"(t\.me\/[a-zA-Z0-9_]+)",                # Telegram invite link
        r"(chat\.whatsapp\.com\/[a-zA-Z0-9]+)",    # WhatsApp group invite
        r"(wa\.me\/\d+)"                          # WhatsApp direct click
    ]

    @classmethod
    def analyze(cls, text: str) -> Dict[str, Any]:
        """
        Executes end-to-end multi-layer audit on text payload.
        Returns Trust Score, Threat Classification, Red Flags, Positive Passes, and Evidence Dossier.
        """
        text_clean = (text or "").strip()
        if not text_clean:
            return {
                "error": "Empty text provided. Please enter job description or message.",
                "trust_score": 0,
                "classification": "INVALID_INPUT"
            }

        score = 100
        flags: List[Dict[str, str]] = []
        passes: List[Dict[str, str]] = []

        # 1. EXTRACT ENTITIES
        extracted_entities = cls._extract_entities(text_clean)

        # 2. CHECK CROWDSOURCED BLACKLIST
        matched_blacklist = None
        for candidate in [extracted_entities.get("phone"), extracted_entities.get("upi_id"), extracted_entities.get("telegram")]:
            if candidate:
                matched_blacklist = blacklist_db.check_identifier(candidate)
                if matched_blacklist:
                    break

        if matched_blacklist:
            score = 5  # Immediate collapse
            flags.append({
                "type": "BLACKLIST_MATCH",
                "severity": "CRITICAL",
                "title": f"Known Fraud Identifier ({matched_blacklist['identifier']})",
                "description": f"Flagged in national student blacklist {matched_blacklist['reported_count']} times for: {matched_blacklist['scam_category']}."
            })

        # 3. RULE: CRITICAL FINANCIAL CREDENTIAL HARVESTING
        cred_theft_detected = False
        for pattern in cls.CREDENTIAL_THEFT_PATTERNS:
            if re.search(pattern, text_clean, re.IGNORECASE):
                cred_theft_detected = True
                break

        if cred_theft_detected:
            score -= 55
            flags.append({
                "type": "CREDENTIAL_HARVESTING",
                "severity": "CRITICAL",
                "title": "Demanding Sensitive Banking Credentials",
                "description": "Requests bank OTP, ATM PIN, CVV, or blank cheques. Legitimate employers strictly transfer salaries via NEFT/IMPS and never solicit authentication credentials."
            })

        # 4. RULE: REMOTE DESKTOP TROJAN / DEVICE HIJACK
        trojan_detected = False
        for pattern in cls.REMOTE_TROJAN_PATTERNS:
            if re.search(pattern, text_clean, re.IGNORECASE):
                trojan_detected = True
                break

        if trojan_detected:
            score -= 55
            flags.append({
                "type": "REMOTE_ACCESS_TROJAN",
                "severity": "CRITICAL",
                "title": "Remote Desktop / APK Hijacking Vector",
                "description": "Directs applicant to install screen sharing tools (AnyDesk, TeamViewer) or unverified APK files, enabling cybercriminals to take over devices and drain bank accounts."
            })

        # 5. RULE: CRYPTO / PREPAID TASK PONZI SCAM
        crypto_detected = False
        for pattern in cls.CRYPTO_PONZI_PATTERNS:
            if re.search(pattern, text_clean, re.IGNORECASE):
                crypto_detected = True
                break

        if crypto_detected:
            score -= 55
            flags.append({
                "type": "CRYPTO_PONZI_TASK",
                "severity": "CRITICAL",
                "title": "Cryptocurrency / Prepaid Task Ponzi Trap",
                "description": "Requires cryptocurrency deposits (USDT/TRX) or prepaid recharge tasks to unlock payouts. This is a classic multi-tiered Ponzi fraud."
            })

        # 6. RULE: UPFRONT FEE EXTORTION
        fee_detected = False
        for pattern in cls.FEE_PATTERNS:
            if re.search(pattern, text_clean, re.IGNORECASE):
                fee_detected = True
                break

        if fee_detected:
            score -= 50
            flags.append({
                "type": "UPFRONT_FEE_EXTORTION",
                "severity": "CRITICAL",
                "title": "Upfront Monetary Demand Detected",
                "description": "Demands payment under the guise of registration, laptop security deposit, training kit, or courier charges. Legitimate employers NEVER charge applicants."
            })
        else:
            # Positive: Transparent Zero-Fee Policy
            if re.search(r"no\s*(fee|charge|money)\s*is\s*charged|free\s*of\s*charge|never\s*ask\s*for\s*money|zero\s*fee", text_clean, re.IGNORECASE):
                score += 5
                passes.append({
                    "title": "Transparent Zero-Fee Policy",
                    "description": "Explicitly emphasizes that recruitment is 100% free of charge."
                })

        # 7. RULE: TASK SCAMS & UNREALISTIC WAGES
        task_detected = False
        for pattern in cls.TASK_SCAM_PATTERNS:
            if re.search(pattern, text_clean, re.IGNORECASE):
                task_detected = True
                break

        if task_detected:
            score -= 25
            flags.append({
                "type": "TASK_SCAM_PROFILE",
                "severity": "HIGH",
                "title": "Unrealistic Wage / Social Media Task Scam",
                "description": "Promises high daily payouts (e.g. ₹2,000 - ₹5,000/day) for trivial tasks like watching YouTube videos, rating Google Maps, or captcha typing."
            })

        # 8. RULE: FAKE LEGAL INTIMIDATION
        legal_threat_detected = False
        for pattern in cls.LEGAL_THREAT_PATTERNS:
            if re.search(pattern, text_clean, re.IGNORECASE):
                legal_threat_detected = True
                break

        if legal_threat_detected:
            score -= 30
            flags.append({
                "type": "LEGAL_INTIMIDATION",
                "severity": "HIGH",
                "title": "Coercive Legal Threat / Fake FIR Extortion",
                "description": "Uses fabricated court notices or police FIR threats to intimidate students into paying bogus penalty charges for uncompleted data entry tasks."
            })

        # 9. RULE: ARTIFICIAL URGENCY & SELECTION WITHOUT INTERVIEW
        urgency_detected = False
        for pattern in cls.URGENCY_PATTERNS:
            if re.search(pattern, text_clean, re.IGNORECASE):
                urgency_detected = True
                break

        if urgency_detected:
            score -= 15
            flags.append({
                "type": "COERCION_URGENCY",
                "severity": "MODERATE",
                "title": "Artificial Urgency & Coercive Pressure",
                "description": "Uses high-pressure tactics ('only 2 spots left', 'offer expires in 1 hour', 'immediate joining without interview') to provoke hasty decisions."
            })

        # 10. RULE: ANONYMOUS ROUTING (Telegram / WhatsApp links)
        anonymous_channel_detected = False
        for pattern in cls.ANONYMOUS_CHANNEL_PATTERNS:
            if re.search(pattern, text_clean, re.IGNORECASE):
                anonymous_channel_detected = True
                break

        if anonymous_channel_detected:
            score -= 15
            flags.append({
                "type": "ANONYMOUS_ROUTING",
                "severity": "HIGH",
                "title": "Anonymous Messaging Redirection",
                "description": "Reroutes candidates to unofficial Telegram handles or WhatsApp groups to evade corporate auditing."
            })

        # 11. OSINT AUDIT: EMAIL INTEGRITY
        email_val = extracted_entities.get("email")
        if email_val:
            email_audit = OSINTChecker.audit_email(email_val, extracted_entities.get("company", ""))
            if email_audit.get("is_suspicious"):
                score -= email_audit.get("penalty", 20)
                flags.append({
                    "type": "FREE_EMAIL_HR",
                    "severity": email_audit.get("severity", "HIGH"),
                    "title": "Suspicious Recruiter Email Domain",
                    "description": email_audit.get("reason")
                })
            else:
                score += 5
                passes.append({
                    "title": "Enterprise Corporate Email Verified",
                    "description": email_audit.get("reason")
                })

        # 12. OSINT AUDIT: URL & DOMAIN INTEGRITY
        url_val = extracted_entities.get("url")
        if url_val:
            url_audit = OSINTChecker.audit_domain_url(url_val)
            if url_audit.get("is_suspicious"):
                score -= url_audit.get("penalty", 15)
                flags.append({
                    "type": "SUSPICIOUS_DOMAIN",
                    "severity": "HIGH",
                    "title": "Questionable Link / Phishing Domain",
                    "description": url_audit.get("reason")
                })
            elif url_audit.get("bonus"):
                score += url_audit.get("bonus", 15)
                passes.append({
                    "title": "Authoritative Employment Gateway Verified",
                    "description": url_audit.get("reason")
                })

        # 13. RECOGNIZE AUTHENTIC ENTERPRISE PROCESSES
        if extracted_entities.get("company") and extracted_entities["company"] != "Not Specified":
            if not fee_detected and not task_detected and not cred_theft_detected and not trojan_detected:
                passes.append({
                    "title": f"Known Enterprise Entity: {extracted_entities['company']}",
                    "description": "Matches verified corporate employer directory with standard recruitment verbiage."
                })

        # Clamp Score between 5 and 100
        score = max(5, min(100, score))
        risk_score = 100 - score

        # CLASSIFICATION & VERDICTS
        if score >= 80:
            classification = "VERIFIED LEGITIMATE"
            status_color = "emerald"
            summary_verdict = "This vacancy demonstrates established recruitment standards with zero monetary extortion triggers."
        elif score >= 50:
            classification = "SUSPICIOUS - PROCEED WITH CAUTION"
            status_color = "amber"
            summary_verdict = "Contains questionable indicators. Do not transfer any funds or disclose private identity documents."
        else:
            classification = "HIGH RISK SCAM"
            status_color = "rose"
            summary_verdict = "DANGER: High probability of financial cyber fraud. Demands upfront funds, sensitive credentials, or matches known scam patterns."

        # GENERATE EVIDENCE DOSSIER FOR CYBERCRIME.GOV.IN & 1930
        police_dossier = cls._generate_evidence_dossier(
            text_clean, extracted_entities, classification, risk_score, flags
        )

        return {
            "trust_score": score,
            "risk_score": risk_score,
            "classification": classification,
            "status_color": status_color,
            "summary_verdict": summary_verdict,
            "extracted_entities": extracted_entities,
            "flags": flags,
            "passes": passes,
            "police_dossier": police_dossier,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    @classmethod
    def _extract_entities(cls, text: str) -> Dict[str, Any]:
        """Extract contact, financial, and organizational metadata."""
        entities = {
            "company": "Not Specified",
            "phone": None,
            "email": None,
            "upi_id": None,
            "telegram": None,
            "url": None,
            "demanded_amount": None
        }

        # 1. Email extraction
        email_m = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
        if email_m:
            entities["email"] = email_m.group(0)

        # 2. Indian Phone extraction
        phone_m = re.search(r"(?:\+?91[\-\s]?)?[6-9]\d{4}[\-\s]?\d{5}", text)
        if phone_m:
            entities["phone"] = phone_m.group(0).strip()

        # 3. UPI ID extraction (standard banking handles)
        upi_pattern = r"[a-zA-Z0-9.\-_]+@(?:oksbi|okhdfcbank|okaxis|okicici|paytm|ybl|apl|upi|axl|ibl|barodampay|kotak|sbi|icici|hdfcbank|federal|idfcbank|freecharge)"
        upi_m = re.search(upi_pattern, text, re.IGNORECASE)
        if upi_m:
            entities["upi_id"] = upi_m.group(0)
        else:
            # Check for upi: handle format
            upi_m2 = re.search(r"(?:upi|gpay|phonepe|paytm)\s*[:=\-]?\s*([a-zA-Z0-9.\-_]+@[a-zA-Z0-9.\-_]+)", text, re.IGNORECASE)
            if upi_m2:
                entities["upi_id"] = upi_m2.group(1)

        # 4. Telegram handle / link
        tg_m = re.search(r"@[a-zA-Z0-9_]{4,32}|t\.me\/[a-zA-Z0-9_]+", text)
        if tg_m:
            entities["telegram"] = tg_m.group(0)

        # 5. URL extraction
        url_m = re.search(r"https?:\/\/[^\s]+", text)
        if url_m:
            entities["url"] = url_m.group(0)

        # 6. Extracted Demanded Amount
        amt_m = re.search(r"(?:rs\.?|inr|₹)\s*(\d{2,5})", text, re.IGNORECASE)
        if amt_m:
            entities["demanded_amount"] = f"₹{amt_m.group(1)}"

        # 7. Company Identification
        for comp in [
            "Tata Consultancy Services", "TCS", "Infosys", "Wipro", "Amazon", 
            "Cognizant", "HCL", "Accenture", "Google", "Microsoft", "Deloitte", 
            "IBM", "Capgemini", "Tech Mahindra", "Reliance", "Flipkart", "Apple"
        ]:
            if comp.lower() in text.lower():
                entities["company"] = comp
                break

        return entities

    @classmethod
    def _generate_evidence_dossier(cls, raw_text: str, entities: Dict, classification: str, risk_score: int, flags: List[Dict]) -> str:
        """Format an official pre-filled complaint for cybercrime.gov.in and Helpline 1930."""
        timestamp = datetime.now().strftime("%d-%b-%Y, %H:%M IST")
        flag_lines = "\n".join([f"- [{f.get('severity', 'FLAG')}] {f['title']}: {f['description']}" for f in flags]) or "None detected"

        return f"""=====================================================
NATIONAL CYBER CRIME REPORTING PORTAL (cybercrime.gov.in)
INCIDENT COMPLAINT DOSSIER • GENERATED BY JOBSHIELD AI
=====================================================
Date & Time of Audit: {timestamp}
Incident Category: Online Employment / Job Offer Cyber Fraud
Threat Assessment: {classification} ({risk_score}% Risk Score)

1. SUSPECT IDENTIFIERS DETECTED:
- Phone / Contact: {entities.get('phone') or 'Not provided in text'}
- Payment / UPI ID: {entities.get('upi_id') or 'Not provided in text'}
- Telegram Handle: {entities.get('telegram') or 'Not provided in text'}
- Contact Email: {entities.get('email') or 'Not provided in text'}
- Suspect Website / URL: {entities.get('url') or 'Not provided in text'}
- Claimed Company: {entities.get('company')}
- Extortion Amount Demanded: {entities.get('demanded_amount') or 'None detected'}

2. EVIDENCE OF FRAUDULENT ACTIVITY:
{flag_lines}

3. RAW TEXT RECEIVED BY VICTIM:
\"\"\"{raw_text[:600]}\"\"\"

=====================================================
CITIZEN EMERGENCY NOTICE:
If funds have been transferred, immediately call Helpline 1930 
to request an emergency financial freeze with your bank, and submit 
this dossier at https://cybercrime.gov.in/home.
====================================================="""
