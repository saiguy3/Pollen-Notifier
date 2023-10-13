from twilio.rest import Client
from typing import Any

import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

ACCOUNT_SID = os.environ.get("ACCOUNT_SID")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")
RECEIVER_PHONE_NUMBER = os.environ.get("RECEIVER_PHONE_NUMBER")


class TwilioGateway:
    def __init__(self) -> None:
        """
        Initiates a Twilio Client from ENV vars
        """
        self.client = Client(ACCOUNT_SID, AUTH_TOKEN)

    def send_message(self, body: str) -> Any:
        """
        Sends a message with the supplied body.
        """
        message = self.client.messages.create(
            from_=TWILIO_PHONE_NUMBER,
            to=RECEIVER_PHONE_NUMBER,
            body=body,
        )
        return message
