import os
import subprocess
import uuid

from dateutil import relativedelta as rdelta
from django.conf import settings
from django.utils import timezone
from django.utils.formats import get_format


def chrometopdf(html, name=""):
    """use headles chrome to convert an html document to pdf"""

    try:

        if not name:
            name = uuid.uuid4().hex[:10]

        fname = "%s_%s.html" % (name, uuid.uuid4().hex[:10])
        path = os.path.join(settings.TMP_REPORT_ROOT, fname)
        out_path = "%s.pdf" % path

        tmp_html = open(path, "wb")
        tmp_html.write(html.encode("UTF-8"))
        tmp_html.flush()

        out_file = open(out_path, "wb")

        command = [
            settings.CHROME_PATH,
            '--headless',
            '--disable-gpu',
            '--no-sandbox',
            '--print-to-pdf=%s' % out_file.name,
            "file://%s" % tmp_html.name,
        ]

        if os.name.lower() == "nt":
            command = ' '.join(command)

        stdout = open(os.path.join(settings.LOG_ROOT, 'report-stdout.txt'), 'a')
        stderr = open(os.path.join(settings.LOG_ROOT, 'report-stderr.txt'), 'a')
        subprocess.call(command, stdout=stdout, stderr=stderr)

        pdf = open(out_file.name, 'r+b').read()

    except OSError:
        raise OSError("chrome '%s' executable not found" % (settings.CHROME_PATH))
    finally:
        tmp_html.close()
        out_file.close()
        try:
            os.unlink(tmp_html.name)
        except:  # noqa: E722
            pass

    return pdf


def format_datetime(dt, fmt=settings.DATETIME_INPUT_FORMATS[0]):
    """Take a date time and return as string formatted date time after converting to localtime"""

    if not dt:
        return ""

    if isinstance(dt, timezone.datetime) and timezone.is_aware(dt):
        dt = timezone.localtime(dt)

    return dt.strftime(fmt)


def format_as_date(dt, fmt=settings.DATE_INPUT_FORMATS[0]):
    """Take a date time and return as string formatted date after converting to localtime"""

    return format_datetime(dt, fmt=fmt)


def format_as_time(dt, fmt=settings.TIME_INPUT_FORMATS[0]):
    return format_datetime(dt, fmt=fmt)


def parse_datetime(dt_str):
    """Take string and return datetime object"""
    for fmt in get_format("DATETIME_INPUT_FORMATS"):
        try:
            return timezone.datetime.strptime(dt_str, fmt)
        except (ValueError, TypeError):
            continue


def parse_date(dt_str, as_date=True):
    """Take a string and return date object"""
    for fmt in get_format("DATE_INPUT_FORMATS"):
        try:
            dt = timezone.datetime.strptime(dt_str, fmt)
            if as_date:
                dt = dt.date()
            return dt
        except (ValueError, TypeError):
            continue


def end_of_day(dt):
    """Take datetime and move forward to last microsecond of date"""

    return dt.replace(hour=23, minute=59, second=59, microsecond=999999)


def start_of_day(dt):
    """Take datetime and move backward first microsecond of date"""
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)


def today_start_end():
    """Return datetimes representing start and end of today"""
    now = timezone.localtime(timezone.now())
    return start_of_day(now), end_of_day(now)


def today_start():
    """Return datetime representing start of today"""
    now = timezone.localtime(timezone.now())
    return start_of_day(now)


def today_end():
    """Return datetime representing start of today"""
    now = timezone.localtime(timezone.now())
    return end_of_day(now)


