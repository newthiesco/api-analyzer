import os
import json
import requests
import asyncio
import logging
from typing import List, Dict, Any
from fastapi import FastAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="eCFR Analyzer API")

# In-memory cache
agency_cache: List[Dict[str, Any]] = None

class ECFRClient:
    def __init__(self):
        self.base_url = "https://www.ecfr.gov/api"

    def get_agencies(self) -> List[Dict[str, Any]]:
        """Fetch list of agencies from eCFR"""
        try:
            resp = requests.get(f"{self.base_url}/admin/v1/agencies.json", timeout=30)
            resp.raise_for_status()
            return resp.json().get("agencies", [])
        except Exception as e:
            logger.error(f"Error fetching agencies: {e}")
            return []

    def get_titles_for_agency(self, slug: str) -> Dict:
        """Fetch regulation titles for a given agency slug"""
        try:
            resp = requests.get(
                f"{self.base_url}/versioner/v1/titles.json",
                params={"agency": slug},
                timeout=30
            )
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            logger.error(f"Error fetching titles for {slug}: {e}")
        return {}

    def calculate_size(self, data: Dict) -> float:
        """Calculate data size in MB"""
        if not data:
            return 0.0
        json_string = json.dumps(data)
        size_bytes = len(json_string.encode("utf-8"))
        return round(size_bytes / (1024 * 1024), 2)

async def analyze_regulations():
    """Fetch & analyze regulation sizes for agencies"""
    global agency_cache
    client = ECFRClient()
    agencies = client.get_agencies()
    results = []

    for agency in agencies[:10]:  # Limit to 10 agencies for demo
        name = agency.get("name", "Unknown")
        slug = agency.get("slug", "")

        try:
            data = client.get_titles_for_agency(slug)
            if data:
                size_mb = client.calculate_size(data)
                results.append({
                    "agency_name": name,
                    "agency_slug": slug,
                    "regulation_size_mb": size_mb,
                    "last_updated": data.get("last_updated", "N/A")
                })
            await asyncio.sleep(0.2)  # throttle API calls
        except Exception as e:
            logger.error(f"Error analyzing {name}: {e}")
            continue

    agency_cache = sorted(results, key=lambda x: x["regulation_size_mb"], reverse=True)
    return agency_cache

@app.on_event("startup")
async def startup_event():
    logger.info("Running initial analysis...")
    await analyze_regulations()
    logger.info("Initial analysis complete")

@app.get("/")
async def root():
    return {
        "message": "eCFR Regulation Analyzer API",
        "status": "running",
        "endpoints": {
            "agency_sizes": "/api/v1/agencies/size",
            "health": "/api/v1/health",
            "update": "/api/v1/update"
        }
    }

@app.get("/api/v1/agencies/size")
async def get_agency_sizes():
    if agency_cache is None:
        await analyze_regulations()
    return agency_cache or []

@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy", "service": "eCFR Analyzer"}

@app.get("/api/v1/update")
async def manual_update():
    results = await analyze_regulations()
    return {
        "message": "Data updated successfully",
        "agencies_analyzed": len(results)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
