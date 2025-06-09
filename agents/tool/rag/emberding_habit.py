from config.llm import llm
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from agents.tool.interface.index import State
import json
import torch
import numpy as np
from transformers import AutoTokenizer, AutoModel
from langchain_community.vectorstores import FAISS
from langchain.embeddings.base import Embeddings
from langchain.docstore.document import Document


events = [
    {
        "DayOfWeek": "Monday",
        "title": "Tập thể dục buổi sáng",
        "description": "Khởi động ngày mới với bài tập nhẹ nhàng.",
        "location": "Nhà",
        "start_time": "2024-07-01T06:00:00",
        "end_time": "2024-07-01T06:30:00",
        "icon": "🧘‍♀️",
        "priority": "medium",
        "event_category": "habit",
    },
    {
        "DayOfWeek": "Monday",
        "title": "Ăn sáng",
        "description": "Bữa sáng chay lành mạnh.",
        "location": "Nhà",
        "start_time": "2024-07-01T06:30:00",
        "end_time": "2024-07-01T07:00:00",
        "icon": "🍽️",
        "priority": "high",
        "event_category": "habit",
    },
    {
        "DayOfWeek": "Monday",
        "title": "Học tập",
        "description": "Học các môn quan trọng.",
        "location": "Thư viện",
        "start_time": "2024-07-01T07:00:00",
        "end_time": "2024-07-01T11:00:00",
        "icon": "📚",
        "priority": "high",
        "event_category": "habit",
    },
    {
        "DayOfWeek": "Monday",
        "title": "Nghỉ ngơi",
        "description": "Nghỉ ngơi giữa buổi học.",
        "location": "Quán cafe",
        "start_time": "2024-07-01T11:00:00",
        "end_time": "2024-07-01T11:30:00",
        "icon": "☕",
        "priority": "low",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Monday",
        "title": "Ăn trưa",
        "description": "Bữa trưa chay.",
        "location": "Nhà",
        "start_time": "2024-07-01T11:30:00",
        "end_time": "2024-07-01T12:30:00",
        "icon": "🍽️",
        "priority": "high",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Monday",
        "title": "Làm việc",
        "description": "Giải quyết công việc.",
        "location": "Văn phòng",
        "start_time": "2024-07-01T12:30:00",
        "end_time": "2024-07-01T17:00:00",
        "icon": "💼",
        "priority": "medium",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Monday",
        "title": "Nghỉ ngơi",
        "description": "Đi dạo thư giãn.",
        "location": "Công viên",
        "start_time": "2024-07-01T17:00:00",
        "end_time": "2024-07-01T17:30:00",
        "icon": "🚶‍♀️",
        "priority": "low",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Monday",
        "title": "Ăn tối",
        "description": "Bữa tối chay nhẹ nhàng.",
        "location": "Nhà",
        "start_time": "2024-07-01T18:30:00",
        "end_time": "2024-07-01T19:30:00",
        "icon": "🍽️",
        "priority": "high",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Monday",
        "title": "Đọc sách",
        "description": "Đọc sách trước khi ngủ.",
        "location": "Phòng ngủ",
        "start_time": "2024-07-01T21:30:00",
        "end_time": "2024-07-01T22:30:00",
        "icon": "📖",
        "priority": "low",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Tuesday",
        "title": "Ngày vui chơi",
        "description": "Tận hưởng trọn vẹn một ngày vui vẻ.",
        "location": "Không xác định",
        "start_time": "2024-07-02T06:00:00",
        "end_time": "2024-07-02T23:00:00",
        "icon": "🎉",
        "priority": "high",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Wednesday",
        "title": "Tập thể dục buổi sáng",
        "description": "Khởi động ngày mới với bài tập nhẹ nhàng.",
        "location": "Nhà",
        "start_time": "2024-07-03T06:00:00",
        "end_time": "2024-07-03T06:30:00",
        "icon": "🧘‍♀️",
        "priority": "medium",
        "event_category": "habit",
    },
    {
        "DayOfWeek": "Wednesday",
        "title": "Ăn sáng",
        "description": "Bữa sáng chay lành mạnh.",
        "location": "Nhà",
        "start_time": "2024-07-03T06:30:00",
        "end_time": "2024-07-03T07:00:00",
        "icon": "🍽️",
        "priority": "high",
        "event_category": "habit",
    },
    {
        "DayOfWeek": "Wednesday",
        "title": "Học tập",
        "description": "Học các môn quan trọng.",
        "location": "Thư viện",
        "start_time": "2024-07-03T07:00:00",
        "end_time": "2024-07-03T11:00:00",
        "icon": "📚",
        "priority": "high",
        "event_category": "habit",
    },
    {
        "DayOfWeek": "Wednesday",
        "title": "Nghỉ ngơi",
        "description": "Nghỉ ngơi giữa buổi học.",
        "location": "Quán cafe",
        "start_time": "2024-07-03T11:00:00",
        "end_time": "2024-07-03T11:30:00",
        "icon": "☕",
        "priority": "low",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Wednesday",
        "title": "Ăn trưa",
        "description": "Bữa trưa chay.",
        "location": "Nhà",
        "start_time": "2024-07-03T11:30:00",
        "end_time": "2024-07-03T12:30:00",
        "icon": "🍽️",
        "priority": "high",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Wednesday",
        "title": "Làm việc",
        "description": "Giải quyết công việc.",
        "location": "Văn phòng",
        "start_time": "2024-07-03T12:30:00",
        "end_time": "2024-07-03T17:00:00",
        "icon": "💼",
        "priority": "medium",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Wednesday",
        "title": "Nghỉ ngơi",
        "description": "Đi dạo thư giãn.",
        "location": "Công viên",
        "start_time": "2024-07-03T17:00:00",
        "end_time": "2024-07-03T17:30:00",
        "icon": "🚶‍♀️",
        "priority": "low",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Wednesday",
        "title": "Ăn tối",
        "description": "Bữa tối chay nhẹ nhàng.",
        "location": "Nhà",
        "start_time": "2024-07-03T18:30:00",
        "end_time": "2024-07-03T19:30:00",
        "icon": "🍽️",
        "priority": "high",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Wednesday",
        "title": "Đọc sách",
        "description": "Đọc sách trước khi ngủ.",
        "location": "Phòng ngủ",
        "start_time": "2024-07-03T21:30:00",
        "end_time": "2024-07-03T22:30:00",
        "icon": "📖",
        "priority": "low",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Thursday",
        "title": "Tập thể dục buổi sáng",
        "description": "Khởi động ngày mới với bài tập nhẹ nhàng.",
        "location": "Nhà",
        "start_time": "2024-07-04T06:00:00",
        "end_time": "2024-07-04T06:30:00",
        "icon": "🧘‍♀️",
        "priority": "medium",
        "event_category": "habit",
    },
    {
        "DayOfWeek": "Thursday",
        "title": "Ăn sáng",
        "description": "Bữa sáng chay lành mạnh.",
        "location": "Nhà",
        "start_time": "2024-07-04T06:30:00",
        "end_time": "2024-07-04T07:00:00",
        "icon": "🍽️",
        "priority": "high",
        "event_category": "habit",
    },
    {
        "DayOfWeek": "Thursday",
        "title": "Học tập",
        "description": "Học các môn quan trọng.",
        "location": "Thư viện",
        "start_time": "2024-07-04T07:00:00",
        "end_time": "2024-07-04T11:00:00",
        "icon": "📚",
        "priority": "high",
        "event_category": "habit",
    },
    {
        "DayOfWeek": "Thursday",
        "title": "Nghỉ ngơi",
        "description": "Nghỉ ngơi giữa buổi học.",
        "location": "Quán cafe",
        "start_time": "2024-07-04T11:00:00",
        "end_time": "2024-07-04T11:30:00",
        "icon": "☕",
        "priority": "low",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Thursday",
        "title": "Ăn trưa",
        "description": "Bữa trưa chay.",
        "location": "Nhà",
        "start_time": "2024-07-04T11:30:00",
        "end_time": "2024-07-04T12:30:00",
        "icon": "🍽️",
        "priority": "high",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Thursday",
        "title": "Làm việc",
        "description": "Giải quyết công việc.",
        "location": "Văn phòng",
        "start_time": "2024-07-04T12:30:00",
        "end_time": "2024-07-04T17:00:00",
        "icon": "💼",
        "priority": "medium",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Thursday",
        "title": "Nghỉ ngơi",
        "description": "Đi dạo thư giãn.",
        "location": "Công viên",
        "start_time": "2024-07-04T17:00:00",
        "end_time": "2024-07-04T17:30:00",
        "icon": "🚶‍♀️",
        "priority": "low",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Thursday",
        "title": "Ăn tối",
        "description": "Bữa tối chay nhẹ nhàng.",
        "location": "Nhà",
        "start_time": "2024-07-04T18:30:00",
        "end_time": "2024-07-04T19:30:00",
        "icon": "🍽️",
        "priority": "high",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Thursday",
        "title": "Đọc sách",
        "description": "Đọc sách trước khi ngủ.",
        "location": "Phòng ngủ",
        "start_time": "2024-07-04T21:30:00",
        "end_time": "2024-07-04T22:30:00",
        "icon": "📖",
        "priority": "low",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Friday",
        "title": "Tập thể dục buổi sáng",
        "description": "Khởi động ngày mới với bài tập nhẹ nhàng.",
        "location": "Nhà",
        "start_time": "2024-07-05T06:00:00",
        "end_time": "2024-07-05T06:30:00",
        "icon": "🧘‍♀️",
        "priority": "medium",
        "event_category": "habit",
    },
    {
        "DayOfWeek": "Friday",
        "title": "Ăn sáng",
        "description": "Bữa sáng chay lành mạnh.",
        "location": "Nhà",
        "start_time": "2024-07-05T06:30:00",
        "end_time": "2024-07-05T07:00:00",
        "icon": "🍽️",
        "priority": "high",
        "event_category": "habit",
    },
    {
        "DayOfWeek": "Friday",
        "title": "Học tập",
        "description": "Học các môn quan trọng.",
        "location": "Thư viện",
        "start_time": "2024-07-05T07:00:00",
        "end_time": "2024-07-05T11:00:00",
        "icon": "📚",
        "priority": "high",
        "event_category": "habit",
    },
    {
        "DayOfWeek": "Friday",
        "title": "Nghỉ ngơi",
        "description": "Nghỉ ngơi giữa buổi học.",
        "location": "Quán cafe",
        "start_time": "2024-07-05T11:00:00",
        "end_time": "2024-07-05T11:30:00",
        "icon": "☕",
        "priority": "low",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Friday",
        "title": "Ăn trưa",
        "description": "Bữa trưa chay.",
        "location": "Nhà",
        "start_time": "2024-07-05T11:30:00",
        "end_time": "2024-07-05T12:30:00",
        "icon": "🍽️",
        "priority": "high",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Friday",
        "title": "Làm việc",
        "description": "Giải quyết công việc.",
        "location": "Văn phòng",
        "start_time": "2024-07-05T12:30:00",
        "end_time": "2024-07-05T17:00:00",
        "icon": "💼",
        "priority": "medium",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Friday",
        "title": "Nghỉ ngơi",
        "description": "Đi dạo thư giãn.",
        "location": "Công viên",
        "start_time": "2024-07-05T17:00:00",
        "end_time": "2024-07-05T17:30:00",
        "icon": "🚶‍♀️",
        "priority": "low",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Friday",
        "title": "Ăn tối",
        "description": "Bữa tối chay nhẹ nhàng.",
        "location": "Nhà",
        "start_time": "2024-07-05T18:30:00",
        "end_time": "2024-07-05T19:30:00",
        "icon": "🍽️",
        "priority": "high",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Friday",
        "title": "Đọc sách",
        "description": "Đọc sách trước khi ngủ.",
        "location": "Phòng ngủ",
        "start_time": "2024-07-05T21:30:00",
        "end_time": "2024-07-05T22:30:00",
        "icon": "📖",
        "priority": "low",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Saturday",
        "title": "Tập thể dục nhẹ nhàng",
        "description": "Yoga hoặc đi bộ.",
        "location": "Công viên",
        "start_time": "2024-07-06T07:00:00",
        "end_time": "2024-07-06T07:30:00",
        "icon": "🚶‍♀️",
        "priority": "low",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Saturday",
        "title": "Ăn sáng",
        "description": "Bữa sáng chay.",
        "location": "Nhà",
        "start_time": "2024-07-06T07:30:00",
        "end_time": "2024-07-06T08:30:00",
        "icon": "🍽️",
        "priority": "high",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Saturday",
        "title": "Thư giãn",
        "description": "Xem phim hoặc nghe nhạc.",
        "location": "Nhà",
        "start_time": "2024-07-06T08:30:00",
        "end_time": "2024-07-06T11:30:00",
        "icon": " relaxation",
        "priority": "low",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Saturday",
        "title": "Ăn trưa",
        "description": "Bữa trưa chay.",
        "location": "Nhà",
        "start_time": "2024-07-06T11:30:00",
        "end_time": "2024-07-06T12:30:00",
        "icon": "🍽️",
        "priority": "high",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Saturday",
        "title": "Đi chơi",
        "description": "Gặp gỡ bạn bè.",
        "location": "Quán cafe",
        "start_time": "2024-07-06T14:00:00",
        "end_time": "2024-07-06T17:00:00",
        "icon": "☕",
        "priority": "low",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Saturday",
        "title": "Ăn tối",
        "description": "Bữa tối chay.",
        "location": "Nhà",
        "start_time": "2024-07-06T18:30:00",
        "end_time": "2024-07-06T19:30:00",
        "icon": "🍽️",
        "priority": "high",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Saturday",
        "title": "Đọc sách",
        "description": "Đọc sách trước khi ngủ.",
        "location": "Phòng ngủ",
        "start_time": "2024-07-06T21:30:00",
        "end_time": "2024-07-06T22:30:00",
        "icon": "📖",
        "priority": "low",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Sunday",
        "title": "Tập thể dục nhẹ nhàng",
        "description": "Yoga hoặc đi bộ.",
        "location": "Công viên",
        "start_time": "2024-07-07T07:00:00",
        "end_time": "2024-07-07T07:30:00",
        "icon": "🚶‍♀️",
        "priority": "low",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Sunday",
        "title": "Ăn sáng",
        "description": "Bữa sáng chay.",
        "location": "Nhà",
        "start_time": "2024-07-07T07:30:00",
        "end_time": "2024-07-07T08:30:00",
        "icon": "🍽️",
        "priority": "high",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Sunday",
        "title": "Thư giãn",
        "description": "Xem phim hoặc nghe nhạc.",
        "location": "Nhà",
        "start_time": "2024-07-07T08:30:00",
        "end_time": "2024-07-07T11:30:00",
        "icon": " relaxation",
        "priority": "low",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Sunday",
        "title": "Ăn trưa",
        "description": "Bữa trưa chay.",
        "location": "Nhà",
        "start_time": "2024-07-07T11:30:00",
        "end_time": "2024-07-07T12:30:00",
        "icon": "🍽️",
        "priority": "high",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Sunday",
        "title": "Tổng kết tuần",
        "description": "Xem lại những gì đã làm trong tuần.",
        "location": "Nhà",
        "start_time": "2024-07-07T14:00:00",
        "end_time": "2024-07-07T16:00:00",
        "icon": " reflection",
        "priority": "medium",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Sunday",
        "title": "Ăn tối",
        "description": "Bữa tối chay.",
        "location": "Nhà",
        "start_time": "2024-07-07T18:30:00",
        "end_time": "2024-07-07T19:30:00",
        "icon": "🍽️",
        "priority": "high",
        "event_category": "general",
    },
    {
        "DayOfWeek": "Sunday",
        "title": "Đọc sách",
        "description": "Đọc sách trước khi ngủ.",
        "location": "Phòng ngủ",
        "start_time": "2024-07-07T21:30:00",
        "end_time": "2024-07-07T22:30:00",
        "icon": "📖",
        "priority": "low",
        "event_category": "general",
    },
]


