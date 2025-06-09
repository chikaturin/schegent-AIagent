from agents.tool.interface.index import State


def cancel_schedule(state: State):
    state["messages"].append({"role": "assistant", "content": "Lịch trình đã bị huỷ."})
    state["message_type"] = "cancel"
    return state
