from twilio.rest import Client

class TextMessageSender:
    def __init__(self, account_sid: str, auth_token: str, from_phone: str):
        self.client = Client(account_sid, auth_token)
        self.from_phone = from_phone

    def send_message(self, to_phone: str, message: str):
        try:
            message = self.client.messages.create(
                body=message,
                from_=self.from_phone,
                to=to_phone
            )
            return message.sid
        except Exception as e:
            print(f"Error sending message: {e}")
            return None