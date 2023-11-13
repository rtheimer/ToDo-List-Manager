from project import validate_date, calculate_days_overdue, validate_entry
from datetime import datetime, timedelta


def test_validate_entry():
    # minimum 3 characters
    assert validate_entry("ABC") == True
    assert validate_entry("abc") == True
    # starts with 3 Letters
    assert validate_entry("1AB") == False
    assert validate_entry("ab1") == False
    # no blanks at the beginning
    assert validate_entry(" AB") == False
    assert validate_entry("   ") == False
    # blank after three characters are allowed
    assert validate_entry("ABC DEF") == True
    # hyphens and underscore are allowed
    assert validate_entry("ABC _Text -") == True


def test_validate_date():
    # format must be mm/dd/YYYY   or mm-dd-YYYY
    assert validate_date("10/10/1962") == True
    assert validate_date("10-10-1962") == True
    assert validate_date("10-10-65") == False
    assert validate_date("") == False
    assert validate_date("10.12.1965") == False
    assert validate_date("<html>") == False


def test_calculate_days_overdue():
    d_today = datetime.today()
    date_today = d_today.strftime("%m%d%Y")

    day_future = d_today + timedelta(days=100)
    day_future = day_future.strftime("%m/%d/%Y")

    day_past = d_today - timedelta(days=100)
    day_past = day_past.strftime("%m/%d/%Y")

    # date today
    assert calculate_days_overdue(date_today) == None
    # date in the future
    assert calculate_days_overdue(day_future) == 100
    # date in the past
    assert calculate_days_overdue(day_past) == -100
    # format not supported
    assert calculate_days_overdue("not supported") == None
