import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / 'data' / 'infrastructure_history.db'


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.execute(
        '''
        CREATE TABLE IF NOT EXISTS infrastructure_assets (
            asset_id TEXT PRIMARY KEY,
            asset_type TEXT,
            zone TEXT,
            age_years REAL,
            material TEXT,
            traffic_density REAL,
            average_load REAL,
            annual_rainfall REAL,
            average_temperature REAL,
            maintenance_count REAL,
            days_since_maintenance REAL,
            days_since_inspection REAL,
            structural_score REAL,
            corrosion_level REAL,
            previous_failures INTEGER,
            usage_intensity REAL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )
    connection.execute(
        '''
        CREATE TABLE IF NOT EXISTS prediction_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_id TEXT,
            asset_type TEXT,
            zone TEXT,
            failure_probability REAL,
            risk_level TEXT,
            remaining_useful_life REAL,
            priority TEXT,
            recommendation TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )
    connection.commit()
    connection.close()


def save_prediction_history(record: dict):
    init_db()
    connection = sqlite3.connect(DB_PATH)
    connection.execute(
        '''
        INSERT INTO prediction_history (
            asset_id, asset_type, zone, failure_probability, risk_level,
            remaining_useful_life, priority, recommendation
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            record.get('asset_id'),
            record.get('asset_type'),
            record.get('zone'),
            record.get('failure_probability'),
            record.get('risk_level'),
            record.get('remaining_useful_life'),
            record.get('priority'),
            record.get('recommendation'),
        )
    )
    connection.commit()
    connection.close()


def get_prediction_history(limit: int = 10):
    init_db()
    connection = sqlite3.connect(DB_PATH)
    rows = connection.execute(
        '''SELECT asset_id, asset_type, zone, failure_probability, risk_level, remaining_useful_life, priority, recommendation
        FROM prediction_history ORDER BY id DESC LIMIT ?''',
        (limit,),
    ).fetchall()
    connection.close()
    return [
        {
            'asset_id': row[0],
            'asset_type': row[1],
            'zone': row[2],
            'failure_probability': row[3],
            'risk_level': row[4],
            'remaining_useful_life': row[5],
            'priority': row[6],
            'recommendation': row[7],
        }
        for row in rows
    ]
