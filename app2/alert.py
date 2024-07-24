import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()


def email_alert(subject, body, to, image_paths=None):
    # Create a multipart message
    msg = MIMEMultipart()
    msg.attach(MIMEText(body, "plain"))
    msg["Subject"] = subject
    msg["To"] = to
    msg["From"] = os.getenv("EMAIL_TO_REPORT")

    # Attach images as attachments
    if image_paths:
        for image_data in image_paths:
            # Add padding to the base64 string if necessary
            missing_padding = len(image_data) % 4
            if missing_padding:
                image_data += "=" * (4 - missing_padding)
            image_bytes = base64.b64decode(image_data)
            image = MIMEImage(image_bytes, _subtype="png")
            image.add_header("Content-Disposition", f"attachment; filename=image.png")
            msg.attach(image)

    # Send the email
    user = os.getenv("USER")
    password = os.getenv("PASSWORD")

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(user, password)
        server.sendmail(user, to, msg.as_string())
