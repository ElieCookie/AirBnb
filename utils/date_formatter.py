from datetime import datetime, timedelta
import random


def random_date_range() -> tuple[str, str]:
    check_in = datetime.today() + timedelta(days=random.randint(5, 10))
    check_out = check_in + timedelta(days=random.randint(3, 5))
    return check_in.strftime("%Y-%m-%d"), check_out.strftime("%Y-%m-%d")


def format_airbnb_date(date: datetime) -> str:
    return date.strftime("%-d, %A, %B %Y").lstrip("0")


def random_date_range_airbnb_format() -> tuple[str, str]:
    check_in = datetime.today() + timedelta(days=random.randint(5, 10))
    check_out = check_in + timedelta(days=random.randint(3, 5))
    airbnb_check_in = format_airbnb_date(check_in)
    airbnb_check_out = format_airbnb_date(check_out)
    iso_check_in = check_in.strftime("%Y-%m-%d")
    iso_check_out = check_out.strftime("%Y-%m-%d")
    month_name = check_in.strftime("%B")
    start_day = check_in.day
    end_day = check_out.day

    return (
        airbnb_check_in,  # e.g. "6, Tuesday, May 2025"
        airbnb_check_out,  # e.g. "10, Saturday, May 2025"
        iso_check_in,  # e.g. "2025-05-06"
        iso_check_out,  # e.g. "2025-05-10"
        month_name,  # e.g. "May"
        start_day,  # e.g. 6
        end_day,  # e.g. 10
    )
