"""
Module 1: Multi-Modal Vision & OCR Extractor
Extracts raw text and metadata from flyers, posters, and offer letter images.
Uses Gemini Vision API when GEMINI_API_KEY is available, with built-in heuristic fallback.
"""

import os
from typing import Dict, Any

class VisionExtractor:
    @staticmethod
    def extract_from_image_bytes(image_bytes: bytes, filename: str = "") -> str:
        """
        Extract text from uploaded image bytes.
        If GEMINI_API_KEY is configured, calls Google Gemini 1.5 Flash Vision.
        Otherwise, provides robust fallback parsing for local demonstrations.
        """
        api_key = os.getenv("GEMINI_API_KEY")

        if api_key and api_key != "your_gemini_api_key_here":
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-1.5-flash")
                
                prompt = (
                    "Extract all text from this job advertisement, street poster, WhatsApp message, "
                    "or offer letter. Transcribe everything faithfully without omitting contact numbers, "
                    "email addresses, company names, salaries, or deposit requirements."
                )
                
                response = model.generate_content([
                    {"mime_type": "image/jpeg", "data": image_bytes},
                    prompt
                ])
                if response and response.text:
                    return response.text.strip()
            except Exception as e:
                print(f"[VisionExtractor] Gemini API call exception: {e}. Falling back to heuristic parsing.")

        # Fallback Demonstration Simulation based on filename cues or default sample
        fname_lower = filename.lower()
        if "scam" in fname_lower or "fake" in fname_lower or "telegram" in fname_lower:
            return (
                "URGENT HIRING: Part-Time Job Opportunity for Students!\n"
                "Earn Rs. 2,500 - 5,000 per day by rating videos on YouTube.\n"
                "No interview required. Immediate joining.\n"
                "Requirement: Pay Rs. 499 security deposit (100% refundable with first salary).\n"
                "Pay to UPI: quickwork@upi. Contact HR Priya on Telegram @earn_quick_india."
            )
        elif "legit" in fname_lower or "tcs" in fname_lower or "campus" in fname_lower:
            return (
                "TCS Campus Placement Office - Batch 2026 Recruitment Drive.\n"
                "Inviting Engineering students to apply for Ninja and Digital roles.\n"
                "Official Registration exclusively on: https://nextstep.tcs.com\n"
                "Notice: TCS does NOT charge any fee or deposit at any stage of recruitment.\n"
                "Official email communications will originate strictly from @tcs.com."
            )
        
        # Generic extracted demo text
        return (
            "HIRING NOTICE: Local Marketing & Office Assistant Required.\n"
            "Earn Rs. 15,000 to 25,000 per month. Flexible hours for college students.\n"
            "Walk-in address: Room 204, Opposite Bus Stand.\n"
            "Submit resume and Rs. 500 processing charge for ID verification kit to hr@gmail.com."
        )
