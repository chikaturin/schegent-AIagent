from agents.tool.interface.index import State
from langchain.tools import tool
from config.llm import llm
from agents.tool.Data.events import getSchedule, processEvents
from config.convert_json import convert_json
from datetime import datetime

import json


def planning_prompt(schedule, require_user):
    now = datetime.now().isoformat()
    return f"""
    Bạn là AI chuyên gia quản lý lịch trình thông minh với khả năng xử lý xung đột thời gian và tối ưu hóa scheduling.
    NHIỆM VỤ: Chỉnh sửa lịch trình dựa trên yêu cầu cụ thể với logic xử lý intelligent.

    DỮ LIỆU ĐẦU VÀO:
    📦 Dữ liệu đầu vào:
    {json.dumps({"schedule": schedule,"current_time":now, "require_user": require_user}, ensure_ascii=False)}
    - schedule: Lịch trình hiện tại
    - require_user: Yêu cầu chỉnh sửa
    - current_time: Thời gian hiện tại (ISO format)

    LOGIC XỬ LÝ:
    1. PHÂN TÍCH THỜI GIAN:
    - Sự kiện đã qua: Không thay đổi của ngày hôm đó
    - Sự kiện đang diễn ra: Chỉ sửa phần còn lại từ current_time
    - Sự kiện tương lai: Có thể sửa toàn bộ

    2. XỬ LÝ XUNG ĐỘT:
    - Nếu Sự kiện bị dính thời gian cần sửa trong 1 ngày → Sửa toàn bộ ngày đó

    3. QUYẾT ĐỊNH SMART:
    - Tối ưu hóa khoảng trống
    - Giữ nguyên pattern thói quen
    - Minimize disruption

    ĐẦU RA: Chỉ trả về events bị thay đổi (new/update/delete) dưới dạng JSON array:

   ```json
    {{
    "state": "new | update | delete",
    "id": "string (optional, chỉ khi state là update, delete)",
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

    YÊU CẦU: Chỉ JSON, không markdown, không giải thích thêm.


    """


def extract_constraints(user_content: str, llm) -> str:
    messages = [
        {
            "role": "system",
            "content": "Trích xuất các yêu cầu ràng buộc từ người dùng, ví dụ: nghỉ ngày nào, muốn làm gì, giờ nào và các hoạt động ưu tiên. Trả về một đoạn ngắn tóm tắt, nếu người dùng ghi ví dụ: 12h là 12 giờ.",
        },
        {"role": "user", "content": user_content},
    ]
    response = llm.invoke(messages)
    return response.content


def extract_infor(user_content: str, llm) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "Trích xuất các yêu cầu ràng buộc từ người dùng. Trả về một đoạn ngắn tóm tắt.\n"
                "json:\n"
                "{\n"
                '    "day_of_week" : "Monday, Tuesday,...,Sunday ",\n'
                "}"
            ),
        },
        {"role": "user", "content": user_content},
    ]
    response = llm.invoke(messages)
    return response.content


def update_schedule(state: State):
    print("Update schedule...")

    last_message = state["messages"][-1]
    user_content = last_message.get("content", "")

    # Trích xuất thông tin từ người dùng để xác định ngày và yêu cầu cập nhật lịch trình
    response = extract_infor(user_content, llm)
    query = convert_json(response)
    result = getSchedule(query.get("day_of_week", ""))

    # Trích xuất các ràng buộc từ nội dung người dùng
    user_constraints = extract_constraints(user_content, llm)
    prompt = planning_prompt(result, user_constraints)

    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": user_content},
    ]

    reply = llm.invoke(messages)

    print(f"LLM Update reply: {reply.content}")

    save_schegent = convert_json(reply.content)
    processEvents(save_schegent)

    state["messages"].append(
        {"role": "assistant", "content": "Lịch trình đã được cập nhật."}
    )
    state["message_type"] = "schedule_created"

    return state
