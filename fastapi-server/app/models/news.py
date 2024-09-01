from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

class NewsItem(BaseModel):
    news_id: str
    title: str
    content: str
    hilight: str
    published_at: datetime
    enveloped_at: datetime
    dateline: datetime
    provider: str
    category: List[str]
    category_incident: List[str]
    byline: str
    provider_link_page: str
    printing_page: Optional[str] = None

