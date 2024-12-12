import os
from dotenv import load_dotenv

from langchain import hub
from langchain_openai import ChatOpenAI

from langgraph.prebuilt import create_react_agent

from appointy_agent_toolkit.toolkit import AppointyAgentToolkit

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o",
)

appointy_agent_toolkit = AppointyAgentToolkit(
    api_key=os.getenv("APPOINTY_API_KEY"),
    configuration={
        "actions": {
            "appointments": {
                "create": True,
                "update": True,
                "read": True,
            },
        }
    },
)

tools = []
tools.extend(appointy_agent_toolkit.get_tools())

langgraph_agent_executor = create_react_agent(llm, tools)

input_state = {
    "messages": """
        Create an appointment for a new customer called 'test' with a start time
        of '2023-10-01T10:00:00Z' and end time of '2023-10-01T11:00:00Z'.
        The description should be a haiku about scheduling appointments.
    """,
}

output_state = langgraph_agent_executor.invoke(input_state)

print(output_state["messages"][-1].content)
