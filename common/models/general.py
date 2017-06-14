import datetime
from django.conf import settings

def date_to_str(o):
    if o is not None:
        if isinstance(o, datetime.date):
            return o.strftime(settings.DISPLAY_DATE)
        elif isinstance(o, datetime.time):
            return o.strftime(settings.DISPLAY_TIME)
        elif isinstance(o, datetime.datetime):
            return o.strftime(settings.DISPLAY_DATE_TIME)
    else:
        return ''