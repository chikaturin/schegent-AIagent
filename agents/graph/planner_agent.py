from langgraph.graph import StateGraph, START, END
from agents.tool.interface.index import State
from agents.tool.common.classify_messages import classify_message
from agents.tool.common.router_agent import router
from agents.tool.agent_schedule.create_schedule import create_new_schedule
from agents.tool.agent_schedule.update_schedule import update_schedule
from agents.tool.agent_schedule.create_new_task import create_new_task
from agents.tool.accept_unaccept.accept import accept_schedule
from agents.tool.accept_unaccept.unaccept import unaccept_schedule
from agents.tool.rag.emberding_habit import emberding_rag


# ⛔ Node xử lý khi người dùng cancel lịch
def cancel_schedule(state):
    state["messages"].append({"role": "assistant", "content": "Lịch trình đã bị huỷ."})
    state["message_type"] = "cancel"
    state["next"] = None
    return state


# ✅ Node xử lý phản hồi từ user (accept/cancel)
def handle_pending_response(state):
    user_input = state["messages"][-1]["content"].strip().lower()

    if user_input in ["accept", "ok", "đồng ý", "lưu"]:
        state["next"] = "accept_schedule"
    elif user_input in ["cancel", "hủy", "huỷ", "không"]:
        state["next"] = "cancel"
    else:
        state["messages"].append(
            {
                "role": "assistant",
                "content": "Vui lòng trả lời 'accept' để lưu hoặc 'cancel' để huỷ lịch trình.",
            }
        )
        state["next"] = None
    return state


# ✅ Tạo graph
graph_builder = StateGraph(State)

# Thêm các node
graph_builder.add_node("classifier", classify_message)
graph_builder.add_node("router", router)
graph_builder.add_node("create_new_schedule", create_new_schedule)
graph_builder.add_node("create_new_task", create_new_task)
graph_builder.add_node("update_schedule", update_schedule)
graph_builder.add_node("accept_schedule", accept_schedule)
graph_builder.add_node("unaccept_schedule", unaccept_schedule)
graph_builder.add_node("emberding_rag", emberding_rag)
graph_builder.add_node("cancel", cancel_schedule)
graph_builder.add_node("handle_pending_response", handle_pending_response)

# ✅ Điều hướng START tùy theo message_type
graph_builder.add_conditional_edges(
    START,
    lambda state: state.get("message_type") if state.get("message_type") else "new",
    {
        "new": "classifier",  # luồng xử lý message mới
        "pending_schedule": "handle_pending_response",  # xử lý phản hồi accept/cancel
    },
)

# ✅ classifier → router
graph_builder.add_edge("classifier", "router")

# ✅ router → các tác vụ
graph_builder.add_conditional_edges(
    "router",
    lambda state: state.get("next") if state.get("next") else "cancel",
    {
        "create_new_schedule": "create_new_schedule",
        "update_schedule": "update_schedule",
        "create_new_task": "create_new_task",
    },
)

# ✅ create_new_schedule → chờ phản hồi accept/cancel
graph_builder.add_conditional_edges(
    "create_new_schedule",
    lambda state: state.get("next") if state.get("next") else "cancel",
    {
        "accept_schedule": "accept_schedule",
        "create_new_schedule": "create_new_schedule",
        "cancel": "cancel",
    },
)

# ✅ handle phản hồi từ người dùng
graph_builder.add_conditional_edges(
    "handle_pending_response",
    lambda state: state.get("next") if state.get("next") else "cancel",
    {
        "accept_schedule": "accept_schedule",
        "cancel": "cancel",
    },
)

# ✅ Các edge bình thường
graph_builder.add_edge("create_new_task", "update_schedule")
graph_builder.add_edge("accept_schedule", "emberding_rag")
graph_builder.add_edge("update_schedule", END)
graph_builder.add_edge("emberding_rag", END)
graph_builder.add_edge("cancel", END)

# ✅ Biên dịch graph
graph = graph_builder.compile()
