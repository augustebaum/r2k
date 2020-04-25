import smtplib
from email.message import EmailMessage
from typing import List, Optional, Tuple

from r2k.cli import logger

from .config import config
from .unicode import strip_common_unicode_chars


def build_basic_message(title: str) -> EmailMessage:
    msg = EmailMessage()
    msg["Subject"] = title
    msg["To"] = config.send_to
    msg["From"] = config.send_from
    return msg


def send_email_message(server: smtplib.SMTP, msg: EmailMessage) -> bool:
    """Send a single EmailMessage"""
    logger.debug("Sending the email...")
    try:
        server.send_message(msg)
        return True
    except smtplib.SMTPException as e:
        logger.error(f"Caught an exception while trying to send an email.\nError: {e}")
        return False


def send_email_messages(msgs: List[EmailMessage]) -> int:
    """Send an email"""
    # TODO: Consider making smtp server configurable
    messages_sent = 0
    try:
        logger.debug("Connecting to SMTP...")
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.ehlo()
            logger.debug("Logging into the SMTP server...")
            server.login(config.send_from, config.password)
            for msg in msgs:
                if send_email_message(server, msg):
                    messages_sent += 1
                    logger.info("Email sent successfully!")
    except smtplib.SMTPException as e:
        logger.error(f"Caught an exception while trying to send an email.\nError: {e}")
    return messages_sent


def set_content(msg: EmailMessage, title: str, url: Optional[str], content: Optional[str]) -> None:
    """Either set the text content of the email message, or attach an attachment, based on the current parser"""
    if content:
        filename = f"{title}.html"
        logger.debug(f"Setting attachment for {filename}")
        msg.add_attachment(
            content.encode("utf-8"),
            maintype="text",
            subtype=f'html; charset=utf-8; name="{filename}"',
            filename=filename,
        )
    elif url:
        logger.debug(f"Setting email content to {url}")
        msg.set_content(url)


def create_email_message(title: str, url: Optional[str], content: Optional[str]) -> EmailMessage:
    title = strip_common_unicode_chars(title)
    msg = build_basic_message(title)
    set_content(msg, title, url, content)
    return msg


def send_html(title: str, content: str) -> int:
    """Send an HTML file to Kindle"""
    msg = create_email_message(title, None, content)
    return send_email_messages([msg])


def send_urls(articles: List[Tuple[str, str]]) -> int:
    """Send a list of URLs to Kindle (via pushtokindle)"""
    msgs = []
    for title, url in articles:
        msgs.append(create_email_message(title, url, None))
    return send_email_messages(msgs)
