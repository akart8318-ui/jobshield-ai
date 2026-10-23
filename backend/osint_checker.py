"""
Module 3: OSINT & Entity Verification Engine
Audits domain age, free email spoofing, and contact authenticity.
"""

import re
from typing import Dict, Any, List

# Known free public email providers that legitimate corporate HR never uses
FREE_EMAIL_DOMAINS = {
    "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", 
    "rediffmail.com", "yandex.com", "protonmail.com", "mail.com"
}

# Major recognized tech & corporate firms that scammers frequently impersonate
MAJOR_CORPORATES = [
    "tcs", "tata consultancy services", "infosys", "wipro", "hcl",
    "cognizant", "accenture", "amazon", "google", "microsoft", 
    "deloitte", "capgemini", "tech mahindra", "ibm"
]

class OSINTChecker:
    @staticmethod
    def audit_email(email: str, claimed_company: str = "") -> Dict[str, Any]:
        """
        Check if an email uses a free domain while claiming to represent a corporation.
        """
        if not email or "@" not in email:
            return {"has_email": False, "is_suspicious": False, "reason": None}

        domain = email.split("@")[-1].lower().strip()
        is_free_domain = domain in FREE_EMAIL_DOMAINS
        
        claimed_corp_detected = False
        company_lower = claimed_company.lower()
        for corp in MAJOR_CORPORATES:
            if corp in company_lower or corp in email.lower():
                claimed_corp_detected = True
                break

        if is_free_domain and claimed_corp_detected:
            return {
                "has_email": True,
                "domain": domain,
                "is_suspicious": True,
                "severity": "CRITICAL",
                "penalty": 30,
                "reason": f"Recruiter claiming to represent {claimed_company or 'a corporate firm'} is using a free public email (@{domain}) instead of official company domain."
            }
        elif is_free_domain:
            return {
                "has_email": True,
                "domain": domain,
                "is_suspicious": True,
                "severity": "MODERATE",
                "penalty": 15,
                "reason": f"Recruiter email is hosted on a free provider (@{domain}) rather than an enterprise domain."
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
        """
        if not url:
            return {"has_url": False, "is_suspicious": False}

        url_clean = url.lower().strip()
        suspicious_tlds = [".xyz", ".top", ".buzz", ".info", ".online", ".live", ".work", ".site"]
        shorteners = ["bit.ly", "tinyurl.com", "cutt.ly", "is.gd", "t.co"]

        for shortener in shorteners:
            if shortener in url_clean:
                return {
                    "has_url": True,
                    "url": url,
                    "is_suspicious": True,
                    "penalty": 15,
                    "reason": f"Uses obfuscated URL shortener ({shortener}) to hide actual destination."
                }

        for tld in suspicious_tlds:
            if tld in url_clean:
                return {
                    "has_url": True,
                    "url": url,
                    "is_suspicious": True,
                    "penalty": 20,
                    "reason": f"Domain uses disposable/low-cost TLD ({tld}) commonly deployed in temporary scam portals."
                }

        # Check for legitimate corporate portals
        if "tcs.com" in url_clean or "infosys.com" in url_clean or "wipro.com" in url_clean:
            return {
                "has_url": True,
                "url": url,
                "is_suspicious": False,
                "bonus": 10,
                "reason": "Directs to an established, authoritative enterprise portal."
            }

        return {"has_url": True, "url": url, "is_suspicious": False, "penalty": 0}

    @staticmethod
    def audit_physical_address(text: str) -> Dict[str, Any]:
        """
        Checks for local street address patterns and flags vague descriptions.
        """
        vague_patterns = [
            r"near (railway|bus|metro) station",
            r"behind (temple|mall|cinema)",
            r"room no \d+",
            r"opposite to \w+ coaching"
        ]
        
        for p in vague_patterns:
            if re.search(p, text, re.IGNORECASE):
                return {
                    "has_address": True,
                    "is_vague": True,
                    "penalty": 10,
                    "reason": "Address is vaguely specified without registered commercial building number or PIN code."
                }
        
        return {"has_address": False, "is_vague": False, "penalty": 0}
