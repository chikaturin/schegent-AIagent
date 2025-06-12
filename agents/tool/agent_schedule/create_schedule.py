from agents.tool.interface.index import State
from langchain.tools import tool
from config.llm import llm
from agents.tool.Data.get_habits import getHabits
from agents.tool.rag.query_habit import query_rag


import json


def planning_prompt(habits, habitPlan, require_user):
    return f"""
    Bạn là một trợ lý lập kế hoạch AI thông minh.
    🎯 Nhiệm vụ: Lập lịch tuần đầu tiên cho người dùng dựa trên thói quen, mục tiêu, và dữ liệu lịch biểu hiện có.

    📦 Dữ liệu đầu vào:
    {json.dumps({"habits": habits, "habitPlan": habitPlan, "require_user": require_user}, ensure_ascii=False)}

    ⚙️ Hướng dẫn xử lý:
    1. Nếu có `habitPlan` thì dùng làm ưu tiên chính để chèn lịch dựa trên mức độ ưu tiên và các hoạt động thường ngày.
    2. Nếu không có, dùng thói quen và nguyên tắc mặc định. Bạn tự tạo lịch.
    🧩 Nguyên tắc xử lý lịch:
    - Tìm **các khung thời gian trống trong ngày** (giữa giờ thức dậy và giờ ngủ).
    - Trong các khung trống đó, chèn thêm hoạt động còn thiếu theo mức độ ưu tiên: học tập > công việc > thể dục > nghỉ ngơi.
    - Đảm bảo mỗi ngày có:
    - 3 bữa ăn (sáng, trưa, tối)
    - 1–2 khoảng nghỉ rõ ràng
    - Không xếp quá tải liên tục trên 4 tiếng

    📅 Quy định mặc định:
    - Thứ 2 – Thứ 6: học tập, làm việc, thể dục.
    - Cuối tuần: thư giãn, tổng kết tuần, nghỉ ngơi, vận động nhẹ.

    📄 Mỗi hoạt động có cấu trúc:
    ```json
    {{
    "DayOfWeek": "Monday | Tuesday | ...",
    "title": "string",
    "description": "string (optional)",
    "location": "string (optional)",
    "start_time": "ISO datetime",
    "end_time": "ISO datetime",
    "hangout_link": "string (optional)",
    "icon": "string - biểu tượng hoạt động (vd: 📚, 🧘‍♀️, 🍽️...)",
    "priority": "low | medium | high",
    "event_category": "general | habit | task"
    }}
    """


def extract_constraints(user_content: str, llm) -> str:
    messages = [
        {
            "role": "system",
            "content": "Trích xuất các yêu cầu ràng buộc từ người dùng, ví dụ: nghỉ ngày nào, muốn làm gì, các hoạt động ưu tiên. Trả về một đoạn ngắn tóm tắt.",
        },
        {"role": "user", "content": user_content},
    ]
    response = llm.invoke(messages)
    return response.content


def create_new_schedule(state: State):
    print("Creating new schedule...")
    last_message = state["messages"][-1]
    user_content = last_message.get("content", "")
    print(f"User content: {user_content}")

    habits = getHabits()
    user_constraints = extract_constraints(user_content, llm)
    habitPlan = query_rag()
    prompt = planning_prompt(habits, habitPlan, user_constraints)

    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": user_content},
    ]

    reply = llm.invoke(messages)

    print(f"LLM Creater reply: {reply.content}")

    state["messages"].append({"role": "assistant", "content": reply.content})
    state["message_type"] = "schedule_created"

    return state
