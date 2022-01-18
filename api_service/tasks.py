from celery import shared_task
from celery.utils.log import get_task_logger

from django.core.mail import send_mail


logger = get_task_logger(__name__)


@shared_task(name="sent_email_to_admin")
def sent_email_to_admin(subject, message, sender, receivers):
    try:
        send_mail(subject, message, sender, receivers)
    except:
        logger.info(f"Need real data for sender and receiver(s)")
        logger.info(f"Data used in test:")
        logger.info(
            f"subject: {subject}, message: {message}, sender: {sender}, receiver: {receivers}"
        )
