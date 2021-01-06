from datetime import datetime

from bson import ObjectId, Decimal128
from flask import json
from online_shopping.util.filters import format_currency, format_date_to_jalali


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, Decimal128):
            return format_currency(o)
        elif isinstance(o, datetime):
            return format_date_to_jalali(o, "%Y/%m/%d %H:%M:%S")
        return json.JSONEncoder.default(self, o)
