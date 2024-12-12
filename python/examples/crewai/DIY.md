# DIY: Creating an Agent Toolkit for AppointyAPIs in Python

This guide will walk you through the process of creating an agent toolkit for AppointyAPIs in Python, using the existing Stripe toolkit as a reference.

## Step 1: Set Up Your Project

1. Create a new directory for your project.
2. Set up a virtual environment and activate it:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install the necessary dependencies:
   ```sh
   pip install pydantic requests
   ```

## Step 2: Create the Core Implementation Files

### 2.1 `api.py`

Create a file named `api.py` in your project directory. This file will contain the `AppointyAPI` class to interact with Appointy APIs.

```python
from pydantic import BaseModel
from typing import Optional
import json

class AppointyAPI(BaseModel):
    api_key: str

    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = api_key

    def create_appointment(self, title: str, start_time: str, end_time: str, customer_name: str, customer_email: str) -> dict:
        # Implement the logic to create an appointment using Appointy API
        pass

    def list_appointments(self) -> list:
        # Implement the logic to list appointments using Appointy API
        pass

    def update_appointment(self, appointment_id: str, title: Optional[str] = None, start_time: Optional[str] = None, end_time: Optional[str] = None, customer_name: Optional[str] = None, customer_email: Optional[str] = None) -> dict:
        # Implement the logic to update an appointment using Appointy API
        pass
```

### 2.2 `tool.py`

Create a file named `tool.py` in your project directory. This file will contain the `AppointyTool` class for interacting with Appointy APIs.

```python
from pydantic import BaseModel
from typing import Any, Optional, Type

class AppointyTool(BaseModel):
    appointy_api: AppointyAPI
    method: str
    name: str = ""
    description: str = ""
    args_schema: Optional[Type[BaseModel]] = None

    def run(self, *args: Any, **kwargs: Any) -> str:
        return self.appointy_api.run(self.method, *args, **kwargs)
```

### 2.3 `toolkit.py`

Create a file named `toolkit.py` in your project directory. This file will contain the `AppointyAgentToolkit` class to manage Appointy tools.

```python
from typing import List, Optional
from pydantic import BaseModel

class AppointyAgentToolkit(BaseModel):
    api_key: str
    tools: List[AppointyTool] = []

    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = api_key
        self.tools = self._initialize_tools()

    def _initialize_tools(self) -> List[AppointyTool]:
        # Initialize the tools with the appropriate methods and descriptions
        pass

    def get_tools(self) -> List[AppointyTool]:
        return self.tools
```

### 2.4 `functions.py`

Create a file named `functions.py` in your project directory. This file will contain functions for creating, listing, and updating appointments.

```python
import requests
from typing import Optional

def create_appointment(api_key: str, title: str, start_time: str, end_time: str, customer_name: str, customer_email: str) -> dict:
    # Implement the logic to create an appointment using Appointy API
    pass

def list_appointments(api_key: str) -> list:
    # Implement the logic to list appointments using Appointy API
    pass

def update_appointment(api_key: str, appointment_id: str, title: Optional[str] = None, start_time: Optional[str] = None, end_time: Optional[str] = None, customer_name: Optional[str] = None, customer_email: Optional[str] = None) -> dict:
    # Implement the logic to update an appointment using Appointy API
    pass
```

### 2.5 `configuration.py`

Create a file named `configuration.py` in your project directory. This file will contain configuration classes for the Appointy toolkit.

```python
from typing import Optional
from pydantic import BaseModel

class Context(BaseModel):
    api_base_url: Optional[str] = "https://api.appointy.com"
    api_key: Optional[str] = None

class Actions(BaseModel):
    create: Optional[bool] = False
    update: Optional[bool] = False
    read: Optional[bool] = False

class Configuration(BaseModel):
    actions: Optional[Actions] = Actions()
    context: Optional[Context] = Context()
```

### 2.6 `prompts.py`

Create a file named `prompts.py` in your project directory. This file will contain prompt messages for Appointy tools.

```python
CREATE_APPOINTMENT_PROMPT = """
This tool will create an appointment in Appointy.

It takes the following arguments:
- title (str): The title of the appointment.
- start_time (str): The start time of the appointment.
- end_time (str): The end time of the appointment.
- customer_name (str): The name of the customer.
- customer_email (str): The email address of the customer.
"""

LIST_APPOINTMENTS_PROMPT = """
This tool will list appointments in Appointy.

It takes no input.
"""

UPDATE_APPOINTMENT_PROMPT = """
This tool will update an appointment in Appointy.

It takes the following arguments:
- appointment_id (str): The ID of the appointment.
- title (str, optional): The title of the appointment.
- start_time (str, optional): The start time of the appointment.
- end_time (str, optional): The end time of the appointment.
- customer_name (str, optional): The name of the customer.
- customer_email (str, optional): The email address of the customer.
"""
```

## Step 3: Create Example Usage Files

### 3.1 CrewAI Example

Create a file named `crewai_example.py` in your project directory. This file will demonstrate how to use the AppointyAPI toolkit with CrewAI.

```python
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
```

### 3.2 LangChain Example

Create a file named `langchain_example.py` in your project directory. This file will demonstrate how to use the AppointyAPI toolkit with LangChain.

```python
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
```

## Step 4: Update README

Update your project's `README.md` file to include installation and usage instructions for the Appointy toolkit, similar to the existing Stripe toolkit instructions.

```markdown
# Appointy Agent Toolkit - Python

The Appointy Agent Toolkit library enables popular agent frameworks including LangChain and CrewAI to integrate with Appointy APIs through function calling. The
library is not exhaustive of the entire Appointy API. It is built directly on top
of the [Appointy API Documentation][appointy-api-docs].

## Installation

You don't need this source code unless you want to modify the package. If you just
want to use the package, just run:

```sh
pip install appointy-agent-toolkit
```

### Requirements

- Python 3.11+

## Usage

The library needs to be configured with your account's API key which is
available in your [Appointy Dashboard][api-keys].

```python
from appointy_agent_toolkit.toolkit import AppointyAgentToolkit

appointy_agent_toolkit = AppointyAgentToolkit(
    api_key="your_api_key",
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
```

The toolkit works with LangChain and CrewAI and can be passed as a list of tools. For example:

```python
from crewai import Agent

appointy_agent = Agent(
    role="Appointy Agent",
    goal="Integrate with Appointy",
    backstory="You are an expert at integrating with Appointy",
    tools=[*appointy_agent_toolkit.get_tools()]
)
```

Examples for LangChain and CrewAI are included in `/examples`.

[appointy-api-docs]: https://docs.appointy.com
[api-keys]: https://dashboard.appointy.com/account/apikeys

#### Context

In some cases you will want to provide values that serve as defaults when making requests. Currently, the `account` context value enables you to make API calls for your [connected accounts](https://docs.appointy.com/connect/authentication).

```python
appointy_agent_toolkit = AppointyAgentToolkit(
    api_key="your_api_key",
    configuration={
        "context": {
            "account": "acct_123"
        }
    }
)
```

## Development

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
```

## Conclusion

By following these steps, you have successfully created an agent toolkit for AppointyAPIs in Python. You can now use this toolkit to integrate Appointy APIs with popular agent frameworks like LangChain and CrewAI.
