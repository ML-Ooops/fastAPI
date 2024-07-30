from typing import List

from pydantic import BaseModel


class NewsItemCategory(BaseModel):
    news_id: str
    category_array: List[int]