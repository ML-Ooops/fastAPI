from typing import List, Dict

from pydantic import BaseModel

CATEGORY_INDEX = {
    "IT_과학>과학": 0,
    "IT_과학>보안": 1,
    "IT_과학>모바일": 2,
    "IT_과학>콘텐츠": 3,
    "IT_과학>인터넷_SNS": 4,
    "IT_과학>IT_과학일반": 5
}

def category_to_array(categories: List[str]) -> List[int]:
    array = [0] * len(CATEGORY_INDEX)
    for category in categories:
        if category in CATEGORY_INDEX:
            array[CATEGORY_INDEX[category]] = 1
    return array

def news_Category_helper(news: Dict) -> Dict:
    return {
        "news_id": news.get("news_id", ""),
        "category_array": category_to_array(news.get("category", []))
    }

def news_item_helper(news_item) -> dict:
    return {
        "news_id": news_item.get("news_id", ""),
        "title": news_item.get("title", ""),
        "content": news_item.get("content", ""),
        "hilight": news_item.get("hilight", ""),
        "published_at": news_item.get("published_at", ""),
        "enveloped_at": news_item.get("enveloped_at", ""),
        "dateline": news_item.get("dateline", ""),
        "provider": news_item.get("provider", ""),
        "category": news_item.get("category", []),
        "category_incident": news_item.get("category_incident", []),
        "byline": news_item.get("byline", ""),
        "provider_link_page": news_item.get("provider_link_page", ""),
        "printing_page": news_item.get("printing_page", ""),
    }
