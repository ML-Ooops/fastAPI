from http.client import HTTPException
from typing import List, Dict

from db import db


async def fetch_all_news(helper_func) -> List[Dict]:
    news_collection = db.news_collection
    news_documents = await news_collection.find().to_list(None)
    if news_documents:
        return [helper_func(news) for doc in news_documents for news in doc.get("documents", [])]
    else:
        raise HTTPException(status_code=404, detail="News items not found")


async def fetch_find_news(helper_func, ars) -> List[Dict]:
    news_collection = db.news_collection
    news_documents = await news_collection.find().to_list(None)
    if news_documents:
        return [helper_func(news) for doc in news_documents for news in doc.get("documents", [])]
    else:
        raise HTTPException(status_code=404, detail="News items not found")