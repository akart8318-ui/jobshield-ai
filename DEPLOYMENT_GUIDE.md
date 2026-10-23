# JobShield AI — Deployment Guide

This guide provides **two simple ways** to deploy and share JobShield AI live:

---

## ⚡ Method 1: Instant 30-Second Public HTTPS URL (Best for Live Hackathon Stage Demo)
*Gives you a public link (e.g., `https://friendly-tiger-42.loca.lt`) in 30 seconds that judges can open on their mobile phones right in the room—zero cloud setup required.*

1. **Step 1:** Double-click [`start_backend.bat`](start_backend.bat) to launch the FastAPI server locally on port 8000.
2. **Step 2:** Double-click [`start_public_tunnel.bat`](start_public_tunnel.bat).
3. **Step 3:** The terminal will display your live public URL:
   ```text
   your url is: https://funny-otter-82.loca.lt
   ```
4. Share that link with judges or project it on stage!

---

## ☁️ Method 2: Free Permanent Cloud Deployment on Render.com (via GitHub)
*Gives you a permanent URL like `https://jobshield-ai.onrender.com` that stays live 24/7.*

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit for JobShield AI"
   git branch -M main
   git remote add origin https://github.com/<your-username>/jobshield-ai.git
   git push -u origin main
   ```

2. **Deploy on Render (100% Free):**
   - Go to [**render.com**](https://render.com) and sign in with GitHub.
   - Click **New +** ➔ **Web Service**.
   - Connect your `jobshield-ai` repository.
   - Settings are automatically detected from `render.yaml`:
     - **Environment:** `Python 3`
     - **Build Command:** `pip install -r backend/requirements.txt`
     - **Start Command:** `uvicorn app:app --app-dir backend --host 0.0.0.0 --port $PORT`
   - Click **Deploy Web Service**.
   - In 2 minutes, your website is live worldwide!

---

## 🐳 Method 3: Docker Deployment
If deploying on AWS, DigitalOcean, or Azure:
```bash
docker build -t jobshield-ai .
docker run -p 8000:8000 jobshield-ai
```
Visit `http://localhost:8000`.