class relative_dates:

    FUTURE_RANGES = [
        "next 7 days",
        "next 30 days",
        "next 365 days",
        "this week",
        "this month",
        "this year",
        "next week",
        "next month",
        "next year",
        "today",
    ]

    PAST_RANGES = [
        "today",
        "last 7 days",
        "last 30 days",
        "last 365 days",
        "this week",
        "this month",
        "this year",
        "last week",
        "last month",
        "last year",
    ]

    ALL_DATE_RANGES = PAST_RANGES + FUTURE_RANGES

    def __init__(self, date_range, pivot=None):
        """
        Initialize a relative_dates object.

        date_range is a string from PAST_RANGES/FUTURE_RANGES and times for
        start_dt & end_dt are start of day and end of day respectively.

        Example Usage:

            rd = relative_dates("next 7 days")
            start_dt, end_dt = rd.range

            pivot = timezone.now() + timezone.timedelta(days=4)
            rd = relative_dates("next 7 days", pivot=pivot)
            start_dt = rd.start
            end_dt = rd.end
        """

        if not date_range.lower() in self.ALL_DATE_RANGES:
            raise ValueError("%s is not a valid date range string")

        self.date_range = date_range.strip().lower()

        self.pivot = (pivot or timezone.now()).astimezone(timezone.get_current_timezone())

    def range(self):

        if self.date_range.startswith("today"):
            return start_of_day(self.pivot), end_of_day(self.pivot)
        elif self.date_range.startswith("next"):
            return self._next_interval()
        elif self.date_range.startswith("this"):
            return self._this_interval()
        elif self.date_range.startswith("last"):
            return self._last_interval()

    def start(self):
        return self.range()[0]

    def end(self):
        return self.range()[1]

    def _next_interval(self):

        dr = self.date_range

        if 'days' in dr:
            __, num, interval = dr.split()
            start = start_of_day(self.pivot)
            end = end_of_day(start + timezone.timedelta(days=int(num)))
        elif 'week' in dr:
            start = start_of_day(self.pivot) + rdelta.relativedelta(days=1, weekday=rdelta.SU)
            end = end_of_day(self.pivot) + rdelta.relativedelta(days=7, weekday=rdelta.SA)
        elif 'month' in dr:
            start = start_of_day(self.pivot) + rdelta.relativedelta(months=1, day=1)
            end = end_of_day(self.pivot) + rdelta.relativedelta(months=1, day=31)
        elif 'year' in dr:
            start = start_of_day(self.pivot) + rdelta.relativedelta(years=1, month=1, day=1)
            end = end_of_day(self.pivot) + rdelta.relativedelta(years=1, month=12, day=31)
        return start, end

    def _this_interval(self):
        dr = self.date_range

        if 'days' in dr:
            __, num, interval = dr.split()
            start = start_of_day(self.pivot)
            end = end_of_day(start + timezone.timedelta(days=int(num)))
        elif 'week' in dr:
            start = start_of_day(self.pivot) + rdelta.relativedelta(weekday=rdelta.SU(-1))
            end = end_of_day(self.pivot) + rdelta.relativedelta(weekday=rdelta.SA(1))
        elif 'month' in dr:
            start = start_of_day(self.pivot) + rdelta.relativedelta(months=0, day=1)
            end = end_of_day(self.pivot) + rdelta.relativedelta(months=0, day=31)
        elif 'year' in dr:
            start = start_of_day(self.pivot) + rdelta.relativedelta(month=1, day=1)
            end = end_of_day(self.pivot) + rdelta.relativedelta(month=12, day=31)

        return start, end

    def _last_interval(self):

        dr = self.date_range

        if 'days' in dr:
            __, num, interval = dr.split()
            end = end_of_day(self.pivot)
            start = start_of_day(end + timezone.timedelta(days=-int(num)))
        elif 'week' in dr:
            start = start_of_day(self.pivot) + rdelta.relativedelta(weekday=rdelta.SU(-2))
            end = end_of_day(self.pivot) + rdelta.relativedelta(weeks=-1, weekday=rdelta.SA(1))
        elif 'month' in dr:
            start = start_of_day(self.pivot) + rdelta.relativedelta(months=-1, day=1)
            end = end_of_day(self.pivot) + rdelta.relativedelta(months=-1, day=31)
        elif 'year' in dr:
            start = start_of_day(self.pivot) + rdelta.relativedelta(years=-1, month=1, day=1)
            end = end_of_day(self.pivot) + rdelta.relativedelta(years=-1, month=12, day=31)
        return start, end
