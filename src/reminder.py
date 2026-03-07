"""Email notification system for DeadlineHQ.

Supports two email providers:
- Resend (recommended): Simple API-based email, no password needed — just an API key
- SMTP: Traditional email sending via SMTP (e.g., Gmail with App Password)

Configure the provider in config.json under email.provider ("resend" or "smtp").
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .config import get_config
from .logger import get_logger

logger = get_logger()


def send_email(to_email: str, subject: str, body: str):
    """Send an email using the configured provider.
    
    Automatically routes to Resend or SMTP based on config.json settings.
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        body: Email body text
    """
    config = get_config()
    provider = config.get('email', 'provider', default='smtp')
    
    if provider == 'resend':
        _send_via_resend(to_email, subject, body)
    elif provider == 'smtp':
        _send_via_smtp(to_email, subject, body)
    else:
        logger.error(f"Unknown email provider: {provider}. Use 'resend' or 'smtp'.")
        print(f"Error: Unknown email provider '{provider}'. Set email.provider to 'resend' or 'smtp' in config.json")


def _send_via_resend(to_email: str, subject: str, body: str):
    """Send email using the Resend API.
    
    Requires:
        - config.json: email.provider = "resend"
        - config.json: email.resend_from = "DeadlineHQ <notifications@yourdomain.com>"
        - Environment variable: DEADLINEHQ_RESEND_API_KEY
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        body: Email body text
    """
    import os
    
    try:
        import resend
    except ImportError:
        logger.error("Resend package not installed. Run: pip install resend")
        print("Error: Resend package not installed. Run: pip install resend")
        return
    
    config = get_config()
    
    api_key = os.getenv('DEADLINEHQ_RESEND_API_KEY')
    if not api_key:
        logger.error("DEADLINEHQ_RESEND_API_KEY environment variable not set")
        print("Error: Set DEADLINEHQ_RESEND_API_KEY environment variable with your Resend API key.")
        print("  Get one free at https://resend.com/api-keys")
        return
    
    from_email = config.get('email', 'resend_from', default='DeadlineHQ <onboarding@resend.dev>')
    
    resend.api_key = api_key
    
    try:
        params = {
            "from": from_email,
            "to": [to_email],
            "subject": subject,
            "text": body
        }
        
        email = resend.Emails.send(params)
        logger.info(f"Email sent to {to_email} via Resend (id: {email.get('id', 'unknown')})")
        print(f"Email sent to {to_email}")
    except Exception as e:
        logger.error(f"Failed to send email via Resend: {e}")
        print(f"Failed to send email: {e}")


def _send_via_smtp(to_email: str, subject: str, body: str):
    """Send email using SMTP (e.g., Gmail with App Password).
    
    Requires:
        - config.json: email.provider = "smtp"
        - config.json: email.smtp_server, email.smtp_port
        - Environment variable: DEADLINEHQ_EMAIL_PASSWORD (Gmail App Password)
        - Environment variable or config: DEADLINEHQ_SENDER_EMAIL
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        body: Email body text
    """
    config = get_config()
    
    smtp_server = config.get('email', 'smtp_server')
    smtp_port = config.get('email', 'smtp_port')
    sender_email = config.get_sender_email()
    
    if not sender_email:
        logger.error("Sender email not configured")
        print("Error: Sender email not configured. Set DEADLINEHQ_SENDER_EMAIL or update config.json")
        return
    
    try:
        sender_password = config.get_email_password()
    except ValueError as e:
        logger.error(str(e))
        print(f"Error: {e}")
        return
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, to_email, text)
        server.quit()
        logger.info(f"Email sent to {to_email} via SMTP")
        print(f"Email sent to {to_email}")
    except Exception as e:
        logger.error(f"Failed to send email via SMTP: {e}")
        print(f"Failed to send email: {e}")


def send_daily_status(task, subscriber):
    """Send a daily status update email for a task.
    
    Args:
        task: Task object to report on
        subscriber: Subscriber email address
    """
    status = f"Task: {task.name}\nDescription: {task.description}\nDeadline: {task.deadline}\nCompleted: {task.completed}\nSub-tasks:\n"
    for st in task.sub_tasks:
        status += f"- {st.name}: {'Done' if st.completed else 'Pending'}\n"
    send_email(subscriber, f"Daily Status: {task.name}", status)


def send_deadline_alert(task, subscriber):
    """Send a deadline alert email for a task.
    
    Args:
        task: Task object approaching deadline
        subscriber: Subscriber email address
    """
    body = f"Alert: Deadline approaching for task '{task.name}' on {task.deadline}"
    send_email(subscriber, f"Deadline Alert: {task.name}", body)
