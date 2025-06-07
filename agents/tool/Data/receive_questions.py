from config.database import get_db

default_data = {
    "Target Goal": "Học tập",
    "Available Time": "Sáng",
    "Planning Frequency": "Ngày",
    "Priorities": "Sức khỏe > Học tập > Công việc",
    "Sleep Habit": "Ngủ lúc 11 giờ tối, dậy lúc 6 giờ sáng",
    "Food Preferences": "Thích ăn chay, hạn chế đồ ngọt",
}


def save_habitat():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user_habits (
            id SERIAL PRIMARY KEY,
            target_goal VARCHAR(255),
            available_time VARCHAR(255),
            planning_frequency VARCHAR(255),
            priorities TEXT,
            sleep_habit TEXT,
            food_preferences TEXT
        )
    """
    )

    # Insert dữ liệu
    cursor.execute(
        """
        INSERT INTO user_habits (target_goal, available_time, planning_frequency, priorities, sleep_habit, food_preferences)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            default_data["Target Goal"],
            default_data["Available Time"],
            default_data["Planning Frequency"],
            default_data["Priorities"],
            default_data["Sleep Habit"],
            default_data["Food Preferences"],
        ),
    )

    conn.commit()
    cursor.close()
    print("✅ Dữ liệu đã được lưu thành công.")
    return default_data
