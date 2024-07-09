from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from fastapi import APIRouter

from userservice.models import Forgot_password_request

router = APIRouter(
    prefix='/user',
    tags=['Manage password']
)

def send_email(to_email: str, subject: str, body: str):
    from_email = "ziamartapi@gmail.com"
    password = "formartapi6221"
    
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    
    msg.attach(MIMEText(body, "plain"))
    
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

@router.post('/forgot_password')
async def request_password_recovery(req:Forgot_password_request):
    