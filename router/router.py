from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Literal
import json

from agents.graph.planner_agent import graph
from agents.tool.Data.receive_questions import save_habitat

router = APIRouter()


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class QueryRequest(BaseModel):
    Message: str


class QueryResponse(BaseModel):
    messages: List[Message]


@router.post("/chat", response_model=QueryResponse, tags=["Chat"])
def run_chatbot(request: QueryRequest):
    state = {
        "messages": [{"role": "user", "content": request.Message}],
        "message_type": None,
    }

    state = graph.invoke(state)

    if state.get("messages") and len(state["messages"]) > 0:
        assistant_content = next(
            (
                msg["content"]
                for msg in reversed(state["messages"])
                if msg["role"] == "assistant"
            ),
            None,
        )
        print(f"Assistant raw output: {assistant_content}")
        if assistant_content and assistant_content.startswith("```json"):
            cleanedResult = (
                assistant_content.replace("```json", "").replace("```", "").strip()
            )
            try:
                json_result = json.loads(cleanedResult)
                return json_result
            except json.JSONDecodeError:
                pass
        return {
            "messages": [
                {
                    "role": "assistant",
                    "content": assistant_content
                    or "Xin lỗi, tôi không thể xử lý yêu cầu này.",
                }
            ]
        }


@router.get("/save_habitat", tags=["Habitat"])
def save_habitat_endpoint():
    try:
        save_habitat()
        return {"message": "Habitat saved successfully."}
    except Exception as e:
        return {"error": str(e)}
