from bson import Decimal128
import jdatetime
from persiantools.jdatetime import JalaliDateTime


def format_currency(value):
    return "{:,}".format(value.to_decimal())


def format_date_to_jalali(value, format_str):
    return JalaliDateTime(value).strftime(format_str)
