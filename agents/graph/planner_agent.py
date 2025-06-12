from langgraph.graph import StateGraph, START, END
from agents.tool.interface.index import State
from agents.tool.common.classify_messages import classify_message
from agents.tool.common.router_agent import router
from agents.tool.agent_schedule.create_schedule import create_new_schedule
from agents.tool.agent_schedule.update_schedule import update_schedule
from agents.tool.accept_unaccept.accept import accept_schedule
from agents.tool.rag.emberding_habit import emberding_rag

graph_builder = StateGraph(State)

graph_builder.add_node("classifier", classify_message)
graph_builder.add_node("router", router)
graph_builder.add_node("create_new_schedule", create_new_schedule)
graph_builder.add_node("update_schedule", update_schedule)
graph_builder.add_node("accept_schedule", accept_schedule)
graph_builder.add_node("emberding_rag", emberding_rag)

graph_builder.add_edge(START, "classifier")
graph_builder.add_edge("classifier", "router")

graph_builder.add_conditional_edges(
    "router",
    lambda state: state.get("next"),
    {
        "create_new_schedule": "create_new_schedule",
        "update_schedule": "update_schedule",
        "accept_schedule": "accept_schedule",
    },
)

graph_builder.add_edge("create_new_schedule", END)
graph_builder.add_edge("update_schedule", END)

graph_builder.add_edge("accept_schedule", "emberding_rag")
graph_builder.add_edge("emberding_rag", END)

graph = graph_builder.compile()
