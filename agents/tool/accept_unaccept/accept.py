from config.database import get_db
from agents.tool.interface.index import State
import json
import os

events = [
    {
        "DayOfWeek": "Monday",
        "title": "Học tập buổi sáng",
        "description": "Dành thời gian cho việc học tập vào buổi sáng.",
        "location": "Nhà",
        "start_time": "2024-07-01T07:00:00",
        "end_time": "2024-07-01T11:00:00",
        "icon": "📚",
        "priority": "high",
        "event_category": "habit",
    },
    {
        "DayOfWeek": "Monday",
        "title": "Ăn trưa",
        "description": "Bữa trưa chay.",
        "location": "Nhà",
        "start_time": "2024-07-01T12:00:00",
        "end_time": "2024-07-01T13:00:00",
        "icon": "🍽️",
        "priority": "medium",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Monday",
        "title": "Tập thể dục",
        "description": "Tập thể dục nhẹ nhàng.",
        "location": "Công viên",
        "start_time": "2024-07-01T16:00:00",
        "end_time": "2024-07-01T17:00:00",
        "icon": "🧘‍♀️",
        "priority": "medium",
        "event_category": "habit",
    },
    {
        "DayOfWeek": "Monday",
        "title": "Ăn tối",
        "description": "Bữa tối chay.",
        "location": "Nhà",
        "start_time": "2024-07-01T19:00:00",
        "end_time": "2024-07-01T20:00:00",
        "icon": "🍽️",
        "priority": "medium",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Tuesday",
        "title": "Học tập buổi sáng",
        "description": "Dành thời gian cho việc học tập vào buổi sáng.",
        "location": "Nhà",
        "start_time": "2024-07-02T07:00:00",
        "end_time": "2024-07-02T11:00:00",
        "icon": "📚",
        "priority": "high",
        "event_category": "habit",
    },
    {
        "DayOfWeek": "Tuesday",
        "title": "Ăn trưa",
        "description": "Bữa trưa chay.",
        "location": "Nhà",
        "start_time": "2024-07-02T12:00:00",
        "end_time": "2024-07-02T13:00:00",
        "icon": "🍽️",
        "priority": "medium",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Tuesday",
        "title": "Tập thể dục",
        "description": "Tập thể dục nhẹ nhàng.",
        "location": "Công viên",
        "start_time": "2024-07-02T16:00:00",
        "end_time": "2024-07-02T17:00:00",
        "icon": "🧘‍♀️",
        "priority": "medium",
        "event_category": "habit",
    },
    {
        "DayOfWeek": "Tuesday",
        "title": "Ăn tối",
        "description": "Bữa tối chay.",
        "location": "Nhà",
        "start_time": "2024-07-02T19:00:00",
        "end_time": "2024-07-02T20:00:00",
        "icon": "🍽️",
        "priority": "medium",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Wednesday",
        "title": "Nghỉ ngơi",
        "description": "Ngày nghỉ ngơi hoàn toàn.",
        "location": "Nhà",
        "start_time": "2024-07-03T06:00:00",
        "end_time": "2024-07-03T22:00:00",
        "icon": "🏖️",
        "priority": "high",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Thursday",
        "title": "Học tập buổi sáng",
        "description": "Dành thời gian cho việc học tập vào buổi sáng.",
        "location": "Nhà",
        "start_time": "2024-07-04T07:00:00",
        "end_time": "2024-07-04T11:00:00",
        "icon": "📚",
        "priority": "high",
        "event_category": "habit",
    },
    {
        "DayOfWeek": "Thursday",
        "title": "Ăn trưa",
        "description": "Bữa trưa chay.",
        "location": "Nhà",
        "start_time": "2024-07-04T12:00:00",
        "end_time": "2024-07-04T13:00:00",
        "icon": "🍽️",
        "priority": "medium",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Thursday",
        "title": "Cuộc hẹn",
        "description": "Cuộc hẹn quan trọng.",
        "location": "Địa điểm hẹn",
        "start_time": "2024-07-04T14:00:00",
        "end_time": "2024-07-04T17:00:00",
        "icon": "💼",
        "priority": "high",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Thursday",
        "title": "Ăn tối",
        "description": "Bữa tối chay.",
        "location": "Nhà",
        "start_time": "2024-07-04T19:00:00",
        "end_time": "2024-07-04T20:00:00",
        "icon": "🍽️",
        "priority": "medium",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Friday",
        "title": "Học tập buổi sáng",
        "description": "Dành thời gian cho việc học tập vào buổi sáng.",
        "location": "Nhà",
        "start_time": "2024-07-05T07:00:00",
        "end_time": "2024-07-05T11:00:00",
        "icon": "📚",
        "priority": "high",
        "event_category": "habit",
    },
    {
        "DayOfWeek": "Friday",
        "title": "Ăn trưa",
        "description": "Bữa trưa chay.",
        "location": "Nhà",
        "start_time": "2024-07-05T12:00:00",
        "end_time": "2024-07-05T13:00:00",
        "icon": "🍽️",
        "priority": "medium",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Friday",
        "title": "Tập thể dục",
        "description": "Tập thể dục nhẹ nhàng.",
        "location": "Công viên",
        "start_time": "2024-07-05T16:00:00",
        "end_time": "2024-07-05T17:00:00",
        "icon": "🧘‍♀️",
        "priority": "medium",
        "event_category": "habit",
    },
    {
        "DayOfWeek": "Friday",
        "title": "Ăn tối",
        "description": "Bữa tối chay.",
        "location": "Nhà",
        "start_time": "2024-07-05T19:00:00",
        "end_time": "2024-07-05T20:00:00",
        "icon": "🍽️",
        "priority": "medium",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Saturday",
        "title": "Thư giãn buổi sáng",
        "description": "Thời gian thư giãn và làm những điều mình thích.",
        "location": "Nhà",
        "start_time": "2024-07-06T08:00:00",
        "end_time": "2024-07-06T11:00:00",
        "icon": "☕",
        "priority": "low",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Saturday",
        "title": "Ăn trưa",
        "description": "Bữa trưa chay.",
        "location": "Nhà",
        "start_time": "2024-07-06T12:00:00",
        "end_time": "2024-07-06T13:00:00",
        "icon": "🍽️",
        "priority": "medium",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Saturday",
        "title": "Đi dạo",
        "description": "Đi dạo trong công viên.",
        "location": "Công viên",
        "start_time": "2024-07-06T16:00:00",
        "end_time": "2024-07-06T17:00:00",
        "icon": "🚶",
        "priority": "low",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Saturday",
        "title": "Ăn tối",
        "description": "Bữa tối chay.",
        "location": "Nhà",
        "start_time": "2024-07-06T19:00:00",
        "end_time": "2024-07-06T20:00:00",
        "icon": "🍽️",
        "priority": "medium",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Sunday",
        "title": "Thư giãn buổi sáng",
        "description": "Thời gian thư giãn và làm những điều mình thích.",
        "location": "Nhà",
        "start_time": "2024-07-07T08:00:00",
        "end_time": "2024-07-07T11:00:00",
        "icon": "☕",
        "priority": "low",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Sunday",
        "title": "Ăn trưa",
        "description": "Bữa trưa chay.",
        "location": "Nhà",
        "start_time": "2024-07-07T12:00:00",
        "end_time": "2024-07-07T13:00:00",
        "icon": "🍽️",
        "priority": "medium",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Sunday",
        "title": "Tập thể dục nhẹ nhàng",
        "description": "Yoga hoặc đi bộ.",
        "location": "Nhà/Công viên",
        "start_time": "2024-07-07T16:00:00",
        "end_time": "2024-07-07T17:00:00",
        "icon": "🧘‍♀️",
        "priority": "low",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Sunday",
        "title": "Ăn tối",
        "description": "Bữa tối chay.",
        "location": "Nhà",
        "start_time": "2024-07-07T19:00:00",
        "end_time": "2024-07-07T20:00:00",
        "icon": "🍽️",
        "priority": "medium",
        "event_category": "general",
    },
]


def accept_schedule(state: State):
    print("⏳ Saving new schedule from state...")

    events = state.get("pending_schedule", [])
    if not events:
        state["messages"].append(
            {"role": "assistant", "content": "Không có lịch trình nào để lưu."}
        )
        return state

    conn = get_db()
    cursor = conn.cursor()

    for event in events:
        cursor.execute(
            """
            INSERT INTO events (
                day_of_week,
                title, description, location, start_time, end_time,
                icon, priority, event_category
            )
            VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s)
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

    conn.commit()
    cursor.close()

    print("✅ Lịch trình đã được lưu thành công.")
    state["messages"].append(
        {"role": "assistant", "content": "✅ Lịch trình đã được lưu thành công."}
    )
    state["message_type"] = "schedule_created"
    state.pop("pending_schedule", None)

    return state
