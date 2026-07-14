import sqlite3
from datetime import datetime
from typing import Optional, List
from contextlib import contextmanager
from schemas import Alert, Prediction

DATABASE_PATH = "data/sentinelflow.db"


@contextmanager
def get_db():
    """Context manager for safe DB connections."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    """Create tables if they don't exist."""
    with get_db() as conn:
        conn.execute("""
                     CREATE TABLE IF NOT EXISTS predictions
                     (
                         flow_id
                         INTEGER
                         PRIMARY
                         KEY,
                         timestamp
                         TEXT,
                         anomaly_score
                         REAL,
                         is_anomaly
                         INTEGER,
                         confidence
                         REAL
                     )
                     """)
        conn.execute("""
                     CREATE TABLE IF NOT EXISTS alerts
                     (
                         alert_id
                         INTEGER
                         PRIMARY
                         KEY
                         AUTOINCREMENT,
                         timestamp
                         TEXT,
                         severity
                         TEXT,
                         source_ip
                         TEXT,
                         destination_ip
                         TEXT,
                         alert_type
                         TEXT,
                         description
                         TEXT,
                         anomaly_score
                         REAL,
                         status
                         TEXT
                     )
                     """)


def insert_prediction(pred: Prediction) -> None:
    """Store a model prediction."""
    with get_db() as conn:
        conn.execute(
            """INSERT OR REPLACE INTO predictions 
               (flow_id, timestamp, anomaly_score, is_anomaly, confidence)
               VALUES (?, ?, ?, ?, ?)""",
            (
                pred.flow_id,
                pred.timestamp.isoformat(),
                pred.anomaly_score,
                int(pred.is_anomaly),
                pred.confidence,
            ),
        )


def insert_alert(alert: Alert) -> None:
    """Store a generated alert."""
    with get_db() as conn:
        cursor = conn.execute(
            """INSERT INTO alerts
               (timestamp, severity, source_ip, destination_ip,
                alert_type, description, anomaly_score, status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                alert.timestamp.isoformat(),
                alert.severity.value,
                alert.source_ip,
                alert.destination_ip,
                alert.alert_type,
                alert.description,
                alert.anomaly_score,
                alert.status.value,
            ),
        )
        alert.alert_id = cursor.lastrowid


def get_alerts(
        status: Optional[str] = None,
        limit: int = 100,
) -> List[Alert]:
    """Fetch alerts, optionally filtered by status."""
    with get_db() as conn:
        query = "SELECT * FROM alerts"
        params = []
        if status:
            query += " WHERE status = ?"
            params.append(status)
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)

        rows = conn.execute(query, params).fetchall()
        return [
            Alert(
                alert_id=row["alert_id"],
                timestamp=datetime.fromisoformat(row["timestamp"]),
                severity=row["severity"],
                source_ip=row["source_ip"],
                destination_ip=row["destination_ip"],
                alert_type=row["alert_type"],
                description=row["description"],
                anomaly_score=row["anomaly_score"],
                status=row["status"],
            )
            for row in rows
        ]


def update_alert_status(alert_id: int, status: str) -> bool:
    """Mark an alert as investigating, resolved, etc."""
    with get_db() as conn:
        cursor = conn.execute(
            "UPDATE alerts SET status = ? WHERE alert_id = ?",
            (status, alert_id),
        )
        return cursor.rowcount > 0