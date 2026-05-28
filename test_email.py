import smtplib, ssl
from email.message import EmailMessage
import certifi

email_sender = "meryljo25@gmail.com"
email_password = "qdnngmrsibcxmbvz"  # Your App Password
email_receiver = "sandriya200@gmail.com"  # Replace with your email

subject = "Test Email"
body = "This is a test email from Django project."

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

# Use certifi's CA bundle
context = ssl.create_default_context(cafile=certifi.where())

try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
    print("✅ Email sent successfully!")
except Exception as e:
    print(f"❌ Error: {e}")
