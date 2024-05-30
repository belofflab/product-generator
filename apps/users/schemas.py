from pydantic import BaseModel


class UserCreate(BaseModel):
  id: int
  username: str
  full_name: str