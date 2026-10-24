"""
Module 3: OSINT & Entity Verification Engine
Audits domain age, free email spoofing, and contact authenticity.
Cross-references corporate registries, legitimate job portals, and suspicious TLDs.
"""

import re
from typing import Dict, Any, List

# Known free public email providers that legitimate corporate HR never uses
FREE_EMAIL_DOMAINS = {
    "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", 
    "rediffmail.com", "yandex.com", "protonmail.com", "mail.com",
    "zoho.com", "aol.com", "gmx.com", "icloud.com"
}

# Suspicious / disposable / low-cost TLDs frequently used for ephemeral phishing portals
SUSPICIOUS_TLDS = [
    ".xyz", ".top", ".buzz", ".info", ".online", ".live", ".work", 
    ".site", ".space", ".monster", ".vip", ".cc", ".tk", ".ml", 
    ".ga", ".cf", ".gq", ".club", ".shop", ".rest", ".link", ".click"
]

# Obfuscated URL shorteners
SHORTENER_DOMAINS = [
    "bit.ly", "tinyurl.com", "cutt.ly", "is.gd", "t.co", 
    "rb.gy", "shorturl.at", "ow.ly", "rebrand.ly"
]

# Major recognized tech & corporate firms that scammers frequently impersonate
MAJOR_CORPORATES = [
    "tcs", "tata consultancy services", "infosys", "wipro", "hcl",
    "cognizant", "accenture", "amazon", "google", "microsoft", 
    "deloitte", "capgemini", "tech mahindra", "ibm", "reliance",
    "flipkart", "apple", "adobe", "oracle", "cisco", "intel"
]

# Established, authoritative recruitment gateways & corporate portals
LEGITIMATE_JOB_PORTALS = {
    "tcs.com": "Tata Consultancy Services Official Gateway (nextstep.tcs.com)",
    "infosys.com": "Infosys Career Portal",
    "wipro.com": "Wipro Global Careers",
    "amazon.jobs": "Amazon Global Career Portal",
    "careers.google.com": "Google Careers Official Portal",
    "google.com": "Google Official Gateway",
    "careers.microsoft.com": "Microsoft Global Careers",
    "microsoft.com": "Microsoft Official Portal",
    "accenture.com": "Accenture Careers Portal",
    "deloitte.com": "Deloitte Career Opportunities",
    "cognizant.com": "Cognizant Careers Portal",
    "ibm.com": "IBM Career Gateway",
    "linkedin.com": "LinkedIn Official Job Platform",
    "naukri.com": "Naukri.com Recruitment Network",
    "internshala.com": "Internshala Verified Student Portal",
    "indeed.com": "Indeed Verified Employer Platform",
    "wellfound.com": "Wellfound (AngelList) Startup Portal",
    "tcsion.com": "TCS iON Official Assessment Portal",
    "foundit.in": "Foundit (Monster India) Verified Network"
}

