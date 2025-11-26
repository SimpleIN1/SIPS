from django.conf import settings

from AccountApp.services.mail.mail_sender import SenderEmail


class ConfirmationEmail(SenderEmail):
    template = "mail/verify_email.html"
    subject = f"Confirmation register — {settings.WEBSITE_NAME}"


class ResetPasswordEmail(SenderEmail):
    template = "mail/password_reset_email.html"
    subject = f"Reset password — {settings.WEBSITE_NAME}"
