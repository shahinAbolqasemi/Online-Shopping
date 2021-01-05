from bson import Decimal128
import jdatetime
from persiantools.jdatetime import JalaliDate


def format_currency(value):
    return "{:,}".format(value.to_decimal())


def format_date_to_jalali(value):
    return JalaliDate(value).strftime("%Y/%m/%d")
