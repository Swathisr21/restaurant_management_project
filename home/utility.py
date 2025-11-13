from datetime import datetime
from .models import DailyOperatingHours

def get_today_operating_hours():
    """
    Return today's operating hours as a tuple (open_time, close_time).
    if no record is found for today, returns (None, None).
    """
    today_name = datetime.now().strftime('%A')
    try:
        hours = DailyOperatingHours.objects.get(day_of_week=today_name)
        return (hours.open_time, hours.close_time)
    except DailyOperatingHours.DoesNotExist:
        return (None, None)   