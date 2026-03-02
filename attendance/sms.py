import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def send_sms(phone_number, message):
    """
    Send SMS notification. Uses console logging by default.
    Set SMS_BACKEND = 'twilio' in settings and configure Twilio credentials
    to enable real SMS sending.
    """
    backend = getattr(settings, 'SMS_BACKEND', 'console')

    if backend == 'twilio':
        try:
            from twilio.rest import Client
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            client.messages.create(
                body=message,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=phone_number
            )
            logger.info(f"Twilio SMS sent to {phone_number}")
            return True
        except Exception as e:
            logger.error(f"Twilio SMS failed: {e}")
            return False
    else:
        # Console/file logging backend
        log_message = f"[SMS] To: {phone_number} | Message: {message}"
        print(log_message)
        logger.info(log_message)

        sms_log = getattr(settings, 'SMS_LOG_FILE', None)
        if sms_log:
            try:
                with open(sms_log, 'a') as f:
                    from django.utils import timezone
                    f.write(f"[{timezone.now()}] {log_message}\n")
            except Exception as e:
                logger.error(f"SMS log write failed: {e}")
        return True


def send_absent_sms(student, session):
    """Send SMS notification for absent student."""
    percentage = student.attendance_percentage()
    message = (
        f"Dear Parent, {student.name} (Reg: {student.register_number}) "
        f"was ABSENT on {session.date} during Period {session.period.period_number} "
        f"({session.period.start_time.strftime('%H:%M')} - {session.period.end_time.strftime('%H:%M')}). "
        f"Current Attendance: {percentage}%"
    )
    return send_sms(student.parent_phone, message)
