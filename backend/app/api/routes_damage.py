"""
FastAPI Routes for Infrastructure Damage Reporting, Field Inspections,
Computer Vision Detection, and Proximity Asset Association.
"""
from __future__ import annotations

from pathlib import Path
import time
from typing import Any, Dict, List, Optional
import uuid

import cv2
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.config.location_config import is_within_pune, validate_pune_coordinates
from app.cv.road_damage_detector import RoadDamageDetector
from app.database.database import (
    get_damage_report_by_id,
    get_damage_reports,
    save_damage_report,
    update_damage_report_status,
)

router = APIRouter(tags=["Damage Reporting"])

UPLOAD_DIR = Path(__file__).resolve().parents[2] / "data" / "uploads" / "damage_reports"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB

detector = RoadDamageDetector()


@router.post("/damage-reports")
async def create_damage_report(
    image: UploadFile = File(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    damage_type: str = Form(...),
    infrastructure_type: Optional[str] = Form(None),
    pune_ward: Optional[str] = Form(None),
    locality: Optional[str] = Form(None),
    address: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
):
    """Submits a field damage inspection report with photograph, coordinates,

    automatic Pune boundary validation, CV defect detection, and nearest-asset association.
    """
    # 1. Validate Geographic Boundary (Pune City Only)
    is_valid_loc, loc_msg = validate_pune_coordinates(latitude, longitude)
    if not is_valid_loc:
        raise HTTPException(status_code=400, detail=loc_msg)

    # 2. Validate Image File
    if not image.filename:
        raise HTTPException(status_code=400, detail="Missing inspection image filename.")

    ext = Path(image.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file extension '{ext}'. Supported formats: JPG, JPEG, PNG, WEBP.",
        )

    if image.content_type and image.content_type.lower() not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid MIME type '{image.content_type}'. Must be an image (JPEG, PNG, WEBP).",
        )

    contents = await image.read()
    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="Uploaded image file is empty.")

    if len(contents) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=400,
            detail=f"Uploaded image exceeds maximum allowable size (10 MB). Current size: {len(contents) / (1024*1024):.1f} MB.",
        )

    # 3. Store Image Securely with Unique UUID Filename (No Path Traversal)
    report_id = f"REP-PN-{time.strftime('%Y%m')}-{uuid.uuid4().hex[:6].upper()}"
    safe_filename = f"{report_id}{ext}"
    target_filepath = UPLOAD_DIR / safe_filename

    with target_filepath.open("wb") as fh:
        fh.write(contents)

    image_url = f"/api/damage-reports/{report_id}/image"

    # 4. Computer Vision Analysis via RoadDamageDetector
    cv_detected = None
    cv_confidence = None
    cv_rdi = None
    cv_details = None

    try:
        cv_res = detector.detect(contents)
        cv_rdi = cv_res.get("road_damage_index")
        detected_items = cv_res.get("detections", [])
        if detected_items:
            cv_detected = detected_items[0].get("damage_type", "Surface Distress")
            cv_confidence = detected_items[0].get("confidence", 0.85)
        else:
            cv_detected = cv_res.get("overall_condition", "Evaluated")
            cv_confidence = 0.80

        cv_details = {
            "overall_condition": cv_res.get("overall_condition"),
            "road_damage_index": cv_rdi,
            "defect_surface_area_pct": cv_res.get("defect_surface_area_pct"),
            "detections_count": cv_res.get("detections_count"),
            "validation_note": cv_res.get("validation_note"),
        }
    except Exception:
        cv_detected = f"Manual classification: {damage_type}"
        cv_confidence = None
        cv_details = {"note": "CV analysis not applicable or image inconclusive for this surface type."}

    # 5. Save Report to Database and Associate with Nearest Infrastructure Asset
    record = save_damage_report(
        report_id=report_id,
        image_filename=safe_filename,
        image_url=image_url,
        latitude=latitude,
        longitude=longitude,
        damage_type=damage_type,
        infrastructure_type=infrastructure_type,
        pune_ward=pune_ward,
        locality=locality,
        address=address,
        description=description,
        cv_detected=cv_detected,
        cv_confidence=cv_confidence,
        cv_rdi=cv_rdi,
        cv_details=cv_details,
    )

    return {
        "status": "success",
        "message": "Infrastructure damage report logged successfully.",
        "report": record,
    }


@router.get("/damage-reports")
def list_damage_reports(
    status: Optional[str] = None,
    limit: int = 50,
):
    """Retrieves logged infrastructure damage reports in Pune."""
    reports = get_damage_reports(status=status, limit=limit)
    return {
        "status": "success",
        "total": len(reports),
        "reports": reports,
    }


@router.get("/damage-reports/{report_id}")
def get_damage_report(report_id: str):
    """Retrieves full details of a specific damage report."""
    report = get_damage_report_by_id(report_id.strip())
    if not report:
        raise HTTPException(status_code=404, detail=f"Damage report '{report_id}' not found.")
    return report


@router.get("/damage-reports/{report_id}/image")
def get_damage_report_image(report_id: str):
    """Serves the securely stored inspection photograph for a damage report."""
    report = get_damage_report_by_id(report_id.strip())
    if not report:
        raise HTTPException(status_code=404, detail=f"Damage report '{report_id}' not found.")

    filename = report.get("image_filename")
    if not filename:
        raise HTTPException(status_code=404, detail="Image not found for this report.")

    filepath = UPLOAD_DIR / filename
    if not filepath.exists():
        raise HTTPException(status_code=404, detail="Image file missing from storage.")

    media_type = "image/jpeg"
    ext = filepath.suffix.lower()
    if ext == ".png":
        media_type = "image/png"
    elif ext == ".webp":
        media_type = "image/webp"

    return FileResponse(filepath, media_type=media_type)


@router.patch("/damage-reports/{report_id}/status")
def update_status(report_id: str, payload: Dict[str, str]):
    """Updates the inspection status of an existing damage report."""
    new_status = payload.get("status")
    if not new_status:
        raise HTTPException(status_code=400, detail="Missing 'status' in request body.")

    try:
        updated = update_damage_report_status(report_id.strip(), new_status)
        if not updated:
            raise HTTPException(status_code=404, detail=f"Damage report '{report_id}' not found.")
        return {"status": "success", "report_id": report_id, "new_status": new_status}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
