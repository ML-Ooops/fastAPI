from typing import List, Dict
import uvicorn
from fastapi import FastAPI, Query, HTTPException

from models.category import NewsItemCategory
from services.recommend import (
    recommend_news,
    recommend_popular_news,
    recommend_based_on_demographics,
    recommend_based_on_new_words,
    recommend_for_job_seekers
)
from services.news_category_jsonStructure import *

from services.searchNews import fetch_all_news

app = FastAPI()

@app.get("/recommend")
def recommend(user_id: str):
    recommendations = recommend_news(user_id)
    return {"recommendations": recommendations}

@app.get("/recommend/popular")
def popular():
    recommendations = recommend_popular_news()
    return {"recommendations": recommendations}

@app.get("/recommend/demographics")
def demographics(gender: str, age_group: str):
    recommendations = recommend_based_on_demographics(gender, age_group)
    return {"recommendations": recommendations}

@app.get("/recommend/new-words")
def new_words():
    recommendations = recommend_based_on_new_words()
    return {"recommendations": recommendations}

@app.get("/recommend/job-seekers")
def job_seekers():
    recommendations = recommend_for_job_seekers()
    return {"recommendations": recommendations}

# return all news
@app.get("/news", response_model=List[Dict])
async def get_news():
    return await fetch_all_news(news_item_helper)

@app.get("/news_category", response_model=List[Dict])
async def get_news_category():
    return await fetch_all_news(news_Category_helper)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
