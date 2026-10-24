"""
Vercel Serverless Entry Point for JobShield AI
Routes all /api/* requests to the FastAPI app via Mangum (ASGI adapter).
Vercel discovers this file and wraps it as a serverless function.
"""

import sys
import os

# Add the project root to path so 'backend' package is importable
root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, os.path.abspath(root))

from backend.app import app
from mangum import Mangum

# Vercel's Python runtime looks for a callable named 'handler'
handler = Mangum(app, lifespan="off")
