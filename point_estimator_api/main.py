import os

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from point_estimator_api.schemas import (
    EstimatePointsRequest,
    EstimatePointsResponse,
    HealthResponse,
)
from point_estimator_api.services import calculate_points


app = FastAPI(
    title="Point Estimator API",
    version="1.0.0",
    description="REST API for estimating points from stars, description, timestamp, and location.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def require_api_key(x_api_key: str | None):
    expected = os.getenv("API_KEY", "").strip()
    if not expected:
        return
    if not x_api_key or x_api_key != expected:
        raise HTTPException(status_code=401, detail="Invalid or missing X-API-Key header")


@app.get("/")
def root():
    protected = bool(os.getenv("API_KEY", "").strip())
    return {
        "message": "Point Estimator API is running",
        "docs": "/docs",
        "health": "/health",
        "estimate_endpoint": "/estimate-points",
        "api_key_required": protected,
    }


@app.get("/health", response_model=HealthResponse)
def health():
    protected = bool(os.getenv("API_KEY", "").strip())
    return {"status": "ok", "api_key_required": protected}


@app.post("/estimate-points", response_model=EstimatePointsResponse)
def estimate_points(payload: EstimatePointsRequest, x_api_key: str | None = Header(default=None)):
    require_api_key(x_api_key)
    try:
        return calculate_points(
            payload.stars,
            payload.task_title,
            payload.task_description,
            payload.timestamp,
            payload.location,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
