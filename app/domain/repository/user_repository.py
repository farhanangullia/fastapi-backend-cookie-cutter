from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute
from app.monitoring.log import logger
from app.domain.repository.common import BaseTable, get_current_time_utc
from pynamodb.exceptions import DoesNotExist
from pynamodb.settings import OperationSettings
from pynamodb.models import Model


class AdminUser(BaseTable):
    class Meta(BaseTable.Meta):
        table_name = "AdminUsers"

    email = UnicodeAttribute(hash_key=True)
    first_name = UnicodeAttribute(null=True)
    last_name = UnicodeAttribute(null=True)
    created_at = UTCDateTimeAttribute(default_for_new=get_current_time_utc)
    updated_at = UTCDateTimeAttribute(default_for_new=get_current_time_utc)

    # overriding the method to add timestamp on update
    def update(self, actions=[], condition=None, settings=OperationSettings.default):
        actions.append(AdminUser.updated_at.set(get_current_time_utc()))
        Model.update(self, actions, condition, settings)


class UserRepository:
    table: AdminUser = AdminUser

    def __init__(cls) -> None:
        # Create the table
        logger.info(f"Initializing {cls.table.Meta.table_name}")
        if not cls.table.exists():
            logger.info(f"Creating {cls.table.Meta.table_name} table")
            cls.table.create_table(wait=True)

            mock_user = cls.table(
                "sampleuser@gmail.com",
                first_name="John",
            )
            mock_user.save()
            logger.info(
                f"Created {cls.table.Meta.table_name} table and initialized mock data..."
            )

    @classmethod
    def get_user_by_email(cls, email) -> AdminUser:
        try:
            user = cls.table.get(email)
        except DoesNotExist:
            return None
        logger.info(user)
        return user

    @classmethod
    def update_user(cls, email) -> AdminUser:
        try:
            user = cls.table.get(email)
            user.update(actions=[cls.table.last_name.set("Doe")])
        except DoesNotExist:
            return None
        logger.info(user)
        return user