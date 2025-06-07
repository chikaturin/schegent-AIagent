from agents.tool.interface.index import State
from langchain.tools import tool
from config.llm import llm
from agents.tool.Data.get_habits import getHabits

import json


def planning_prompt(habits, require_user):
    return f"""
    Bạn là một trợ lý lập kế hoạch AI thông minh.
    Nhiệm vụ của bạn là lập lịch tuần đầu tiên cho người dùng dựa trên thông tin họ cung cấp (thói quen, ưu tiên, khung giờ,...).

    Dữ liệu người dùng:
    {json.dumps({"habits": habits, "require_user": require_user}, ensure_ascii=False)}

    Nếu người dùng không cung cấp đầy đủ thông tin, hãy sử dụng mặc định:
    🔹 Thứ 2 – Thứ 6:
        - Hoạt động chính: học tập, làm việc, tập thể dục.
        - Có thời gian nghỉ xen kẽ, không để quá tải.
        - Có đủ 3 bữa ăn mỗi ngày.
    🔹 Thứ Bảy và Chủ Nhật:
        - Lịch nhẹ nhàng, tập trung thư giãn, nghỉ ngơi.
        - Vẫn có thể duy trì tập luyện nhẹ và tổng kết tuần.
        - Đầy đủ 3 bữa ăn trong ngày
        - Bắt đầu sau giờ thức dậy và kết thúc trước giờ ngủ.

    🔹 Nếu người dùng đã có lịch biểu trước đó:
    - Giữ nguyên thời gian họ đã đặt.
    - Chỉ bổ sung các khung trống dựa theo thứ tự ưu tiên.

    🔹 Quy định quan trọng:
    - Mỗi hoạt động được mô tả theo đúng định dạng bảng `events` trong hệ thống, có cấu trúc như sau:

    ```json
    {{
        "DayOfWeek" : "Monday | Tuesday ",
        "title": "string - tiêu đề ngắn gọn",
        "description": "string - mô tả chi tiết (tùy chọn)",
        "location": "string - địa điểm nếu có",
        "start_time": "ISO datetime - ví dụ: 2025-06-01T06:30:00",
        "end_time": "ISO datetime - ví dụ: 2025-06-01T07:15:00",
        "hangout_link": "string (tùy chọn) - liên kết video call",
        "icon": "string - biểu tượng hoạt động (vd: 📚, 🧘‍♀️, 🍽️...)",
        "priority": "low | medium | high",
        "event_category": "general | habit | task",
    }}
    ```

    🔹 Trả về kết quả dưới dạng danh sách JSON, gồm nhiều sự kiện trong tuần đầu tiên.
    🔹 Trả về **chỉ nội dung JSON**, không thêm mô tả, không markdown, không ghi chú.

    🧠 Gợi ý ưu tiên:
    - Ưu tiên theo mục tiêu và thói quen của người dùng (ví dụ: học tập > công việc > thể dục).
    - Mỗi ngày có ít nhất 1–3 khoảng nghỉ.
    - Giờ hoạt động nằm trong khung từ giờ thức dậy đến giờ đi ngủ.
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
    prompt = planning_prompt(habits, user_constraints)

    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": user_content},
    ]

    reply = llm.invoke(messages)

    state["messages"].append({"role": "assistant", "content": reply.content})
    state["message_type"] = "schedule_created"

    return state
