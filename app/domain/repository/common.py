from pynamodb.models import Model
from datetime import datetime, timezone
from app.utilities.settings import settings


def get_current_time_utc():
    return datetime.now(timezone.utc)


class BaseTable(Model):
    class Meta:
        read_capacity_units = 1
        write_capacity_units = 1
        host = settings.DYNAMODB_HOST if settings.DYNAMODB_HOST != "" else None
        region = settings.AWS_REGION
        aws_access_key_id = (
            settings.DUMMY_AWS_KEY if settings.DUMMY_AWS_KEY != "" else None
        )
        aws_secret_access_key = (
            settings.DUMMY_AWS_KEY if settings.DUMMY_AWS_KEY != "" else None
        )
