import os
import sys
from datetime import datetime, timedelta, date

# ARG 1:  The abbrev for the unit e.g. "404C"

condo_unit = sys.argv[1]

# QA: collect problems and send one email at the end
QA_PROBLEMS = []


def parse(date_string):
    # Try to handle both date and datetime strings in ICS, removing any trailing newlines/spaces
    date_string = date_string.strip()
    # Handle formats like 20230614 or 20230614T090000Z
    if 'T' in date_string:
        try:
            return datetime.strptime(date_string, "%Y%m%dT%H%M%SZ")
        except ValueError:
            return datetime.strptime(date_string, "%Y%m%dT%H%M%S")
    else:
        return datetime.strptime(date_string, "%Y%m%d")


def dtstart_to_date(dt):
    """Return date part for comparison with today."""
    if isinstance(dt, datetime):
        return dt.date()
    return dt


def send_qa_report_if_needed():
    """Send a single email listing all QA problems, if any."""
    if not QA_PROBLEMS:
        return
    try:
        from send_email import send_email
    except ImportError:
        sys.stderr.write("QA: could not import send_email; skipping report.\n")
        return
    raw_to = os.environ.get("CALENDAR_QA_REPORT_TO") or os.environ.get("ACTION_MAILER_DEFAULT_TO")
    if not raw_to:
        sys.stderr.write("QA: no CALENDAR_QA_REPORT_TO or ACTION_MAILER_DEFAULT_TO; skipping report.\n")
        return
    # Comma-separated list of addresses (same as send_email --to)
    to = [a.strip() for a in raw_to.split(",") if a.strip()]
    subject = "Calendar QA: %s – %d problem(s)" % (condo_unit, len(QA_PROBLEMS))
    body = "Unit: %s\n\n" % condo_unit + "\n".join(QA_PROBLEMS)
    try:
        send_email(to, subject, body)
    except Exception as e:
        sys.stderr.write("QA: failed to send report: %s\n" % e)


# Buffered output so we can parse and transform in one pass
LINES = list(sys.stdin)

today = date.today()
in_vevent = False
current_dtstart = None
current_dtend = None
current_transp = None
current_summary = None
current_uid = None
dtstart_date_only = None   # True = VALUE=DATE (yyyymmdd), False = has time
dtend_date_only = None

for line in LINES:
    if line[0] != ' ':
        (field1, field2) = line.split(':', 1)
        # --- VEVENT state for QA ---
        if field1 == 'BEGIN' and field2.strip() == 'VEVENT':
            in_vevent = True
            current_dtstart = None
            current_dtend = None
            current_transp = None
            current_summary = None
            current_uid = None
            dtstart_date_only = None
            dtend_date_only = None
        elif field1 == 'END' and field2.strip() == 'VEVENT':
            if in_vevent and current_dtstart is not None:
                start_date = dtstart_to_date(current_dtstart)
                if start_date >= today:
                    summary = (current_summary or '').strip() or '(no SUMMARY)'
                    uid = (current_uid or '').strip() or '(no UID)'
                    if current_transp == 'TRANSPARENT':
                        QA_PROBLEMS.append(
                            "\nCalendar entry is not properly set to 'BUSY' status:\n"
                            "DTSTART=%s, SUMMARY=%s, UID=%s" % (current_dtstart, summary, uid)
                        )
                    if not dtstart_date_only or not dtend_date_only:
                        dtstart_val = str(current_dtstart) if current_dtstart is not None else "(not set)"
                        dtend_val = str(current_dtend) if current_dtend is not None else "(not set)"
                        QA_PROBLEMS.append(
                            "\nCalendar entry is not properly set to FULL-DAY status:\n"
                            "DTSTART=%s, DTEND=%s, SUMMARY=%s, UID=%s"
                            % (dtstart_val, dtend_val, summary, uid)
                        )
            in_vevent = False
        elif in_vevent:
            if field1 == 'DTSTART;VALUE=DATE':
                current_dtstart = parse(field2)
                dtstart_date_only = True
            elif field1 == 'DTSTART':
                current_dtstart = parse(field2)
                dtstart_date_only = False
            elif field1 == 'DTEND;VALUE=DATE':
                current_dtend = parse(field2)
                dtend_date_only = True
            elif field1 == 'DTEND':
                current_dtend = parse(field2)
                dtend_date_only = False
            elif field1 == 'TRANSP':
                current_transp = field2.strip()
            elif field1 == 'SUMMARY':
                current_summary = field2
            elif field1 == 'UID':
                current_uid = field2
        # --- transform output ---
        if field1 == 'DTSTART;VALUE=DATE':
            start_day = parse(field2).day
        elif field1 == 'DTSTAMP':
            dtstamp = field2
        elif field1 == 'LAST-MODIFIED':
            print("%s:%s" % (field1, dtstamp.rstrip()))
            continue
        elif field1 == "DTEND;VALUE=DATE":
            end_today = parse(field2)
            end_tomorrow = end_today + timedelta(days=1)
            end_tomorrow_day = end_tomorrow.day
            print("%s:%s" % (field1, end_tomorrow.strftime("%Y%m%d")))
            continue
        elif field1 == "SUMMARY":
            print("%s:%s %s-%s %s" % (field1, condo_unit, start_day, end_today.day, field2.rstrip()))
            continue

    print(line.rstrip())

send_qa_report_if_needed()
