import os 
from typing import Optional
from apps.generator_base.models import UserCard
from sqlalchemy import select, and_
from apps.core.utils.misc.extras import Paginator
from apps.core.date_time import DateTime
from config.settings import MEDIA_DIR

class UserCardService:
    user_card = None
    @classmethod
    def __init__(cls, request = None):
        cls.request = request
        
    @classmethod
    def list_cards(
        cls, user_id: Optional[int] = None, page: int = 1, per_page: int = 10
    ):
        to_search = []
        if user_id is not None:
            to_search.append(UserCard.user_id == user_id)
        paginator = Paginator(
            select(UserCard).where(and_(*to_search)), page=page, per_page=per_page
        )

        return paginator.get_response(serializer=cls.retrive_card)
    
    @classmethod
    def __get_media_url(cls, card: UserCard):
        if cls.request is None:
            base_url = "http://127.0.0.1:8000/"
        else:
            base_url = str(cls.request.base_url)

        return f"{base_url}media/user_cards/{card.user_id}/{card.id}" if os.path.exists(MEDIA_DIR / f"user_cards/{card.user_id}/{card.id}") else None

    @classmethod
    def retrive_card(cls, card_id: int, ret_obj: bool = False):
        cls.user_card = UserCard.get(card_id)
        if ret_obj:
            return cls.user_card
        
        return {
            "user_card_id": cls.user_card.id,
            "image": cls.__get_media_url(cls.user_card),
            "name": cls.user_card.name,
            "description": cls.user_card.description,
            "size": cls.user_card.size,
            "created_at": DateTime.string(cls.user_card.created_at),
            "updated_at": DateTime.string(cls.user_card.updated_at)
        }
