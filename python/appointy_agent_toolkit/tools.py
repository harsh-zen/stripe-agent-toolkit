from typing import Dict, List

from .prompts import (
    CREATE_APPOINTMENT_PROMPT,
    LIST_APPOINTMENTS_PROMPT,
    UPDATE_APPOINTMENT_PROMPT,
    LIST_SERVICES_PROMPT,
    GET_STAFF_INFO_PROMPT,
    GET_SERVICE_INFO_PROMPT,
    GET_AVAILABLE_DATES_PROMPT,
    GET_AVAILABLE_SLOTS_PROMPT,
    GENERATE_BOOKING_LINK_PROMPT,
)

from .schema import (
    CreateAppointment,
    ListAppointments,
    UpdateAppointment,
    ListServices,
    GetStaffInfo,
    GetServiceInfo,
    GetAvailableDates,
    GetAvailableSlots,
    GenerateBookingLink,
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
    {
        "method": "list_services",
        "name": "List Services",
        "description": LIST_SERVICES_PROMPT,
        "args_schema": ListServices,
        "actions": {
            "services": {
                "read": True,
            }
        },
    },
    {
        "method": "get_staff_info",
        "name": "Get Staff Info",
        "description": GET_STAFF_INFO_PROMPT,
        "args_schema": GetStaffInfo,
        "actions": {
            "staff": {
                "read": True,
            }
        },
    },
    {
        "method": "get_service_info",
        "name": "Get Service Info",
        "description": GET_SERVICE_INFO_PROMPT,
        "args_schema": GetServiceInfo,
        "actions": {
            "services": {
                "read": True,
            }
        },
    },
    {
        "method": "get_available_dates",
        "name": "Get Available Dates",
        "description": GET_AVAILABLE_DATES_PROMPT,
        "args_schema": GetAvailableDates,
        "actions": {
            "availability": {
                "read": True,
            }
        },
    },
    {
        "method": "get_available_slots",
        "name": "Get Available Slots",
        "description": GET_AVAILABLE_SLOTS_PROMPT,
        "args_schema": GetAvailableSlots,
        "actions": {
            "availability": {
                "read": True,
            }
        },
    },
    {
        "method": "generate_booking_link",
        "name": "Generate Booking Link",
        "description": GENERATE_BOOKING_LINK_PROMPT,
        "args_schema": GenerateBookingLink,
        "actions": {
            "booking": {
                "create": True,
            }
        },
    },
]
