from pydantic import BaseModel, Field
from typing import Optional


class CreateAppointment(BaseModel):
    title: str = Field(..., description="Title of the appointment")
    start_time: str = Field(..., description="Start time of the appointment")
    end_time: str = Field(..., description="End time of the appointment")
    customer_name: str = Field(..., description="Name of the customer")
    customer_email: str = Field(..., description="Email of the customer")


class ListAppointments(BaseModel):
    pass


class UpdateAppointment(BaseModel):
    appointment_id: str = Field(..., description="ID of the appointment")
    title: Optional[str] = Field(None, description="Title of the appointment")
    start_time: Optional[str] = Field(None, description="Start time of the appointment")
    end_time: Optional[str] = Field(None, description="End time of the appointment")
    customer_name: Optional[str] = Field(None, description="Name of the customer")
    customer_email: Optional[str] = Field(None, description="Email of the customer")
