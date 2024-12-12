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


class ListServices(BaseModel):
    query: Optional[str] = Field(None, description="Query string to filter services")


class GetStaffInfo(BaseModel):
    service_id: str = Field(..., description="ID of the service")
    duration: str = Field(..., description="Duration of the service")


class GetServiceInfo(BaseModel):
    query: str = Field(..., description="Query string to search for service")


class GetAvailableDates(BaseModel):
    filters: dict = Field(..., description="Filters for available dates")
    from_date: str = Field(..., description="Start date for availability search")
    to_date: str = Field(..., description="End date for availability search")


class GetAvailableSlots(BaseModel):
    filters: dict = Field(..., description="Filters for available slots")
    from_date: str = Field(..., description="Start date for availability search")
    to_date: str = Field(..., description="End date for availability search")


class GenerateBookingLink(BaseModel):
    date: str = Field(..., description="Date for the booking")
    time: str = Field(..., description="Time for the booking")
    service_id: str = Field(..., description="ID of the service")
    employee_id: str = Field(..., description="ID of the employee")
