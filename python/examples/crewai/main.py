import os
from dotenv import load_dotenv

from crewai import Agent, Task, Crew
from appointy_agent_toolkit.toolkit import AppointyAgentToolkit

load_dotenv()

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

appointy_agent = Agent(
    role="Appointy Agent",
    goal="Integrate with Appointy effectively to support our business.",
    backstory="You have been using Appointy forever.",
    tools=[*appointy_agent_toolkit.get_tools()],
    allow_delegation=False,
    verbose=True,
)

haiku_writer = Agent(
    role="Haiku writer",
    goal="Write a haiku",
    backstory="You are really good at writing haikus.",
    allow_delegation=False,
    verbose=True,
)

create_appointment = Task(
    description="Create an appointment for a new customer called 'test' "
    "with a start time of '2023-10-01T10:00:00Z' and end time of '2023-10-01T11:00:00Z'. "
    "The description should be a haiku",
    expected_output="appointment_id",
    agent=appointy_agent,
)

write_haiku = Task(
    description="Write a haiku about scheduling appointments.",
    expected_output="haiku",
    agent=haiku_writer,
)

crew = Crew(
    agents=[appointy_agent, haiku_writer],
    tasks=[create_appointment, write_haiku],
    verbose=True,
    planning=True,
)

crew.kickoff()
