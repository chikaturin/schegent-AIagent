import json
import re


def convert_json(response: str):
    if not response or not response.strip():
        raise ValueError("Empty response. Cannot parse JSON.")

    # Bỏ markdown nếu có
    cleaned = response.replace("```json", "").replace("```", "").strip()

    # Cố gắng tìm mảng [] hoặc object {} hợp lệ
    match = re.search(r"(\[.*\]|\{.*\})", cleaned, re.DOTALL)
    if not match:
        raise ValueError("No valid JSON object found in response.")

    json_str = match.group(1)

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print("❌ JSON decoding failed with:", e)
        print("⛔ Raw content received:\n", repr(json_str))
        raise e
