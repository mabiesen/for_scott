import smtplib, ssl

PORT = 465  # For SSL
SMTP_SERVER = "smtp.gmail.com"
SENDER_EMAIL = "upandcomming88@gmail.com"  # Enter your address
RECEIVER_EMAIL = "upandcomming88@gmail.com"  # Enter receiver address

# Prompt will happen the moment we load this file
PASSWORD = input("Type your email password and press enter: ")

def send_email(message):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, PORT, context=context) as server:
        server.login(SENDER_EMAIL, PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message)
