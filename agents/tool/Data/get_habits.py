from config.database import get_db


def getHabits():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_habits")

    columns = [desc[0] for desc in cursor.description]

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    results = [dict(zip(columns, row)) for row in rows]

    return {
        "data": results,
    }
