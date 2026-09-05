import sqlite3
from datetime import datetime

DB_PATH = "database/compliance.db"


def create_database():

    conn = sqlite3.connect(
        DB_PATH
    )

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS violations(
        id INTEGER PRIMARY KEY,
        timestamp TEXT,
        violation_type TEXT
    )
    """)

    # New table used by the redesigned UI to power real dashboard/analytics
    # numbers. Kept separate from the original `violations` table so no
    # existing behaviour is changed.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS detections(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        source_type TEXT,
        predicted_class TEXT,
        confidence REAL,
        is_compliant INTEGER
    )
    """)

    conn.commit()
    conn.close()


def insert_detection(source_type: str, predicted_class: str, confidence: float):
    """Logs a single detection result so the Dashboard/Analytics pages can
    display real figures instead of hardcoded numbers.

    source_type: "image" or "video"
    predicted_class: raw class name returned by the model (e.g. "helmet")
    confidence: model confidence score, 0-1
    """
    create_database()

    is_compliant = 1 if predicted_class.lower() == "helmet" else 0

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO detections (timestamp, source_type, predicted_class, confidence, is_compliant)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            datetime.now().isoformat(timespec="seconds"),
            source_type,
            predicted_class,
            confidence,
            is_compliant,
        ),
    )
    conn.commit()
    conn.close()


def get_summary_stats():
    """Returns aggregate counts used by the Dashboard KPI cards."""
    create_database()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM detections")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM detections WHERE is_compliant = 1")
    compliant = cursor.fetchone()[0]

    conn.close()

    violations = total - compliant
    compliance_rate = (compliant / total * 100) if total > 0 else 0.0

    return {
        "total": total,
        "compliant": compliant,
        "violations": violations,
        "compliance_rate": compliance_rate,
    }


def get_recent_detections(limit: int = 200):
    """Returns the most recent detection rows for the Analytics page and
    history tables. Each row: (timestamp, source_type, predicted_class,
    confidence, is_compliant)."""
    create_database()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT timestamp, source_type, predicted_class, confidence, is_compliant
        FROM detections
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,),
    )
    rows = cursor.fetchall()
    conn.close()
    return rows
