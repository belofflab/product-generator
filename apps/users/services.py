import asyncio
from sqlalchemy import select, update
from apps.users.models import User
from config.database import DatabaseManager
from sqlalchemy.sql import exists
from apps.core.date_time import DateTime
from config.settings import MAX_USER_TASKS
# from loader import analytics


class UserService:
    user = None

    @classmethod
    def create_or_update_user(cls, **data):
        cls._create_or_update_user(**data)

        return cls.retrive_user(cls.user.id)

    @classmethod
    def is_exists(cls, user_id: int):
        with DatabaseManager.session as session:
            result = session.query(exists().where(User.id == user_id)).scalar()
        return result
    
    @classmethod
    def _create_or_update_user(cls, **data):
        user_id = data.pop("id")
        username = data.pop("username")
        full_name = data.pop("full_name")
        cls.user = User.get_or_none(user_id)
        if cls.user is None:
            cls.user = User.create(
                id=user_id,
                username=username,
                full_name=full_name,
            )
        else:
            to_update = {}
            if username != cls.user.username:
                to_update["username"] = username
            if full_name != cls.user.full_name:
                to_update["username"] = username
            if not cls.user.is_active:
                to_update["is_active"] = True
            cls.user = User.update(cls.user.id, **to_update)

    @classmethod
    def get_admins(cls):
        admins_list = []
        with DatabaseManager.session as session:
            admins = session.execute(select(User.id).where(User.is_admin.is_(True)))
            for admin in admins:
                admins_list.append(admin.id)
        return admins_list

    @classmethod
    def retrive_user(cls, user_id: int):
        cls.user = User.get(user_id)

        return {
            "id": cls.user.id,
            "username": cls.user.username,
            "full_name": cls.user.full_name,
            "is_active": cls.user.is_active,
            "is_subscribed": cls.user.is_subscribed,
            "is_admin": cls.user.is_admin,
            "date_joined": DateTime.string(cls.user.date_joined),
            "last_join": DateTime.string(cls.user.last_join),
        }
