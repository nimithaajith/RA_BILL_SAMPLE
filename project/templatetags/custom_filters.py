# for splitting subheading 
from django import template

register = template.Library()

from django import template
from django.utils.timezone import localtime
from pytz import timezone



@register.filter
def to_ist(value):
    """
    Convert a UTC datetime to Indian Standard Time (IST).
    """
    if value is None:
        return ''  # Return an empty string if the value is None
    try:
        ist = timezone('Asia/Kolkata')
        return localtime(value, ist).strftime('%Y-%m-%d %H:%M:%S')  # Return formatted IST time
    except Exception:
        return value  # Return the original value if conversion fails


@register.filter
def split(value, delimiter):
    return value.split(delimiter)
