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

    # @staticmethod
    # def _preprocess_create(values: Dict[str, Any]) -> Dict[str, Any]:
    #     timestamp_now = time.time()
    #     values["id"] = str(uuid.uuid4())
    #     values["created_at"] = timestamp_now
    #     values["updated_at"] = timestamp_now
    #     return values

    # @classmethod
    # def create(cls, product_in: ProductSchemaIn) -> ProductSchemaOut:
    #     data = cls._preprocess_create(product_in.dict())
    #     model = cls.table(**data)
    #     model.save()
    #     return cls.schema_out(**model.attribute_values)

    # @classmethod
    # def get(cls, entry_id: Union[str, uuid.UUID]) -> ProductSchemaOut:
    #     model = cls.table.get(str(entry_id))
    #     return cls.schema_out(**model.attribute_values)
