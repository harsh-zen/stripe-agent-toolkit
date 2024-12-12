CREATE_APPOINTMENT_PROMPT = """
This tool will create an appointment in Appointy.

It takes five arguments:
- title (str): The title of the appointment.
- start_time (str): The start time of the appointment.
- end_time (str): The end time of the appointment.
- customer_name (str): The name of the customer.
- customer_email (str): The email of the customer.
"""

LIST_APPOINTMENTS_PROMPT = """
This tool will fetch a list of appointments from Appointy.

It takes no input.
"""

UPDATE_APPOINTMENT_PROMPT = """
This tool will update an appointment in Appointy.

It takes six arguments:
- appointment_id (str): The ID of the appointment.
- title (str, optional): The title of the appointment.
- start_time (str, optional): The start time of the appointment.
- end_time (str, optional): The end time of the appointment.
- customer_name (str, optional): The name of the customer.
- customer_email (str, optional): The email of the customer.
"""

LIST_SERVICES_PROMPT = """
This tool will list all services for the business.

It takes one optional argument:
- query (str, optional): Query string to filter services.
"""

GET_STAFF_INFO_PROMPT = """
This tool will get available staff for a service.

It takes two arguments:
- service_id (str): The ID of the service.
- duration (str): The duration of the service.
"""

GET_SERVICE_INFO_PROMPT = """
This tool will get detailed service information.

It takes one argument:
- query (str): Query string to search for service.
"""

GET_AVAILABLE_DATES_PROMPT = """
This tool will get available dates for booking.

It takes three arguments:
- filters (dict): Filters for available dates.
- from_date (str): Start date for availability search.
- to_date (str): End date for availability search.
"""

GET_AVAILABLE_SLOTS_PROMPT = """
This tool will get available time slots for booking.

It takes three arguments:
- filters (dict): Filters for available slots.
- from_date (str): Start date for availability search.
- to_date (str): End date for availability search.
"""

GENERATE_BOOKING_LINK_PROMPT = """
This tool will generate a booking link.

It takes four arguments:
- date (str): Date for the booking.
- time (str): Time for the booking.
- service_id (str): ID of the service.
- employee_id (str): ID of the employee.
"""
