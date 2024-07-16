import os
import base64
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.send", "https://www.googleapis.com/auth/gmail.readonly"]

class MailService:
    def __init__(self):
        self.SCOPES = ["https://www.googleapis.com/auth/gmail.send", "https://www.googleapis.com/auth/gmail.readonly"]
        self.creds = None
        if os.path.exists("token.json"):
            self.creds = Credentials.from_authorized_user_file("token.json", self.SCOPES)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(self.creds.to_json())
        self.service = build("gmail", "v1", credentials=self.creds)

    def send_email(self, body, recipient_email):
        try:
            message = MIMEText(body)
            message["to"] = recipient_email
            message["subject"] = "Delta Upgrade Price Alert"
            raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
            message = self.service.users().messages().send(userId="me", body={"raw": raw}).execute()
            print(f'Email sent to {recipient_email}, message ID: {message["id"]}')
        except HttpError as error:
            print(f"An error occurred: {error}")


if __name__ == '__main__':
    mail_service = MailService()
    mail_service.send_email("Hello, this is a fun email", "ms.tam.h.tran@gmail.com")