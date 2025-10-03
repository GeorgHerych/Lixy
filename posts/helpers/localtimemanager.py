from datetime import datetime, timedelta
from django.db.models import QuerySet
from django.utils import timezone

def get_local_diff():
    local_time = datetime.now()
    utc_time = timezone.now()

    local_hours = local_time.hour
    utc_hours = utc_time.hour

    local_minutes = local_time.minute
    utc_minutes = utc_time.minute

    local_minutes += local_hours * 60
    utc_minutes += utc_hours * 60

    diff = local_minutes - utc_minutes

    if diff < -720:
        diff += 1440
    elif diff > 720:
        diff -= 1440

    return diff

def set_local_time_to_model(model:object, property_name:str):
    local_utc_diff = get_local_diff()
    utc_time:datetime = getattr(model, property_name)
    utc_time = utc_time + timedelta(minutes = local_utc_diff)

    setattr(model, property_name, datetime(utc_time.year, utc_time.month, utc_time.day, utc_time.hour, utc_time.minute, utc_time.second))

def set_local_time_to_models(models:QuerySet[object], property_name:str):
    for model in models:
        set_local_time_to_model(model, property_name)