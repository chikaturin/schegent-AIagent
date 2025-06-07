from typing_extensions import TypedDict


class State(TypedDict):
    messages: list
    message_type: str | None
