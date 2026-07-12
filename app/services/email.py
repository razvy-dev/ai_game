# I will implement sending emails here using resend
from app.settings import settings
import resend

class EmailService:
    resend.api_key = settings.resend_api_key.get_secret_value()

    @staticmethod
    def send_forgot_password_email(to: str, validation_code: int, from_addr: str = settings.resend_email_from):
        subject = "Password reset email"
        html= f'<p>Congrats on trying to reset your <a target="_blank" href={settings.frontend_origin}{settings.forgot_password_route}{validation_code}>password</a>!</p>'

        r = resend.Emails.send({
            "from": from_addr,
            "to": to,
            "subject": subject,
            "html": html
        })

    @staticmethod
    def send_confirmation_email(to: str, validation_code: int, from_addr: str = settings.resend_email_from):
        subject = "Please confirm your account"
        html = f'<p>Congrats on trying to create your <a target="_blank" href={settings.frontend_origin}/account?token={validation_code}>account</a>!</p>'

        r = resend.Emails.send({
            "from": from_addr,
            "to": to,
            "subject": subject,
            "html": html
        })