from typing import Optional, List

from pydantic import BaseModel

class UserUpdateDTO_Req(BaseModel):
    user_category: List[float]
    news_id: str


class UserUpdateDTO_Res(BaseModel):
    news_user_category: List[float]