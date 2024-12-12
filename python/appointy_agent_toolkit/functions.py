import requests
from typing import Optional, List, Dict
from pydantic import BaseModel
from .configuration import Context
from datetime import datetime, timedelta
import base64
import json
import logging

logger = logging.getLogger(__name__)


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


def list_services(self, query: str = "") -> List[Dict]:
    """List all services for the business"""
    if not self.config.business_id:
        raise ValueError("Business ID not configured")

    params = {"parent": self.config.business_id}
    data = self._make_request("GET", "/api/v1/services:all", params=params)
    return data.get("services", [])


def get_staff_info(self, service_id: str, duration: str) -> List[str]:
    """Get available staff for a service"""
    if not self.config.business_id:
        raise ValueError("Business ID not configured")

    start_time = datetime.now().isoformat() + "Z"
    end_time = (datetime.now() + timedelta(days=30)).isoformat() + "Z"

    # Convert duration to integer if it ends with 's'
    if isinstance(duration, str) and duration.endswith('s'):
        duration = int(duration[:-1])

    payload = {
        "filter": {
            "timeSlot": {
                "startTime": start_time,
                "endTime": end_time
            },
            "duration": int(duration),  # Ensure duration is an integer
            "parent": self.config.business_id,
            "employees": [],
            "services": [service_id],
            "consumerId": ""
        }
    }

    try:
        data = self._make_request(
            "POST",
            "/api/v1/appointment/availability/improved-services-employees",
            json_data=payload
        )

        logger.debug(f"Staff info response: {data}")
        available_ids = data.get("availableIds", {})

        if not available_ids:
            logger.warning("No available IDs returned from staff info request")
            return []

        if not self._employee_mapping:
            self._employee_mapping = self._fetch_employee_mapping()
            logger.debug(f"Employee mapping: {self._employee_mapping}")

        reverse_lookup = {v: k for k, v in self._employee_mapping.items()}
        available_staff = [reverse_lookup.get(id, f"Unknown ({id})") for id, available in available_ids.items() if available]

        logger.debug(f"Available staff: {available_staff}")
        return available_staff

    except Exception as e:
        logger.error(f"Error getting staff info: {str(e)}")
        return []


def _fetch_employee_mapping(self) -> Dict[str, str]:
    """Fetch employee mapping using GraphQL"""
    group_id, company_id, location_id = self.config.business_id.split("/")

    start_time = datetime.utcnow().isoformat() + "Z"
    end_time = (datetime.utcnow() + timedelta(days=180)).isoformat() + "Z"

    query = """
    query ImprovedAvailableServicesOrEmployeesQuery(
      $filter: AvailabilityFilterInput
      $listEmployees: Boolean!
    ) {
      improvedAvailableServicesOrEmployees(filter: $filter, listEmployees: $listEmployees) {
        availableIds
        errorMessage
      }
    }
    """

    variables = {
        "filter": {
            "timeSlot": {
                "startTime": start_time,
                "endTime": end_time
            },
            "duration": None,
            "parent": self.config.business_id,
            "employees": [],
            "services": [],
            "consumerId": ""
        },
        "listEmployees": True
    }

    payload = {
        "id": "ImprovedAvailableServicesOrEmployeesQuery",
        "query": query,
        "variables": variables
    }

    data = self._make_request("POST", "/graphql", json_data=payload)
    logger.debug(f"Employee mapping response: {data}")

    available_ids_encoded = data.get("data", {}).get("improvedAvailableServicesOrEmployees", {}).get("availableIds", "")
    if not available_ids_encoded:
        return {}

    available_ids_json = base64.b64decode(available_ids_encoded).decode('utf-8')
    available_ids = json.loads(available_ids_json)

    nodes = self._query_employee_nodes(list(available_ids.keys()), group_id)
    employee_nodes = nodes.get("nodes", [])

    mapping = {}
    for node in employee_nodes:
        if node.get("__typename") == "Employee" and node.get("staffProfiles"):
            for profile in node["staffProfiles"]:
                full_name = f"{profile['firstName']} {profile['lastName']}".strip()
                if full_name:
                    mapping[full_name] = node["id"]

    return mapping


