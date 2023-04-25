import pickle
import os

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from base64 import urlsafe_b64decode, urlsafe_b64encode
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type


class SendMail:
    email = None
    picklecred = None
    gmailcred = None
    site = None

    def gmail_authenticate(self):
        SCOPES = ['https://mail.google.com/']
        creds = None
        if os.path.exists(self.picklecred):
            with open(self.picklecred, "rb") as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.gmailcred, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(self.picklecred, "wb") as token:
                pickle.dump(creds, token)
        return build('gmail', 'v1', credentials=creds)

    def build_message(self, destination, obj, body):
        message = MIMEText(body)
        message['to'] = destination
        message['from'] = self.email
        message['subject'] = obj
        return {'raw': urlsafe_b64encode(message.as_bytes()).decode()}

    def send_message(self, service, destination, obj, body):
        return service.users().messages().send(
            userId="me",
            body=self.build_message(destination, obj, body)
        ).execute()


    def __init__(self, email, picklecred, gmailcred, site):
        self.email = email
        self.picklecred = picklecred
        self.gmailcred = gmailcred
        self.site = site

        
    def send_error(self, receiver_emails, error):
        subject = f"Airglow {self.site} Error"
        message = """
This message is sent from """
        message = message + self.site
        message = message + """ FPI site. The program encountered the following error:\

            """
        message = message + str(error)

        service = self.gmail_authenticate()
        for destination in receiver_emails:
            self.send_message(service, destination, subject, message)
    
    
