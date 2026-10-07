from __future__ import annotations

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]


def risk_level_from_probability(probability: float) -> str:
    probability = float(probability)
    if probability < 0.4:
        return 'LOW'
    if probability < 0.7:
        return 'MEDIUM'
    return 'HIGH'


def format_probability(probability: float) -> float:
    return round(float(probability) * 100, 2)


def priority_from_prediction(probability: float, structural_score: float, previous_failures: int, days_since_maintenance: float) -> str:
    score = probability * 100 + (100 - structural_score) * 0.5 + previous_failures * 8 + min(days_since_maintenance / 30, 40)
    if score >= 80:
        return 'CRITICAL'
    if score >= 60:
        return 'HIGH'
    if score >= 40:
        return 'MEDIUM'
    return 'LOW'
