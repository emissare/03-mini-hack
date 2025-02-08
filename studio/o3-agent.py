from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import START, StateGraph, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode
from openai import OpenAI
import os
from dotenv import load_dotenv
import pandas as pd

df = pd.read_csv("stack-python-answers.csv")

def query_dataframe(query):
    """Query the DataFrame using a structured Pandas filter."""
    try:
        result = df.query(query).to_string(index=False)
        return result if result.strip() else "No matching results found."
    except Exception as e:
        return f"Error processing query: {str(e)}"
    
from langchain.tools import Tool

csv_tool = Tool(
    name="StackOverflow Python QA Lookup",
    description="Queries a dataset of high-scoring Python questions and answers from Stack Overflow.",
    func=query_dataframe
)

load_dotenv() 

api_key = os.getenv("API_KEY")
client = OpenAI(api_key=api_key)

"""def stack_overflow_agent_tool(query: str):
    # Create the agent
    agent = create_pandas_dataframe_agent(llm, df, verbose=True, allow_dangerous_code=True)
    # Run the agent with the provided query
    return agent.run(query)

# Register the function as a tool
stack_overflow_tool = Tool(
    name="Stack Overflow DataFrame Agent",
    func=stack_overflow_agent_tool,
    description="A tool to interact with the Stack Overflow Q&A DataFrame using natural language queries."
)

tools.append(stack_overflow_tool)"""

def add(a: int, b: int) -> int:
    """Adds a and b.

    Args:
        a: first int
        b: second int
    """
    return a + b

tools = [add, query_dataframe]

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