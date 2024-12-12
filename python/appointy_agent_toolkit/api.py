"""Util that calls Appointy."""

from __future__ import annotations

import json
from typing import Optional
from pydantic import BaseModel

from .configuration import Context

from .functions import (
    create_appointment,
    list_appointments,
    update_appointment,
)


class AppointyAPI(BaseModel):
    """Wrapper for Appointy API"""

    _context: Context

    def __init__(self, api_key: str, context: Optional[Context]):
        super().__init__()

        self._context = context if context is not None else Context()

        self.api_key = api_key

    def run(self, method: str, *args, **kwargs) -> str:
        if method == "create_appointment":
            return json.dumps(create_appointment(self._context, *args, **kwargs))
        elif method == "list_appointments":
            return json.dumps(list_appointments(self._context, *args, **kwargs))
        elif method == "update_appointment":
            return json.dumps(update_appointment(self._context, *args, **kwargs))
        else:
            raise ValueError("Invalid method " + method)