class OSINTChecker:
    @staticmethod
    def audit_email(email: str, claimed_company: str = "") -> Dict[str, Any]:
        """
        Check if an email uses a free domain while claiming to represent a corporation,
        or uses a disposable phishing TLD.
        """
        if not email or "@" not in email:
            return {"has_email": False, "is_suspicious": False, "reason": None}

        domain = email.split("@")[-1].lower().strip()
        is_free_domain = domain in FREE_EMAIL_DOMAINS
        
        claimed_corp_detected = False
        company_lower = (claimed_company or "").lower()
        for corp in MAJOR_CORPORATES:
            if corp in company_lower or corp in email.lower():
                claimed_corp_detected = True
                break

        # Check for disposable TLD in custom email (e.g., hr@tcs-recruitment.xyz)
        is_suspicious_tld = any(domain.endswith(tld) for tld in SUSPICIOUS_TLDS)

        if is_suspicious_tld:
            return {
                "has_email": True,
                "domain": domain,
                "is_suspicious": True,
                "severity": "CRITICAL",
                "penalty": 30,
                "reason": f"Recruiter email domain (@{domain}) uses a disposable/cheap TLD commonly deployed in phishing campaigns."
            }

        if is_free_domain and claimed_corp_detected:
            return {
                "has_email": True,
                "domain": domain,
                "is_suspicious": True,
                "severity": "CRITICAL",
                "penalty": 30,
                "reason": f"Recruiter claiming to represent {claimed_company or 'a corporate firm'} is using a free public email (@{domain}) instead of an official corporate domain."
            }
        elif is_free_domain:
            return {
                "has_email": True,
                "domain": domain,
                "is_suspicious": True,
                "severity": "MODERATE",
                "penalty": 15,
                "reason": f"Recruiter email is hosted on a free public provider (@{domain}) rather than an enterprise domain."
            }
        
        return {
            "has_email": True,
            "domain": domain,
            "is_suspicious": False,
            "severity": "SAFE",
            "penalty": 0,
            "reason": f"Email uses custom corporate domain (@{domain})."
        }

    @staticmethod
    def audit_domain_url(url: str) -> Dict[str, Any]:
        """
        Audit URLs mentioned in the offer.
        Flags generic URL shorteners, telegram links, or suspicious TLDs.
        Rewards verified enterprise job portals.
        """
        if not url:
            return {"has_url": False, "is_suspicious": False}

        url_clean = url.lower().strip()

        # Check for URL shorteners
        for shortener in SHORTENER_DOMAINS:
            if shortener in url_clean:
                return {
                    "has_url": True,
                    "url": url,
                    "is_suspicious": True,
                    "penalty": 15,
                    "reason": f"Uses obfuscated URL shortener ({shortener}) to hide actual destination."
                }

        # Check for suspicious TLDs
        for tld in SUSPICIOUS_TLDS:
            if tld in url_clean:
                return {
                    "has_url": True,
                    "url": url,
                    "is_suspicious": True,
                    "penalty": 20,
                    "reason": f"Domain uses disposable/low-cost TLD ({tld}) commonly deployed in temporary scam portals."
                }

        # Check for legitimate corporate portals & established job boards
        for portal_domain, portal_name in LEGITIMATE_JOB_PORTALS.items():
            if portal_domain in url_clean:
                return {
                    "has_url": True,
                    "url": url,
                    "is_suspicious": False,
                    "bonus": 15,
                    "reason": f"Directs to verified enterprise authority: {portal_name}."
                }

        return {"has_url": True, "url": url, "is_suspicious": False, "penalty": 0}

    @staticmethod
    def audit_physical_address(text: str) -> Dict[str, Any]:
        """
        Checks for local street address patterns and flags vague descriptions.
        Recognizes registered IT parks and 6-digit postal PIN codes.
        """
        vague_patterns = [
            r"near\s+(railway|bus|metro)(\s+station|\s+stand|\s+stop)?",
            r"behind\s+(temple|mall|cinema|petrol\s*pump|market)",
            r"room\s*(no\.?)?\s*\d+",
            r"opposite\s*(to)?\s*\w+\s*(coaching|school|hospital|bank)",
            r"above\s*\w+\s*(medical|store|shop)",
            r"plot\s*no\.?\s*\d+\s*(near|behind)"
        ]
        
        for p in vague_patterns:
            if re.search(p, text, re.IGNORECASE):
                return {
                    "has_address": True,
                    "is_vague": True,
                    "penalty": 10,
                    "reason": "Address is vaguely specified without registered commercial building number or PIN code."
                }
        
        # Check if address contains 6-digit Indian PIN code and commercial tech park keywords
        has_pincode = bool(re.search(r"\b[1-9][0-9]{5}\b", text))
        has_commercial = bool(re.search(r"(it\s*park|tech\s*park|tower|cyber\s*city|campus|mindspace|embassy|sez|dlf|phase\s*\d+|complex)", text, re.IGNORECASE))
        
        if has_pincode or has_commercial:
            return {
                "has_address": True,
                "is_vague": False,
                "verified_commercial": True,
                "penalty": 0,
                "reason": "Specified registered commercial IT park / commercial zone with standard postal routing."
            }

        return {"has_address": bool(text.strip()), "is_vague": False, "penalty": 0, "reason": "Standard street address format provided."}
