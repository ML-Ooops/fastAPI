from typing import Optional, List

from pydantic import BaseModel

class UserUpdateDTO_Req(BaseModel):
    name: str
    user_category: List[float]
    news_id: str

    class Config:
        arbitrary_types_allowed = True

class UserUpdateDTO_Res(BaseModel):
    news_user_category: List[float]