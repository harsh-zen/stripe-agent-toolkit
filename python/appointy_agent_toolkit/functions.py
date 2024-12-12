import requests
from typing import Optional
from pydantic import BaseModel
from .configuration import Context


class Appointment(BaseModel):
    id: str
    title: str
    start_time: str
    end_time: str
    customer_name: str
    customer_email: str


def create_appointment(
    context: Context,
    title: str,
    start_time: str,
    end_time: str,
    customer_name: str,
    customer_email: str,
) -> Appointment:
    """
    Create an appointment.

    Parameters:
        title (str): The title of the appointment.
        start_time (str): The start time of the appointment.
        end_time (str): The end time of the appointment.
        customer_name (str): The name of the customer.
        customer_email (str): The email address of the customer.

    Returns:
        Appointment: The created appointment.
    """
    appointment_data = {
        "title": title,
        "start_time": start_time,
        "end_time": end_time,
        "customer_name": customer_name,
        "customer_email": customer_email,
    }

    response = requests.post(
        f"{context.api_base_url}/appointments",
        headers={"Authorization": f"Bearer {context.api_key}"},
        json=appointment_data,
    )
    response.raise_for_status()
    return Appointment(**response.json())


def list_appointments(context: Context) -> list[Appointment]:
    """
    List appointments.

    Returns:
        list[Appointment]: A list of appointments.
    """
    response = requests.get(
        f"{context.api_base_url}/appointments",
        headers={"Authorization": f"Bearer {context.api_key}"},
    )
    response.raise_for_status()
    return [Appointment(**appointment) for appointment in response.json()]


def update_appointment(
    context: Context,
    appointment_id: str,
    title: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    customer_name: Optional[str] = None,
    customer_email: Optional[str] = None,
) -> Appointment:
    """
    Update an appointment.

    Parameters:
        appointment_id (str): The ID of the appointment.
        title (str, optional): The title of the appointment.
        start_time (str, optional): The start time of the appointment.
        end_time (str, optional): The end time of the appointment.
        customer_name (str, optional): The name of the customer.
        customer_email (str, optional): The email address of the customer.

    Returns:
        Appointment: The updated appointment.
    """
    appointment_data = {
        "title": title,
        "start_time": start_time,
        "end_time": end_time,
        "customer_name": customer_name,
        "customer_email": customer_email,
    }
    appointment_data = {k: v for k, v in appointment_data.items() if v is not None}

    response = requests.put(
        f"{context.api_base_url}/appointments/{appointment_id}",
        headers={"Authorization": f"Bearer {context.api_key}"},
        json=appointment_data,
    )
    response.raise_for_status()
    return Appointment(**response.json())
