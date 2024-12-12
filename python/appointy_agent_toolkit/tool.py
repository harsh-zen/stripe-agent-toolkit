"""
This tool allows agents to interact with the Appointy API.
"""

from __future__ import annotations

from typing import Any, Optional, Type
from pydantic import BaseModel

from crewai_tools import BaseTool

from ..api import AppointyAPI


class AppointyTool(BaseTool):
    """Tool for interacting with the Appointy API."""

    appointy_api: AppointyAPI
    method: str
    name: str = ""
    description: str = ""
    args_schema: Optional[Type[BaseModel]] = None

    def _run(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        """Use the Appointy API to run an operation."""
        return self.appointy_api.run(self.method, *args, **kwargs)
