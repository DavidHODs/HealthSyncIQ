import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from settings import Config


class EmailService:
  def __init__(self) -> None:
    self.smtp_host = Config.SMTP_HOST
    self.smtp_port = Config.SMTP_PORT
    self.username = Config.SMTP_USERNAME
    self.password = Config.SMTP_PASSWORD
    self.from_email = Config.SMTP_FROM_EMAIL or self.username

  def send_test_email(self, to_email: str, subject: str, body: str) -> bool:
    msg = MIMEText(body, "plain")
    msg["Subject"] = subject
    msg["From"] = self.from_email
    msg["To"] = to_email

    try:
      with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port) as server:
        server.login(self.username, self.password)
        server.send_message(msg)
      return True
    except Exception as e:
      print(f"[send_test_email] Failed: {e}")
      return False

  def send_html_email(self, to_email: str, subject: str, html: str) -> bool:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = self.from_email
    msg["To"] = to_email

    html_part = MIMEText(html, "html")
    msg.attach(html_part)

    try:
      with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port) as server:
        server.login(self.username, self.password)
        server.send_message(msg)
      return True
    except Exception as e:
      return False

  def load_html_template(self, file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
      return f.read().strip()
