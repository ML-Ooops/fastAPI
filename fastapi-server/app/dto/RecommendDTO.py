from typing import Optional, List

from pydantic import BaseModel

class NewsRecommendationDTO_Req(BaseModel):
    name: str
    user_category: List[float]
    num : int


    class Config:
        arbitrary_types_allowed = True


