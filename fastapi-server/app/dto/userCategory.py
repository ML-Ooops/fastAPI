from typing import Optional, List

from pydantic import BaseModel

class UserUpdateDTO_Req(BaseModel):
    name: str
    user_category: List[float]
    new_category: List[float]

    class Config:
        arbitrary_types_allowed = True

class UserUpdateDTO_Res(BaseModel):
    new_user_category: List[float]
