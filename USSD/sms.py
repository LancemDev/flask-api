from __future__ import print_function
from dotenv import load_dotenv
import os
import africastalking

class SMS:
    def __init__(self, username):
         # Get your app credentials from app.africastalking.com
        #  self.username = username
        #  self.api_key = api_key
        load_dotenv()
        self.username = os.getenv('AT_USERNAME')
        self.api_key = os.getenv('AT_API_KEY')

        # Initialize the SDK
        africastalking.initialize(self.username, self.api_key)

        # Get the SMS service
        self.sms = africastalking.SMS

    def send(self, recipients_message, message_recipients, sender = None):
            # Set the numbers you want to send to in international format
            recipients = message_recipients

            # Set your message
            message = recipients_message

            # Set your shortCode or senderId
            try:
				# Thats it, hit send and we'll take care of the rest.
                response = self.sms.send(message, recipients, sender)
                print (response)
            except Exception as e:
                print ('Encountered an error while sending: %s' % str(e))