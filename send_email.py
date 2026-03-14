#!/usr/bin/env python3
"""
Send email via SMTP using credentials from the environment.

Source env-prod (or set SMTP_* and optionally ACTION_MAILER_DEFAULT_FROM)
before running. Example:

    source env-prod
    python -m send_email --to someone@example.com --subject "Test" --body "Hello"
    python -c "from send_email import send_email; send_email('a@b.com', 'Hi', 'Body')"
"""

import os
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def _config():
    """Read SMTP config from environment (e.g. after sourcing env-prod)."""
    host = os.environ.get("SMTP_ADDRESS")
    port = int(os.environ.get("SMTP_PORT", "587"))
    username = os.environ.get("SMTP_USERNAME")
    password = os.environ.get("SMTP_PASSWORD")
    default_from = os.environ.get("ACTION_MAILER_DEFAULT_FROM") or username
    use_starttls = os.environ.get("SMTP_ENABLE_STARTTLS_AUTO", "true").lower() in ("true", "1", "yes")
    if not all((host, username, password)):
        raise RuntimeError(
            "Missing SMTP config. Set SMTP_ADDRESS, SMTP_USERNAME, SMTP_PASSWORD (e.g. source env-prod)."
        )
    return {
        "host": host,
        "port": port,
        "username": username,
        "password": password,
        "default_from": default_from,
        "use_starttls": use_starttls,
    }


def send_email(
    to,
    subject,
    body,
    *,
    from_addr=None,
    body_html=None,
    reply_to=None,
):
    """
    Send an email via the configured SMTP server.

    Args:
        to: Recipient address (str) or list of addresses.
        subject: Subject line.
        body: Plain-text body.
        from_addr: From address (default: ACTION_MAILER_DEFAULT_FROM or SMTP_USERNAME).
        body_html: Optional HTML body; if set, message is sent as multipart/alternative.
        reply_to: Optional Reply-To header.

    Returns:
        None

    Raises:
        RuntimeError: If SMTP env vars are not set.
        smtplib.SMTPException: On send failure.
    """
    cfg = _config()
    from_addr = from_addr or cfg["default_from"]
    if isinstance(to, str):
        to = [to]

    if body_html:
        msg = MIMEMultipart("alternative")
        msg.attach(MIMEText(body, "plain"))
        msg.attach(MIMEText(body_html, "html"))
    else:
        msg = MIMEText(body, "plain")

    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = ", ".join(to)
    if reply_to:
        msg["Reply-To"] = reply_to

    with smtplib.SMTP(cfg["host"], cfg["port"]) as smtp:
        if cfg["use_starttls"]:
            smtp.starttls()
        smtp.login(cfg["username"], cfg["password"])
        smtp.sendmail(from_addr, to, msg.as_string())


def _main():
    import argparse
    p = argparse.ArgumentParser(description="Send email using env SMTP config (e.g. source env-prod).")
    p.add_argument("--to", required=True, help="Recipient email address(es), comma-separated")
    p.add_argument("--subject", required=True, help="Subject line")
    p.add_argument("--body", required=True, help="Plain-text body")
    p.add_argument("--from", dest="from_addr", default=None, help="From address (default from env)")
    p.add_argument("--html", default=None, help="Optional HTML body")
    args = p.parse_args()
    to = [a.strip() for a in args.to.split(",")]
    try:
        send_email(
            to,
            args.subject,
            args.body,
            from_addr=args.from_addr,
            body_html=args.html,
        )
        print("Sent successfully.")
    except RuntimeError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    except smtplib.SMTPException as e:
        print(f"SMTP error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    _main()
