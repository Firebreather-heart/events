import logging
from celery import shared_task
from .main import sendmail

logger = logging.getLogger(__name__)

@shared_task
def send_mail_task(payload, recipient, subject, filepath):
    try:
        sendmail(payload, recipient, subject, filepath=filepath, type='html')
    except Exception as e:
        logger.exception("Error sending email to %s: %s", recipient, str(e))
