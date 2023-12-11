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
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('rrapasheanil@gmail.com', 'wvuvamdufrzhlfbz')
        message = f'Your 6 digit OTP is {otp}'
        server.sendmail('rrapasheanil@gmail.com', email, message)
        server.quit()

    def send_otp_over_mobile(self, mobile_no, otp):
        client = Client(self.account_sid, self.auth_token)
        message_body = f'Your 6 digit OTP is {otp}'
        message = client.messages.create(
            body=message_body,
            from_=self.twilio_number,
            to=f'+91{mobile_no}',
        )
        print(message.body)

    def send_otp_to_mobile_user(self, mobile_user):
        if mobile_user.validate_mobile_no():
            self.send_otp_over_mobile(mobile_user.mobile_no, self.generate_otp())
        else:
            print("Invalid Mobile number")

    def send_otp_to_email_user(self, email_user):
        if email_user.validate_email():
            self.send_email(email_user.email, self.generate_otp())
        else:
            print("Invalid Email")

class MobileUser:
    def __init__(self, mobile_no):
        self.mobile_no = mobile_no

    def validate_mobile_no(self):
        return len(self.mobile_no) == 10 and self.mobile_no.isdigit()

class EmailUser:
    def __init__(self, email):
        self.email = email

    def validate_email(self):
        validation_condition = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return bool(re.search(validation_condition, self.email))

if __name__ == "__main__":
    ACCOUNT_SID = "ACe93ddab96de7a3735e8e026e74d878f1"
    AUTH_TOKEN = "fced3cd503fdd92c1b4ec774bb206020"
    TWILIO_NUMBER = '+18506600452'

    OTP_SENDER = OTPSender(ACCOUNT_SID, AUTH_TOKEN, TWILIO_NUMBER)

    MOBILE_USER = MobileUser(input("Enter the Mobile number:"))
    EMAIL_USER = EmailUser(input("Enter the Email:"))

    OTP_SENDER.send_otp_to_mobile_user(MOBILE_USER)
    OTP_SENDER.send_otp_to_email_user(EMAIL_USER)