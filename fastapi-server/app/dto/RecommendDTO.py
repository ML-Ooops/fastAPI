from typing import Optional, List

from pydantic import BaseModel

class NewsRecommendationDTO_Req(BaseModel):
    name: str
    user_category: List[float]
    num : int


    class Config:
        arbitrary_types_allowed = True


class recommend_news_similarity_InputData(BaseModel):
    category_array: List[int]
    top_n: int

class recommend_news_random_InputData(BaseModel):
    top_n: int
