from dotenv import load_dotenv
from typing import Annotated, Literal
from config.llm import llm
from pydantic import BaseModel, Field
from agents.tool.interface.index import State

load_dotenv()


class MessageClassifier(BaseModel):
    message_type: Literal[
        "create_new_schedule",
        "create_new_task",
        "update_schedule",
        "accept_schedule",
        "unaccept_schedule",
    ] = Field(
        ...,
        description="Classify if the message requires an action related to scheduling or task management (e.g., creating a new schedule, creating a new task, or updating an existing schedule).",
    )


def classify_message(state: State):
    print("Classifying message type...")
    last_message = state["messages"][-1]
    classifier_llm = llm.with_structured_output(MessageClassifier)

    result = classifier_llm.invoke(
        [
            {
                "role": "system",
                "content": """Classify the user message into one of these categories:
                    - 'create_new_schedule': if the message is about creating a new schedule or calendar event.
                    - 'create_new_task': if the message is about creating a new task or to-do item.
                    - 'update_schedule': if the message is about updating or modifying an existing schedule or event.
                    - 'accept_schedule': if the message is about accepting a proposed schedule.
                    - 'unaccept_schedule': if the message is about rejecting or unaccepting a proposed schedule.
                    Only respond with one of these exact labels.""",
            },
            {"role": "user", "content": last_message["content"]},
        ]
    )
    return {"message_type": result.message_type}
