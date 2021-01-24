import smtplib, ssl

PORT = 465  # For SSL
SMTP_SERVER = "smtp.gmail.com"
SENDER_EMAIL = "upandcomming88@gmail.com"  # Enter your address
RECEIVER_EMAIL = "upandcomming88@gmail.com"  # Enter receiver address

def get_password():
    return input("Type your email password and press enter: ")

def send_email(message, password):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, PORT, context=context) as server:
        server.login(SENDER_EMAIL, password)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message)
