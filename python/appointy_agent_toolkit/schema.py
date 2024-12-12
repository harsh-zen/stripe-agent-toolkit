from pydantic import BaseModel
from typing import Optional


class CreateAppointment(BaseModel):
    title: str
    start_time: str
    end_time: str
    customer_name: str
    customer_email: str


class ListAppointments(BaseModel):
    pass


class UpdateAppointment(BaseModel):
    appointment_id: str
    title: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
