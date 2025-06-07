from agents.tool.interface.index import State


def router(state: State):
    print("Routing based on message type...")
    message_type = state.get("message_type", "accept_schedule").strip()

    if message_type == "create_new_schedule":
        return {"next": "create_new_schedule"}

    elif message_type == "create_new_task":
        return {"next": "create_new_task"}

    elif message_type == "update_schedule":
        return {"next": "update_schedule"}

    else:
        return {"next": "accept_schedule"}
