from twilio.rest import Client
import smtplib
import random
import re

class OTPSender:
    def __init__(self, account_sid, auth_token, twilio_number):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.twilio_number = twilio_number

    def generate_otp(self):
        digits = "0123456789"
        return ''.join(random.choice(digits) for _ in range(6))

    def send_email(self, email, otp):
        server = self._setup_email_server()
        message = f'Your 6 digit OTP is {otp}'
        server.sendmail('rrapasheanil@gmail.com', email, message)
        server.quit()

    def _setup_email_server(self):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('rrapasheanil@gmail.com', 'wvuvamdufrzhlfbz')
        return server

    def send_otp_over_mobile(self, mobile_no, otp):
        client = Client(self.account_sid, self.auth_token)
        message_body = f'Your 6 digit OTP is {otp}'
        message = client.messages.create(
            body=message_body,
            from_=self.twilio_number,
            to=f'+91{mobile_no}',
        )
        print(message.body)

    def send_otp(self, user):
        if user.validate():
            if isinstance(user, MobileUser):
                self.send_otp_over_mobile(user.value, self.generate_otp())
            elif isinstance(user, EmailUser):
                self.send_email(user.value, self.generate_otp())
        else:
            print(f"Invalid {user.type}.")

class User:
    def __init__(self, value, type):
        self.value = value
        self.type = type

    def validate(self):
        raise NotImplementedError("Subclasses must implement the validate method.")

class MobileUser(User):
    def __init__(self, mobile_no):
        super().__init__(mobile_no, "Mobile number")

    def validate(self):
        return len(self.value) == 10 and self.value.isdigit()

class EmailUser(User):
    def __init__(self, email):
        super().__init__(email, "Email address")

    def validate(self):
        validation_condition = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return bool(re.search(validation_condition, self.value))

if __name__ == "__main__":
    ACCOUNT_SID = "ACe93ddab96de7a3735e8e026e74d878f1"
    AUTH_TOKEN = "fced3cd503fdd92c1b4ec774bb206020"
    TWILIO_NUMBER = '+18506600452'

    OTP_SENDER = OTPSender(ACCOUNT_SID, AUTH_TOKEN, TWILIO_NUMBER)

    MOBILE_USER = MobileUser(input("Enter the Mobile number:"))
    EMAIL_USER = EmailUser(input("Enter the Email:"))

    OTP_SENDER.send_otp(MOBILE_USER)
    OTP_SENDER.send_otp(EMAIL_USER)