def _query_employee_nodes(self, ids: List[str], group_id: str) -> Dict:
    """Query employee nodes using GraphQL"""
    query = """
    query EmployeeNodesQuery($ids: [ID], $groupId: String, $fetchExtraField: Boolean!) {
        nodes(ids: $ids) {
            __typename
            ... on Employee {
                staffProfiles {
                    firstName
                    lastName
                }
            }
            id
        }
    }
    """

    variables = {
        "ids": ids,
        "groupId": group_id,
        "fetchExtraField": False
    }

    payload = {
        "id": "EmployeeNodesQuery",
        "query": query,
        "variables": variables
    }

    return self._make_request("POST", "/graphql", json_data=payload)["data"]


def get_service_info(self, query: str) -> str:
    """Get detailed service information"""
    if not self.config.business_id:
        raise ValueError("Business ID not configured")

    services = self.list_services(query)
    matching_services = [s for s in services if query.lower() in s['title'].lower()]

    if not matching_services:
        return f"No match found for '{query}'."

    if len(matching_services) > 1:
        service_names = [s['title'] for s in matching_services]
        return f"Multiple matches found: {', '.join(service_names)}"

    service_info = matching_services[0]
    logger.debug(f"Service info: {service_info}")

    result = f"Information for {service_info['title']}:\n"
    result += f"Description: {service_info.get('description', 'No description available')}\n"

    # Convert duration from seconds to minutes
    duration_str = str(service_info.get('durations', ['30'])[0])
    try:
        if duration_str.endswith('s'):
            duration_str = duration_str[:-1]  # Remove 's' suffix
        duration_seconds = int(duration_str)
        duration_minutes = duration_seconds // 60
        result += f"Duration: {duration_minutes} minutes\n"
    except (ValueError, TypeError):
        result += f"Duration: {duration_str}\n"

    return result


def get_available_dates(self, filters: Dict, from_date: str, to_date: str) -> List[str]:
    """Get available dates for booking"""
    if not self.config.business_id:
        raise ValueError("Business ID not configured")

    query = """
    query CalendarPageQuery($timezone: String!, $filter: AvailabilityFilterInput) {
        appointmentAvailabilityDates(timezone: $timezone, filter: $filter) {
            available
            datesStatus
            errorMessage
        }
    }
    """

    variables = {
        "filter": {
            "timeSlot": {
                "startTime": from_date,
                "endTime": to_date
            },
            "parent": self.config.business_id,
            "employees": filters.get('employees', []),
            "services": filters.get('services', []),
        },
        "timezone": "UTC"  # TODO: Make configurable
    }

    payload = {
        "query": query,
        "variables": variables
    }

    data = self._make_request("POST", "/graphql", json_data=payload)
    dates_status = data.get("data", {}).get("appointmentAvailabilityDates", {}).get("datesStatus", "")

    if not dates_status:
        return []

    decoded_dates = base64.b64decode(dates_status).decode('utf-8')
    return decoded_dates.split(",")


def get_available_slots(self, filters: Dict, from_date: str, to_date: str) -> List[str]:
    """Get available time slots for booking"""
    if not self.config.business_id:
        raise ValueError("Business ID not configured")

    query = """
    query CalendarPageQuery($timezone: String!, $filter: AvailabilityFilterInput) {
        improvedAppointmentAvailability(filter: $filter) {
            errorMessage
            slots {
                slotType
                slot {
                    timeSlot {
                        endTime
                        startTime
                    }
                }
            }
        }
    }
    """

    variables = {
        "filter": {
            "timeSlot": {
                "startTime": from_date,
                "endTime": to_date
            },
            "parent": self.config.business_id,
            "employees": filters.get('employees', []),
            "services": filters.get('services', []),
        },
        "timezone": "UTC"  # TODO: Make configurable
    }

    payload = {
        "query": query,
        "variables": variables
    }

    data = self._make_request("POST", "/graphql", json_data=payload)
    slots_data = data.get("data", {}).get("improvedAppointmentAvailability", {}).get("slots", [])

    available_slots = []
    for slot in slots_data:
        if slot.get("slotType") == "Available":
            time_slot = slot.get("slot", {}).get("timeSlot", {})
            if time_slot:
                available_slots.append(f"{time_slot['startTime']} - {time_slot['endTime']}")

    return available_slots


def generate_booking_link(self, date: str, time: str, service_id: str, employee_id: str) -> str:
    """Generate a booking link"""
    if not self.config.booking_link:
        raise ValueError("Booking link not configured")

    return f"{self.config.booking_link}?date={date}&time={time}&service={service_id}&employee={employee_id}"
