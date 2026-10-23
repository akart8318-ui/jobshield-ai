"""
Module 2 & 4: Heuristic Threat Engine, Dynamic Trust Scoring & Evidence Dossier Generator
Performs comprehensive multi-layered analysis on job postings, calculating 0-100% Trust Index.
"""

import re
from datetime import datetime
from typing import Dict, Any, List
from blacklist_db import blacklist_db
from osint_checker import OSINTChecker

class JobVerifierEngine:
    # Heuristic Patterns for Upfront Fee Extortion (Immediate Critical Penalty)
    FEE_PATTERNS = [
        r"(registration|entry|exam|interview|form)\s*(fee|charge|amount)",
        r"(security|caution|refundable)\s*(deposit|money|amount)",
        r"(laptop|kit|id\s*card|training|processing|courier)\s*(charge|fee|deposit|cost)",
        r"(pay|send|transfer|deposit)\s*(rs\.?|inr|₹)?\s*(\d{2,5})",
        r"(upi|gpay|phonepe|paytm)\s*(id|transfer|qr|payment)"
    ]

    # Unrealistic Compensation / Task Scams
    TASK_SCAM_PATTERNS = [
        r"(like|watch|subscribe)\s*(youtube|video|instagram|telegram|channels)",
        r"(earn|make)\s*(rs\.?|inr|₹)?\s*([2-9]\d{3,5})\s*(per|a|every)?\s*(day|daily|hour)",
        r"(data\s*entry|sms\s*sending|form\s*filling|captcha)\s*(without\s*typing|from\s*home|part\s*time)",
        r"(simple|easy)\s*(mobile|phone)\s*(work|task|job)",
        r"(rating|review)\s*(hotels|apps|products)"
    ]

    # Artificial Urgency & Coercion
    URGENCY_PATTERNS = [
        r"(only|just)\s*(\d+)\s*(seats|spots|vacancies)\s*left",
        r"(valid|expires|offer\s*ends)\s*(in|within)?\s*(\d+)?\s*(hours?|today|immediately)",
        r"immediate\s*(joining|selection|offer)\s*(without|no)\s*(interview|test)",
        r"100%\s*(guaranteed|job\s*placement|refund)"
    ]

    # Anonymous Contact Redirection
    ANONYMOUS_CHANNEL_PATTERNS = [
        r"(@[a-zA-Z0-9_]{4,32})",                # Telegram handle
        r"(t\.me\/[a-zA-Z0-9_]+)",                # Telegram invite link
        r"(chat\.whatsapp\.com\/[a-zA-Z0-9]+)",    # WhatsApp group invite
        r"wa\.me\/\d+"                            # WhatsApp direct click
    ]

    @classmethod
    def analyze(cls, text: str) -> Dict[str, Any]:
        """
        Executes end-to-end multi-layer audit on text payload.
        Returns Trust Score, Threat Classification, Red Flags, and Pre-filled Police Report.
        """
        text_clean = text.strip()
        if not text_clean:
            return {
                "error": "Empty text provided. Please enter job description or message."
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

        # 3. HEURISTIC RULE 1: UPFRONT FEE EXTORTION
        fee_detected = False
        fee_details = []
        for pattern in cls.FEE_PATTERNS:
            matches = re.findall(pattern, text_clean, re.IGNORECASE)
            if matches:
                fee_detected = True
                fee_details.append(pattern)

        if fee_detected:
            score -= 50
            flags.append({
                "type": "UPFRONT_FEE_EXTORTION",
                "severity": "CRITICAL",
                "title": "Upfront Monetary Demand Detected",
                "description": "Demands payment under the guise of registration, laptop security deposit, or interview kits. Legitimate employers NEVER charge applicants."
            })
        else:
            # Check for explicit Zero Fee disclaimers
            if re.search(r"no\s*(fee|charge)\s*is\s*charged", text_clean, re.IGNORECASE):
                score += 5
                passes.append({
                    "title": "Transparent Zero-Fee Policy",
                    "description": "Explicitly emphasizes that recruitment is 100% free of charge."
                })

        # 4. HEURISTIC RULE 2: TASK SCAMS & UNREALISTIC WAGES
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
                "description": "Promises high daily payouts (e.g. ₹2,000 - ₹5,000/day) for trivial activities like watching videos, rating hotels, or captcha typing."
            })

        # 5. HEURISTIC RULE 3: ARTIFICIAL URGENCY & SELECTION WITHOUT INTERVIEW
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
                "description": "Uses pressure tactics ('only 2 spots left', 'valid 1 hour', 'immediate joining without interview') to induce panic."
            })

        # 6. HEURISTIC RULE 4: ANONYMOUS ROUTING (Telegram / WhatsApp links)
        anonymous_channel_detected = False
        for pattern in cls.ANONYMOUS_CHANNEL_PATTERNS:
            m = re.search(pattern, text_clean, re.IGNORECASE)
            if m:
                anonymous_channel_detected = True
                break

        if anonymous_channel_detected:
            score -= 15
            flags.append({
                "type": "ANONYMOUS_ROUTING",
                "severity": "HIGH",
                "title": "Anonymous Messaging Redirection",
                "description": "Reroutes candidates to unofficial Telegram handles or WhatsApp links to evade enterprise tracking."
            })

        # 7. OSINT AUDIT: EMAIL & DOMAIN
        email_audit = OSINTChecker.audit_email(extracted_entities.get("email", ""), extracted_entities.get("company", ""))
        if email_audit.get("is_suspicious"):
            score -= email_audit.get("penalty", 20)
            flags.append({
                "type": "FREE_EMAIL_HR",
                "severity": email_audit.get("severity", "HIGH"),
                "title": "Suspicious Recruiter Email",
                "description": email_audit.get("reason")
            })
        elif email_audit.get("has_email"):
            passes.append({
                "title": "Corporate Domain Email",
                "description": email_audit.get("reason")
            })

        # 8. OSINT AUDIT: URL / DOMAIN
        url_audit = OSINTChecker.audit_domain_url(extracted_entities.get("url", ""))
        if url_audit.get("is_suspicious"):
            score -= url_audit.get("penalty", 15)
            flags.append({
                "type": "SUSPICIOUS_DOMAIN",
                "severity": "HIGH",
                "title": "Questionable Link/Domain",
                "description": url_audit.get("reason")
            })
        elif url_audit.get("bonus"):
            score += url_audit.get("bonus")
            passes.append({
                "title": "Official Portal Verified",
                "description": url_audit.get("reason")
            })

        # Clamp Score between 0 and 100
        score = max(5, min(100, score))
        risk_score = 100 - score

        # CLASSIFICATION
        if score >= 80:
            classification = "VERIFIED LEGITIMATE"
            status_color = "emerald"
            summary_verdict = "This vacancy demonstrates established recruitment indicators with zero monetary extortion triggers."
        elif score >= 50:
            classification = "SUSPICIOUS - PROCEED WITH CAUTION"
            status_color = "amber"
            summary_verdict = "Contains multiple questionable indicators. Do not transfer funds or share sensitive ID proofs."
        else:
            classification = "HIGH RISK SCAM"
            status_color = "rose"
            summary_verdict = "DANGER: High probability of financial cyber fraud. Demands upfront funds or matches known scam patterns."

        # GENERATE EVIDENCE DOSSIER FOR CYBERCRIME.GOV.IN
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
    def _extract_entities(cls, text: str) -> Dict[str, str]:
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

        # Email
        email_m = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
        if email_m:
            entities["email"] = email_m.group(0)

        # Phone
        phone_m = re.search(r"(\+?91[\-\s]?)?[6-9]\d{9}", text)
        if phone_m:
            entities["phone"] = phone_m.group(0)

        # UPI ID
        upi_m = re.search(r"[\w\.\-]+@(oksbi|okhdfcbank|okaxis|okicici|paytm|ybl|apl|upi)", text, re.IGNORECASE)
        if upi_m:
            entities["upi_id"] = upi_m.group(0)

        # Telegram
        tg_m = re.search(r"@[a-zA-Z0-9_]{4,32}", text)
        if tg_m:
            entities["telegram"] = tg_m.group(0)

        # URL
        url_m = re.search(r"https?:\/\/[^\s]+", text)
        if url_m:
            entities["url"] = url_m.group(0)

        # Extracted Amount
        amt_m = re.search(r"(?:rs\.?|inr|₹)\s*(\d{2,5})", text, re.IGNORECASE)
        if amt_m:
            entities["demanded_amount"] = f"₹{amt_m.group(1)}"

        # Company Heuristic
        for comp in ["TCS", "Tata Consultancy Services", "Infosys", "Wipro", "Amazon", "Cognizant", "HCL", "Accenture", "Google", "Microsoft"]:
            if comp.lower() in text.lower():
                entities["company"] = comp
                break

        return entities

    @classmethod
    def _generate_evidence_dossier(cls, raw_text: str, entities: Dict, classification: str, risk_score: int, flags: List[Dict]) -> str:
        """Format an official pre-filled complaint for cybercrime.gov.in and Helpline 1930."""
        timestamp = datetime.now().strftime("%d-%b-%Y, %H:%M IST")
        flag_lines = "\n".join([f"- {f['title']}: {f['description']}" for f in flags]) or "None"

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
\"\"\"{raw_text[:500]}\"\"\"

=====================================================
CITIZEN NOTICE:
If funds have been transferred, immediately call Helpline 1930 
to request a financial freeze with your bank, and submit 
this dossier at https://cybercrime.gov.in/home.
====================================================="""
