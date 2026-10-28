import logging
import os
from datetime import datetime, timezone
from threading import Lock
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field


LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Patient Vitals API",
    description="REST API for recording and retrieving patient vital signs.",
    version="1.0.0",
)

class PatientVitals(BaseModel):
    patient_id: str = Field(min_length=1, max_length=50)
    heart_rate: int = Field(ge=20, le=250)
    temperature: float = Field(ge=25, le=45)
    systolic_bp: int = Field(ge=50, le=300)
    diastolic_bp: int = Field(ge=30, le=200)
    spo2: float = Field(ge=0, le=100)


vitals_store: dict[str, dict] = {}
store_lock = Lock()


@app.get("/")
def root() -> dict:
    return {
        "message": "Patient Vitals API is running",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health_check() -> dict:
    return {"status": "healthy"}


@app.post("/vitals", status_code=201)
def create_vitals(vitals: PatientVitals) -> dict:
    record = {
        **vitals.model_dump(),
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }

    with store_lock:
        vitals_store[vitals.patient_id] = record

    logger.info("Vitals recorded for patient_id=%s", vitals.patient_id)

    return {
        "message": "Vitals recorded successfully",
        "data": record,
    }


@app.get("/vitals/{patient_id}")
def get_vitals(patient_id: str) -> dict:
    with store_lock:
        record = vitals_store.get(patient_id)

    if record is None:
        raise HTTPException(
            status_code=404,
            detail="Patient vitals not found",
        )

    return {"data": record}


@app.get("/vitals")
def list_vitals(
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> dict:
    with store_lock:
        records = list(vitals_store.values())

    return {
        "count": len(records[:limit]),
        "items": records[:limit],
    }
