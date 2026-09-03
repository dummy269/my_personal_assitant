import ast
import json
import operator
import os

from dotenv import load_dotenv
from openai import OpenAI

from src.basic_rag import search


def search_pdf(collection, question: str) -> str:
    results = search(collection, question)
    return "\n\n".join(
        f"Source: {result['source']}\n{result['text']}" for result in results
    )


def calculator(expression: str) -> str:
    operations = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
    }

    def evaluate(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.UnaryOp) and type(node.op) in operations:
            return operations[type(node.op)](evaluate(node.operand))
        if isinstance(node, ast.BinOp) and type(node.op) in operations:
            return operations[type(node.op)](evaluate(node.left), evaluate(node.right))
        raise ValueError("Only basic arithmetic is allowed")

    return str(evaluate(ast.parse(expression, mode="eval").body))


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_pdf",
            "description": "Search personal PDF documents for relevant information.",
            "parameters": {
                "type": "object",
                "properties": {"question": {"type": "string"}},
                "required": ["question"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Calculate a basic arithmetic expression.",
            "parameters": {
                "type": "object",
                "properties": {"expression": {"type": "string"}},
                "required": ["expression"],
            },
        },
    },
]


def run_agent(collection, question: str) -> str:
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set in .env")

    client = OpenAI()
    messages = [{"role": "user", "content": question}]

    for _ in range(3):
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=messages,
            tools=TOOLS,
        )
        message = response.choices[0].message
        messages.append(message.model_dump())

        if not message.tool_calls:
            return message.content or "No answer returned."

        for tool_call in message.tool_calls:
            arguments = json.loads(tool_call.function.arguments)
            if tool_call.function.name == "search_pdf":
                result = search_pdf(collection, arguments["question"])
            else:
                result = calculator(arguments["expression"])
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                }
            )

    raise RuntimeError("Agent exceeded the maximum number of tool calls")