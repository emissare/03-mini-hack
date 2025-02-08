from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import START, StateGraph, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv() 

api_key = os.getenv("API_KEY")
client = OpenAI(api_key=api_key)


def add(a: int, b: int) -> int:
    """Adds a and b.

    Args:
        a: first int
        b: second int
    """
    return a + b

tools = [add]

llm = ChatOpenAI(
    model="o3-mini",
    max_tokens=None,
    max_retries=6,
    stop=None,
    api_key=api_key
)

llm_with_tools = llm.bind_tools(tools)

sys_msg = SystemMessage(content="""You are an advanced Python developer.
                        You have access to Stack Overflow community rated Questions and Answers on issues with using the Python programming language. 
                        You have answers rated 5 + and the top questions scored 10 +. You have 68,248 Question and Answer pairs. 
                        You will ask the user for a Python question, including any clarifying questions required to get enough information to answer the question effectively. 
                        You'll prioritize your dataset, if the answer is not included in your stack overflow data, try to help the user refine their question based on the given question set.""")

def python_developer(state: MessagesState):
   return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

builder = StateGraph(MessagesState)
builder.add_node("python_developer", python_developer)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "python_developer")
builder.add_conditional_edges(
    "python_developer",
    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
    tools_condition,
)
builder.add_edge("tools", "python_developer")

graph = builder.compile()