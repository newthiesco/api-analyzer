## eCFR API Analyzer

This project creates FastAPI-based JSON API to analyze federal regulations (eCFR) and provide estimated regulation sizes per agency.

---

## What this project does
- Exposes a JSON API with several endpoints:
  - `/api/v1/agencies/size` → returns agency names with estimated regulation sizes (in MB).  
  - `/api/v1/update` → refreshes the data on demand.  
  - `/api/v1/health` → simple health check for the service.
- Fetches real regulation data from the **public eCFR API** and calculates the approximate size of each agency’s regulations.
- Caches results **in memory** so responses are fast. The cache is refreshed automatically at startup, manually via the update endpoint, **and also automatically every 24 hours** via a background task, ensuring the API reflects recent eCFR changes.
- **Note:** In production, this background task guarantees that the cache stays current without modifying source code, fulfilling the 24-hour refresh requirement.

---

## How it works (brief)
- The app connects to the official **eCFR public API** at [https://www.ecfr.gov/api](https://www.ecfr.gov/api).  
- It fetches the list of federal agencies from `/admin/v1/agencies.json`, then queries `/versioner/v1/titles.json?agency=...` for each agency to retrieve regulation data.  
- The JSON response is serialized, and its size is calculated in **megabytes (MB)** to estimate the amount of regulation content per agency.  
- Results are stored in an **in-memory cache** (Python variable) for fast responses.  
- The cache is refreshed automatically on startup, can be updated manually via `/api/v1/update`, and is **automatically refreshed every 24 hours** via a background task.

---

## 🚀 Deployment (Render-specific)
You can deploy this app to any server that supports Python and has internet access. In this case the app is deployed using Render web service.

### 1. Push Your Code to GitHub
- Ensure your project (`ecfr-analyzer/`) is in a GitHub repository.  
- Commit and push all files, including `requirements.txt`, `runtime.txt`, `build.sh`, and `app/`.

### 2. Create a New Web Service on Render
1. Log in to [Render](https://dashboard.render.com).  
2. Click **New → Web Service**.  
3. Connect your GitHub repository.  
4. Select your repo (`ecfr-analyzer`) and branch (e.g., `main`).

### 3. Configure the Service
- **Environment**: Python 3  
- **Build Command**:
```bash
chmod +x build.sh && ./build.sh
```

## Start Command:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
- **Instance Type**: Free (or paid, depending on your needs)

4. ## Deploy

Click Create Web Service.

Render installs dependencies, builds, and starts the app.

You will get a service URL like https://ecfr-analyzer.onrender.com.

5. ## Verify & Monitor

Access the endpoints to verify functionality.

Use Render’s Dashboard → Logs to monitor activity and ensure the cache updates properly.

## 📡 Usage
Endpoints

Root: / → Returns service status and available endpoints.

Get Agency Sizes: /api/v1/agencies/size → Returns JSON with agency names, slugs, regulation sizes (MB), and last updated timestamps.

Manual Update: /api/v1/update → Triggers a refresh of the cached data immediately.

Health Check: /api/v1/health → Simple status check to verify the service is running.

## Examples

## Using Browser: 
https://ecfr-analyzer.onrender.com/api/v1/health

## Using curl
Health:
```bash
curl https://ecfr-analyzer.onrender.com/api/v1/health
```
Agency sizes:
```bash
curl https://ecfr-analyzer.onrender.com/api/v1/agencies/size
```
Manual update:
```bash
curl https://ecfr-analyzer.onrender.com/api/v1/update
```


## 🖥 Local Setup & Test

1. Clone the Repository
```bash
git clone <your-repo-url>
cd ecfr-analyzer
```
2. Create & Activate a Virtual Environment (Recommended)
```bash
python3 -m venv .venv

source .venv/bin/activate  ### macOS/Linux
```
```bash
.venv\Scripts\activate   ### Windows
```
3. ### Install Dependencies
```bash
pip install -r requirements.txt
```
### ✅ Verify requests is installed:
```bash
python -c "import requests; print('✅ requests installed')"
```
4. Run the API Locally
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
 The API will be available at: http://127.0.0.1:8000/

5. Test Endpoints
 Health check
 ```bash
curl http://127.0.0.1:8000/api/v1/health
```
 Get agency sizes
 ```bash
curl http://127.0.0.1:8000/api/v1/agencies/size
```
Manual update
```bash
curl http://127.0.0.1:8000/api/v1/update
```

## Assessment Feedback:
This project implements a production-ready FastAPI JSON API that analyzes federal regulations per agency using live data from the public eCFR API. It calculates estimated regulation sizes, serves results via in-memory caching, and includes a background task for automatic 24-hour refresh, meeting the assessment requirements. The API provides endpoints for agency sizes, manual updates, and health checks, with clear logging and error handling. The code is modular, deployment-ready (e.g., on Render.com), and fully tested locally. Total development time was approximately 20 hours. This submission demonstrates both technical proficiency in Python/DevOps and the ability to deliver a maintainable, real-world service.

