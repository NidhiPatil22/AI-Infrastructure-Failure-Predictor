"""FastAPI endpoints for Computer Vision road damage inspection."""
from __future__ import annotations

import base64
from pathlib import Path
from typing import Any, Dict

import cv2
from fastapi import APIRouter, File, HTTPException, UploadFile
import numpy as np

from app.cv.road_damage_detector import RoadDamageDetector, generate_sample_road_images

router = APIRouter(tags=["Computer Vision"])
detector = RoadDamageDetector()
SAMPLE_DIR = Path(__file__).resolve().parents[2] / "data" / "sample_road_images"


@router.post("/cv/detect-damage")
async def detect_road_damage(file: UploadFile = File(...)):
    """Uploads road imagery and performs damage detection using OpenCV + YOLO."""
    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Empty image uploaded.")

    try:
        results = detector.detect(contents)
        # Convert annotated RGB image to base64 jpeg
        annotated_bgr = cv2.cvtColor(results["annotated_image_rgb"], cv2.COLOR_RGB2BGR)
        _, buffer = cv2.imencode(".jpg", annotated_bgr)
        b64_img = base64.b64encode(buffer).decode("utf-8")

        return {
            "status": "success",
            "image_dimensions": results["image_dimensions"],
            "detections_count": results["detections_count"],
            "road_damage_index": results["road_damage_index"],
            "overall_condition": results["overall_condition"],
            "defect_surface_area_pct": results["defect_surface_area_pct"],
            "detections": results["detections"],
            "validation_note": results["validation_note"],
            "annotated_image_base64": f"data:image/jpeg;base64,{b64_img}",
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Image processing error: {str(exc)}")


@router.get("/cv/sample-images")
async def list_sample_images():
    """Lists pre-generated sample road images for testing."""
    if not SAMPLE_DIR.exists() or len(list(SAMPLE_DIR.glob("*.jpg"))) == 0:
        generate_sample_road_images(SAMPLE_DIR)

    samples = [f.name for f in SAMPLE_DIR.glob("*.jpg")]
    return {"status": "success", "samples": samples}


@router.get("/cv/detect-sample/{filename}")
async def detect_sample_image(filename: str):
    """Runs detection on one of the pre-generated test road images."""
    target_path = SAMPLE_DIR / filename
    if not target_path.exists():
        raise HTTPException(status_code=404, detail="Sample image not found.")

    results = detector.detect(target_path)
    annotated_bgr = cv2.cvtColor(results["annotated_image_rgb"], cv2.COLOR_RGB2BGR)
    _, buffer = cv2.imencode(".jpg", annotated_bgr)
    b64_img = base64.b64encode(buffer).decode("utf-8")

    return {
        "status": "success",
        "filename": filename,
        "image_dimensions": results["image_dimensions"],
        "detections_count": results["detections_count"],
        "road_damage_index": results["road_damage_index"],
        "overall_condition": results["overall_condition"],
        "defect_surface_area_pct": results["defect_surface_area_pct"],
        "detections": results["detections"],
        "validation_note": results["validation_note"],
        "annotated_image_base64": f"data:image/jpeg;base64,{b64_img}",
    }
