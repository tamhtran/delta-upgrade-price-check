import os
import logging
from twilio.rest import Client

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")  # Ensure this is set in your .env file
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")  # Ensure this is set in your .env file
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")  # Ensure this is set in your .env file


class TextService:
    def __init__(self):
        self.twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")  # Ensure this is set in your .env file
        self.twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")  # Ensure this is set in your .env file
        self.twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")  # Ensure this is set in your .env file
        self.client = Client(self.twilio_account_sid, self.twilio_auth_token)

    def send_alert(self, body, recipient_phone_number):
        message = self.client.messages.create(
            body=body,
            from_=recipient_phone_number,
            to=recipient_phone_number
        )

        logging.info(f"Alert sent: {message.sid}")