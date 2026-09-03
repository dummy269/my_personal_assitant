import os
from typing import TypedDict

from dotenv import load_dotenv
from langgraph.graph import END, START, StateGraph
from openai import OpenAI

from src.agent import search_pdf


class AdvancedState(TypedDict, total=False):
    question: str
    plan: str
    research: str
    draft: str
    verified: bool
    answer: str


def ask_llm(instructions: str, content: str) -> str:
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set in .env")
    response = OpenAI().responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        instructions=instructions,
        input=content,
    )
    return response.output_text


def build_advanced_graph(collection, checkpointer=None):
    def planner(state: AdvancedState) -> dict:
        plan = ask_llm(
            "Create a short research plan for answering the user's question. "
            "Return only the steps.",
            state["question"],
        )
        return {"plan": plan}

    def researcher(state: AdvancedState) -> dict:
        research = search_pdf(collection, state["question"])
        return {"research": research}

    def verifier(state: AdvancedState) -> dict:
        result = ask_llm(
            "Decide whether the research supports an answer to the question. "
            "Reply with only YES or NO.",
            f"Question: {state['question']}\nResearch:\n{state['research']}",
        )
        return {"verified": result.strip().upper().startswith("YES")}

    def final_answer(state: AdvancedState) -> dict:
        answer = ask_llm(
            "Answer using only the research. If it is insufficient, say you do not know.",
            f"Question: {state['question']}\nResearch:\n{state['research']}",
        )
        return {"draft": answer, "answer": answer}

    def no_answer(state: AdvancedState) -> dict:
        return {"answer": "I do not have enough evidence to answer that."}

    def route_after_verifier(state: AdvancedState) -> str:
        return "final_answer" if state["verified"] else "no_answer"

    graph = StateGraph(AdvancedState)
    graph.add_node("planner", planner)
    graph.add_node("researcher", researcher)
    graph.add_node("verifier", verifier)
    graph.add_node("final_answer", final_answer)
    graph.add_node("no_answer", no_answer)
    graph.add_edge(START, "planner")
    graph.add_edge("planner", "researcher")
    graph.add_edge("researcher", "verifier")
    graph.add_conditional_edges(
        "verifier", route_after_verifier, ["final_answer", "no_answer"]
    )
    graph.add_edge("final_answer", END)
    graph.add_edge("no_answer", END)
    return graph.compile(checkpointer=checkpointer)