from dotenv import load_dotenv
from twilio.rest import Client
import os

load_dotenv()

account = os.environ.get("TWILIO_ACCOUNT")
token = os.environ.get("TWILIO_TOKEN")
client = Client(account, token)

# currently an env var, need to make it more structured in a DB or something
recipients = os.environ.get("TWILIO_TO").split(",")

def sendTextAlert(content):
  for recipient in recipients:
    client.messages.create(
      to=recipient,
      messaging_service_sid=os.environ.get("TWILIO_MSG_SID"),
      body=content
    )
