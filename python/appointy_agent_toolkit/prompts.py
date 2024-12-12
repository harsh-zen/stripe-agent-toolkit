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
