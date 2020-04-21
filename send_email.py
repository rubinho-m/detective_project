import smtplib
from config import SENDER_EMAIL, REC_EMAIL, PASSWORD


def send_email(message):

    server = smtplib.SMTP('smtp.gmail.com', 587)

    server.ehlo()

    server.starttls()

    server.login(SENDER_EMAIL, PASSWORD)

    server.sendmail(SENDER_EMAIL, REC_EMAIL, message)

    server.close()


if __name__ == "__main__":
    message = 'Текст для модерации'.encode('utf-8')
    send_email(message)
