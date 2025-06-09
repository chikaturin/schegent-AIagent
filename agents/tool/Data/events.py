from config.database import get_db


def getSchedule(day_of_week: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT * FROM events WHERE day_of_week= %s",
        (day_of_week,),
    )

    columns = [desc[0] for desc in cursor.description]

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    results = [dict(zip(columns, row)) for row in rows]

    return {
        "data": results,
    }


def processEvents(events):
    conn = None
    cursor = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        for event in events:
            if event.get("state") == "new":
                cursor.execute(
                    """
                    INSERT INTO events (day_of_week, title, description, location, start_time, end_time, icon, priority, event_category)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        event.get("DayOfWeek"),
                        event.get("title"),
                        event.get("description"),
                        event.get("location"),
                        event.get("start_time"),
                        event.get("end_time"),
                        event.get("icon"),
                        event.get("priority"),
                        event.get("event_category"),
                    ),
                )
            elif event.get("state") == "update":
                event_id = event.get("id")
                if event_id is None:
                    raise ValueError("Missing 'id' for update event.")

                cursor.execute(
                    """
                    UPDATE events
                    SET  day_of_week = %s,
                         title = %s,
                         description = %s,
                         location = %s,
                         start_time = %s,
                         end_time = %s,
                         icon = %s,
                         priority = %s,
                         event_category = %s
                    WHERE id = %s
                    """,
                    (
                        event.get("DayOfWeek"),
                        event.get("title"),
                        event.get("description"),
                        event.get("location"),
                        event.get("start_time"),
                        event.get("end_time"),
                        event.get("icon"),
                        event.get("priority"),
                        event.get("event_category"),
                        event_id,
                    ),
                )
            elif event.get("state") == "delete":
                event_id = event.get("id")
                if event_id is None:
                    raise ValueError("Missing 'id' for delete event.")

                cursor.execute(
                    """
                    DELETE FROM events WHERE id = %s
                    """,
                    (event_id,),
                )
        if conn and not conn.closed:
            conn.commit()
    except Exception as e:
        print(f"[ERROR] Failed to process events: {e}")
        try:
            if conn and not conn.closed:
                conn.rollback()
        except Exception as rollback_err:
            print(f"[ERROR] Rollback failed: {rollback_err}")
    finally:
        try:
            if cursor:
                cursor.close()
        except Exception as cursor_err:
            print(f"[ERROR] Closing cursor failed: {cursor_err}")
        try:
            if conn and not conn.closed:
                conn.close()
        except Exception as close_err:
            print(f"[ERROR] Closing connection failed: {close_err}")
