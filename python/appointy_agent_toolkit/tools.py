from typing import Dict, List

from .prompts import (
    CREATE_APPOINTMENT_PROMPT,
    LIST_APPOINTMENTS_PROMPT,
    UPDATE_APPOINTMENT_PROMPT,
)

from .schema import (
    CreateAppointment,
    ListAppointments,
    UpdateAppointment,
)

tools: List[Dict] = [
    {
        "method": "create_appointment",
        "name": "Create Appointment",
        "description": CREATE_APPOINTMENT_PROMPT,
        "args_schema": CreateAppointment,
        "actions": {
            "appointments": {
                "create": True,
            }
        },
    },
    {
        "method": "list_appointments",
        "name": "List Appointments",
        "description": LIST_APPOINTMENTS_PROMPT,
        "args_schema": ListAppointments,
        "actions": {
            "appointments": {
                "read": True,
            }
        },
    },
    {
        "method": "update_appointment",
        "name": "Update Appointment",
        "description": UPDATE_APPOINTMENT_PROMPT,
        "args_schema": UpdateAppointment,
        "actions": {
            "appointments": {
                "update": True,
            }
        },
    },
]
