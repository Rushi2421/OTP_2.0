from twilio.rest import Client
import smtplib
import random
import re

class OTPSender:
    def __init__(self, account_sid, auth_token, input_no):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.input_no = input_no

    def validate_mobile_no(self, mobile_no):
        return len(mobile_no) == 10 and mobile_no.isdigit()

    def validate_email(self, email):
        validating_condition = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return bool(re.search(validating_condition, email))

    def generate_otp(self):
        return ''.join([str(random.randint(0, 9)) for _ in range(6)])

    def send_email(self, email, otp):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('rrapasheanil@gmail.com', 'wvuv amdu frzh lfbz')
        message = 'Your 6 digit OTP is ' + str(otp)
        server.sendmail('rrapasheanil@gmail.com', email, message)
        server.quit()

    def send_otp_through_sms(self, mobile_no, otp):
        client = Client(self.account_sid, self.auth_token)
        message = client.messages.create(
            body="Your 6 digit OTP is " + otp,
            from_=self.input_no,
            to='+91' + str(mobile_no),
        )
        print(message.body)

if __name__ == "__main__":
    account_sid = 'ACe93ddab96de7a3735e8e026e74d878f1'
    auth_token = 'fced3cd503fdd92c1b4ec774bb206020'
    input_no = '+18506600452'

    otp_sender = OTPSender(account_sid, auth_token, input_no)

    otp = otp_sender.generate_otp()

    mobile_no = input("Enter the Mobile number:")
    if otp_sender.validate_mobile_no(mobile_no):
        otp_sender.send_otp_through_sms(mobile_no, otp)
    else:
        print("Invalid Mobile no")

    email = input("Enter the Email:")
    if otp_sender.validate_email(email):
        otp_sender.send_email(email, otp)
    else:
        print("Invalid Email ")