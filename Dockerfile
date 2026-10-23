# ==============================================================================
# JobShield AI - Production Container
# ==============================================================================
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies and install
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r ./backend/requirements.txt

# Copy backend and frontend source files
COPY backend ./backend
COPY frontend ./frontend
COPY assets ./assets

ENV PORT=8000
EXPOSE 8000

# Launch FastAPI app with static frontend mounting
CMD ["uvicorn", "app:app", "--app-dir", "backend", "--host", "0.0.0.0", "--port", "8000"]
