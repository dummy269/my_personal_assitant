import json
import os
from typing import TypedDict

from dotenv import load_dotenv
from langgraph.graph import END, START, StateGraph
from openai import OpenAI

from src.agent import TOOLS, calculator, search_pdf


class AgentState(TypedDict):
    messages: list[dict]
    collection: object


def agent_node(state: AgentState) -> dict:
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set in .env")

    response = OpenAI().chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=state["messages"],
        tools=TOOLS,
    )
    return {"messages": state["messages"] + [response.choices[0].message.model_dump()]}


def tool_node(state: AgentState) -> dict:
    message = state["messages"][-1]
    tool_messages = []

    for tool_call in message["tool_calls"]:
        arguments = json.loads(tool_call["function"]["arguments"])
        if tool_call["function"]["name"] == "search_pdf":
            result = search_pdf(state["collection"], arguments["question"])
        else:
            result = calculator(arguments["expression"])
        tool_messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "content": result,
            }
        )

    return {"messages": state["messages"] + tool_messages}


def route_after_agent(state: AgentState) -> str:
    return "tools" if state["messages"][-1].get("tool_calls") else END


def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("agent", agent_node)
    graph.add_node("tools", tool_node)
    graph.add_edge(START, "agent")
    graph.add_conditional_edges("agent", route_after_agent, ["tools", END])
    graph.add_edge("tools", "agent")
    return graph.compile()