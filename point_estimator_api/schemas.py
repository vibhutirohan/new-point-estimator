from pydantic import BaseModel, Field


class EstimatePointsRequest(BaseModel):
    stars: float = Field(..., ge=1, le=5, description="Star rating between 1 and 5")
    task_title: str = Field(..., min_length=1, description="Title of the task")
    task_description: str = Field(..., min_length=1, description="Detailed description of the task")
    timestamp: str = Field(..., description="ISO 8601 UTC timestamp, for example 2026-03-29T02:30:00Z")
    location: str = Field(..., min_length=1, description="Task location")


class HealthResponse(BaseModel):
    status: str
    api_key_required: bool


class EstimatePointsResponse(BaseModel):
    submission: dict
    breakdown: dict
    totalPoints: int
    tier: str
    badge: str
