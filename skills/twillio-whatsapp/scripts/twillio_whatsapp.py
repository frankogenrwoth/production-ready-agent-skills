import os

from twilio.rest import Client # type: ignore
from dotenv import load_dotenv # type: ignore

_ = load_dotenv()  # Load environment variables from .env file

# Your Twilio credentials
account_sid = os.getenv("TWILIO_ACCOUNT_SID", "")
auth_token = os.getenv("TWILIO_AUTH_TOKEN", "")


def send_whatsapp_message(to_number: str, message_body: str) -> str:
    """
    Send a WhatsApp message using Twilio API.

    Args:
        to_number (str): The recipient's WhatsApp number in the format 'whatsapp:+1234567890'.
        message_body (str): The content of the message to be sent.

    Returns:
        str: The SID of the sent message.
    """
    # Initialize Twilio client
    client = Client(account_sid, auth_token)

    # Send WhatsApp message
    message = client.messages.create(
        body=message_body,
        from_="whatsapp:+14155238886",  # Twilio sandbox WhatsApp number
        to=to_number
    )

    return message.sid