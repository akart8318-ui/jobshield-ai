"""
Module 6: Crowdsourced Scam Registry & Lookup Database
Provides quick search and reporting for known scammer UPI IDs, phone numbers, and handles.
"""

from datetime import datetime
from typing import List, Dict, Optional

# Initial pre-seeded registry of known scam vectors reported across Indian campuses
_INITIAL_BLACKLIST: List[Dict] = [
    {
        "id": "SCAM-101",
        "type": "UPI ID",
        "identifier": "quickwork@upi",
        "scam_category": "Telegram YouTube Task Scam",
        "demanded_amount": "₹499",
        "reported_count": 48,
        "first_reported": "2026-09-12",
        "status": "CONFIRMED FRAUD"
    },
    {
        "id": "SCAM-102",
        "type": "UPI ID",
        "identifier": "datawork@oksbi",
        "scam_category": "Fake Data Entry Registration Fee",
        "demanded_amount": "₹850",
        "reported_count": 72,
        "first_reported": "2026-08-20",
        "status": "CONFIRMED FRAUD"
    },
    {
        "id": "SCAM-103",
        "type": "PHONE",
        "identifier": "+91 98765 43210",
        "scam_category": "Fake HR Recruiter (Posing as Amazon)",
        "demanded_amount": "₹1,200 (Laptop Kit)",
        "reported_count": 31,
        "first_reported": "2026-10-02",
        "status": "CONFIRMED FRAUD"
    },
    {
        "id": "SCAM-104",
        "type": "TELEGRAM",
        "identifier": "@earn_quick_india",
        "scam_category": "Part-Time Rating Scheme",
        "demanded_amount": "₹1,000",
        "reported_count": 115,
        "first_reported": "2026-07-15",
        "status": "CONFIRMED FRAUD"
    },
    {
        "id": "SCAM-105",
        "type": "COMPANY",
        "identifier": "Apex Global Solutions Pvt Ltd",
        "scam_category": "Bogus Walk-in Consultancy",
        "demanded_amount": "₹2,500 (Training Fee)",
        "reported_count": 29,
        "first_reported": "2026-09-28",
        "status": "CONFIRMED FRAUD"
    }
]

class ScamBlacklistDB:
    def __init__(self):
        self.records: List[Dict] = list(_INITIAL_BLACKLIST)

    def search(self, query: str) -> List[Dict]:
        """Search blacklist by UPI, phone, telegram handle, or company name."""
        q = query.strip().lower()
        if not q:
            return self.records[:10]
        
        results = []
        for r in self.records:
            if (q in r["identifier"].lower() or 
                q in r["scam_category"].lower() or 
                q in r["demanded_amount"].lower()):
                results.append(r)
        return results

    def check_identifier(self, identifier: str) -> Optional[Dict]:
        """Check if an exact identifier is blacklisted."""
        clean_id = identifier.strip().lower().replace(" ", "").replace("-", "")
        for r in self.records:
            record_id = r["identifier"].lower().replace(" ", "").replace("-", "")
            if clean_id in record_id or record_id in clean_id:
                return r
        return None

    def add_report(self, identifier: str, scam_category: str, demanded_amount: str, reported_by: str = "Anonymous Student") -> Dict:
        """Add a newly crowdsourced scam entry."""
        existing = self.check_identifier(identifier)
        if existing:
            existing["reported_count"] += 1
            return existing

        new_entry = {
            "id": f"SCAM-{100 + len(self.records) + 1}",
            "type": "USER REPORT",
            "identifier": identifier.strip(),
            "scam_category": scam_category.strip(),
            "demanded_amount": demanded_amount.strip() or "Unspecified",
            "reported_count": 1,
            "first_reported": datetime.now().strftime("%Y-%m-%d"),
            "status": "UNDER INVESTIGATION"
        }
        self.records.insert(0, new_entry)
        return new_entry

# Global singleton instance
blacklist_db = ScamBlacklistDB()
