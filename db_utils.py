import sqlite3


def init_db(db_path):
    """
    Set up the attendance database.
    Any existing attendance table is removed to ensure
    the schema is always in a known state.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Remove old table if it exists to avoid schema conflicts
    cursor.execute("DROP TABLE IF EXISTS attendance")

    # Create the attendance table
    cursor.execute("""
        CREATE TABLE attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_name TEXT NOT NULL,
            entry_time TEXT NOT NULL,
            exit_time TEXT,
            outside_duration REAL DEFAULT 0,
            status TEXT DEFAULT 'Inside'
        )
    """)

    conn.commit()
    conn.close()


def create_session(db_path, person_name, entry_time):
    """
    Record a new entry event for a person.
    """
    # Basic validation to avoid empty names
    if not person_name or str(person_name).strip() == "":
        person_name = "Unknown"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO attendance (person_name, entry_time, status)
        VALUES (?, ?, 'Inside')
    """, (person_name, entry_time))

    conn.commit()
    conn.close()


def update_exit(db_path, person_name, exit_time, outside_duration=0):
    """
    Update the most recent open session for a person
    when they leave the monitored area.
    """
    # Basic validation to avoid empty names
    if not person_name or str(person_name).strip() == "":
        person_name = "Unknown"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE attendance
        SET exit_time = ?, outside_duration = ?, status = 'Outside'
        WHERE person_name = ? AND exit_time IS NULL
    """, (exit_time, outside_duration, person_name))

    conn.commit()
    conn.close()
