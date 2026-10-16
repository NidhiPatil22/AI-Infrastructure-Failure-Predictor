"""
FastAPI Endpoints for Dataset Audit and Clean Pipeline Verification
"""
from __future__ import annotations

import io
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query, Response
from fastapi.responses import StreamingResponse

from app.ml.dataset_auditor import auditor
from app.ml.pipeline_verifier import pipeline_verifier

router = APIRouter(tags=["Dataset Audit & Pipeline Verification"])


@router.get("/audit/summary")
async def get_audit_summary() -> Dict[str, Any]:
    """Retrieves full dynamic dataset audit summary, quality score, target imbalance,

    domain validation findings, and provenance metadata.
    """
    try:
        return auditor.audit()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to audit dataset: {exc}")


@router.get("/audit/findings")
async def get_audit_findings(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    issue_type: Optional[str] = None,
) -> Dict[str, Any]:
    """Retrieves paginated record-level validation findings (missing values, range violations)."""
    try:
        report = auditor.audit()
        all_findings: List[Dict[str, Any]] = report.get("record_findings_sample", [])
        if issue_type:
            all_findings = [f for f in all_findings if f.get("issue_type") == issue_type]

        total = len(all_findings)
        paginated = all_findings[offset : offset + limit]

        return {
            "total_findings": total,
            "limit": limit,
            "offset": offset,
            "findings": paginated,
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve audit findings: {exc}")


@router.get("/audit/export/csv")
async def export_audit_csv():
    """Generates and downloads a CSV report containing record-level audit findings."""
    try:
        csv_content = auditor.export_csv_report()
        return StreamingResponse(
            io.StringIO(csv_content),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=dataset_audit_findings.csv"},
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to export CSV: {exc}")


@router.get("/audit/export/json")
async def export_audit_json():
    """Generates and downloads a comprehensive JSON report containing the complete audit."""
    try:
        json_content = auditor.export_json_report()
        return StreamingResponse(
            io.StringIO(json_content),
            media_type="application/json",
            headers={"Content-Disposition": "attachment; filename=dataset_audit_report.json"},
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to export JSON: {exc}")


@router.post("/pipeline-tests/run")
async def run_pipeline_tests() -> Dict[str, Any]:
    """Executes the automated 12-check Clean Pipeline Verification suite

    and returns structured test results, evidence, and code references.
    """
    try:
        return pipeline_verifier.run_all_checks()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to execute pipeline verification: {exc}")


@router.get("/pipeline-tests/results")
async def get_pipeline_test_results() -> Dict[str, Any]:
    """Retrieves the latest verification run results or executes a new run if not yet cached."""
    try:
        cached = pipeline_verifier.get_last_run()
        if cached is None:
            cached = pipeline_verifier.run_all_checks()
        return cached
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve pipeline test results: {exc}")