def genarate_habit_summarise(summarize_habits=False):
    print("Generating habit summary...")

    prompt_template = """
        Bạn là một chuyên gia phân tích thói quen hàng ngày của người dùng. Nhiệm vụ của bạn là tóm tắt các thói quen và sở thích của người dùng dựa trên lịch trình hoạt động hàng tuần.
       Dựa trên lịch trình hoạt động hàng tuần sau đây của người dùng, hãy phân tích và trích xuất các nhóm hoạt động chính mà người dùng thường thực hiện, ví dụ như:
            Ăn uống

            Học tập

            Làm việc

            Giải trí (bao gồm đọc sách, xem phim, đi dạo, chơi game...)

            Nghỉ ngơi

            Gặp gỡ bạn bè / hoạt động xã hội

            Tập thể dục / chăm sóc sức khỏe

            Với mỗi nhóm hoạt động, hãy trả về một đối tượng JSON với các thông tin sau:

            "Nhóm hoạt động": tên nhóm

            "Tần suất": số ngày trong tuần xuất hiện (hoặc các ngày cụ thể)

            "Thời điểm ưu tiên": sáng / chiều / tối / linh hoạt

            "Mức độ ưu tiên tổng thể": cao / trung bình / thấp

            "Sở thích tổng quát": thích / không thích / bình thường

            "Ghi chú đặc biệt": nếu có sự khác biệt theo ngày (ví dụ: thích thư giãn nhiều hơn vào cuối tuần, học tập nhiều vào Chủ nhật...)

            Chỉ trả về JSON, không cần giải thích thêm.
            Mục tiêu là giúp hệ thống hiểu thói quen người dùng để tối ưu lịch trình sau này.
        Lịch trình:
        {events}
    """

    prompt = PromptTemplate(input_variables=["events"], template=prompt_template)

    summary_chain = LLMChain(llm=llm, prompt=prompt)
    print("Habit summary generated.")
    return (
        summary_chain.run(events=json.dumps(events, ensure_ascii=False))
        if summarize_habits
        else "No habit summary requested."
    )


tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/LaBSE")
model = AutoModel.from_pretrained("sentence-transformers/LaBSE")


# list[np.ndarray]
# Một danh sách các mảng numpy, mỗi phần tử là 1 np.ndarray (tức một vector embedding ứng với từng câu)
def labse_embed(texts: list[str]) -> list[np.ndarray]:
    inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
    # return_tensors="pt"
    # Yêu cầu tokenizer trả về kết quả ở dạng tensor PyTorch (pt = PyTorch).
    # padding=True
    # Đảm bảo rằng tất cả các câu được padding (thêm 0) để có cùng độ dài — điều này cần thiết khi xử lý hàng loạt dữ liệu (batch).
    # truncation=True
    # Nếu một câu quá dài (quá giới hạn token của mô hình, ví dụ 512 token), thì câu sẽ bị cắt ngắn lại.
    # Điều này giúp tránh lỗi khi đưa vào mô hình.

    with torch.no_grad():
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state[:, 0, :]
        embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
    # with torch.no_grad():
    # Đây là cú pháp PyTorch để tắt tính toán gradient trong phần này.
    # Gradient chỉ cần khi bạn huấn luyện mô hình.
    # Ở đây bạn chỉ lấy embedding (đặc trưng) từ mô hình nên không cần gradient, làm vậy tiết kiệm bộ nhớ và tăng tốc.
    # ----------
    # outputs = model(**inputs)
    # model là mô hình (ví dụ LaBSE hoặc BERT).
    # inputs là tensor đầu vào (đã được tokenizer chuẩn bị).
    # outputs chứa kết quả của mô hình, thông thường có nhiều thông tin như:
    # last_hidden_state: tensor kích thước (batch_size, seq_len, hidden_size) — đại diện các vector ẩn cho từng token trong câu.
    # Có thể có pooler_output hoặc các thành phần khác tùy mô hình.
    # ----------
    # embeddings = outputs.last_hidden_state[:, 0, :]
    # outputs.last_hidden_state có shape (batch_size, seq_len, hidden_size).
    # [:, 0, :] chọn token đầu tiên của mỗi câu trong batch, token này thường là token [CLS] trong BERT — được xem là đại diện cho toàn bộ câu.
    # embeddings có shape (batch_size, hidden_size) — vector embedding cho từng câu.
    # ----------
    # Chuẩn hóa embedding theo chuẩn L2 (chuẩn Euclid), nghĩa là:
    # Mục đích: giúp embedding có độ dài bằng 1, chuẩn hóa vector để dễ so sánh (ví dụ cosine similarity).
    return embeddings.cpu().numpy()
    # embeddings hiện tại ở thiết bị (device) GPU nếu có, nên ta chuyển về CPU bằng .cpu().
    # .numpy() chuyển tensor PyTorch thành mảng NumPy, tiện cho xử lý hoặc lưu trữ.


def emberding_rag(state: State):
    documents = []
    response = genarate_habit_summarise(summarize_habits=True)
    cleanedResult = response.replace("```json", "").replace("```", "").strip()
    habit_summaries = json.loads(cleanedResult)

    for habit in habit_summaries:
        doc = Document(
            page_content=json.dumps(habit, ensure_ascii=False),
            metadata={"source": "habit_summaries"},
        )
        documents.append(doc)

    # Tạo text_embeddings đúng format
    texts = [doc.page_content for doc in documents]
    embeddings = labse_embed(texts)
    text_embeddings = list(zip(texts, embeddings))

    # ✅ Gọi FAISS đúng cách
    vectorstore = FAISS.from_embeddings(text_embeddings, documents)
    vectorstore.save_local("./faiss_index")

    state["messages"].append(
        {
            "role": "assistant",
            "content": habit_summaries,
        }
    )
    return state
