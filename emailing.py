import smtplib
import imghdr
from email.message import EmailMessage

#default
sender = "bear062005@gmail.com"
receiver = "bear062005@gmail.com"
password = "ykpvbcfyuocivxkt"

#function to send the attachment
def send_email(image_path):
    email_message = EmailMessage()
    email_message["Subject"] = "New customer showed up!"
    email_message.set_content("Hey, we just saw a new customer!")

    with open(image_path, "rb") as file:
        content = file.read()
    email_message.add_attachment(content, maintype= "image", subtype= imghdr.what(None, content))

#connecting the mail to the server
    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(sender, password)
    gmail.sendmail(sender, receiver, email_message.as_string())
    gmail.quit()


