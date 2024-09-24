import random
from typing import Optional

import numpy as np
import uvicorn
from fastapi import FastAPI, Query, HTTPException
from sklearn.metrics.pairwise import cosine_similarity

from dto.RecommendDTO import NewsRecommendationDTO_Req, recommend_news_similarity_InputData, \
    recommend_news_random_InputData, recommend_user_similarity_InputData, NewsById_Req
from services.recommend_user_data import update_interest_vector, find_similar_items
from dto.userCategory import UserUpdateDTO_Res, UserUpdateDTO_Req
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
# clear : (전체 뉴스 조회)
@app.get("/news", response_model=List[Dict])
async def get_news():
    return await fetch_all_news(news_item_helper)

# retrun category of each news
# clear : (전체 뉴스 카테고리(index) 조회)
@app.get("/news_category", response_model=List[Dict])
async def get_news_category():
    return await fetch_all_news(news_Category_helper)

# clear : 사용자 과심카테고리(index)를 바탕으로 content-based 추천방식
@app.post("/news/content/similarity_recommend")
async def recommend_news_similarity(input_data: recommend_news_similarity_InputData):
    news_data=await fetch_all_news(news_Category_helper);
    input_vector = np.array(input_data.category_array).reshape(1, -1)
    news_vectors = np.array([news['category_array'] for news in news_data])
    similarities = cosine_similarity(input_vector, news_vectors).flatten()
    # 뉴스 데이터와 유사도 값을 함께 묶어서 정렬
    similar_news = sorted(zip(news_data, similarities), key=lambda x: x[1], reverse=True)

    # 중복된 news_id를 체크하기 위한 집합
    seen_ids = set()
    top_similar_news = []

    for news in similar_news:
        news_id = news[0]["news_id"]
        if news_id not in seen_ids:
            seen_ids.add(news_id)  # news_id를 추가
            top_similar_news.append({
                "news_id": news_id,
                "similarity": news[1]
            })
        # top_n 개수만큼만 유지
        if len(top_similar_news) >= input_data.top_n:
            break

    return top_similar_news
# clear : 랜덤하게 지정된 개수만큼 뉴스를 반환.
@app.post("/news/content/random_recommend")
async def recommend_news_random(input_data: recommend_news_random_InputData):
    news_data = await fetch_all_news(news_Category_helper)

    # 중복을 방지하기 위한 집합
    seen_ids = set()
    random_news = []

    # 모든 뉴스 데이터에서 중복 없이 랜덤 샘플링
    while len(random_news) < input_data.top_n and len(seen_ids) < len(news_data):
        news = random.choice(news_data)  # 랜덤으로 뉴스 선택
        if news["news_id"] not in seen_ids:
            seen_ids.add(news["news_id"])  # news_id를 추가
            random_news.append(news)  # 뉴스 추가

    return [
        {
            "news_id": news["news_id"]
        } for news in random_news
    ]
@app.post("/news/content/user_recommend")
async def recommend_user_similarity(input_data: recommend_user_similarity_InputData):
    user_vector = np.array(input_data.user_list).reshape(1, -1)
    user_record_vectors = np.array(input_data.user_record_list)

    similarities = cosine_similarity(user_vector, user_record_vectors).flatten()
    most_similar_user_indices = np.argsort(similarities)[::-1]
    similar_users = [
        {
            "user_index": int(index),
            "similarity": float(similarities[index])
        } for index in most_similar_user_indices
    ]

    return similar_users

# clear : 특정 뉴스 id 를 기반으로 뉴스 탐색.
@app.get("/news/{news_id}/")
async def get_news_by_id(news_id: str):
    # news_id를 기반으로 뉴스 데이터 검색
    for news in await fetch_all_news(news_item_helper):
        if news["news_id"] == news_id:
            return news
    raise HTTPException(status_code=404, detail="News not found")

@app.post("/news/news_ids")
async def get_news_by_ids(data : NewsById_Req):
    print(data)
    # news_ids를 기반으로 뉴스 데이터 검색
    all_news = await fetch_all_news(news_item_helper)
    found_news = []

    for newsID in data.news_ids:
        for news in all_news:
            if news["news_id"] == newsID:
                found_news.append(news)
                break

    if not found_news:
        raise HTTPException(status_code=404, detail="No news found for the given IDs")

    return found_news


# 사용자 카테고리 벡터와 뉴스 id를 기반으로 카테고리 벡터를 업데이트
# clear
@app.post("/user_category_update", response_model=UserUpdateDTO_Res)
async def get_news_recommendation(data: UserUpdateDTO_Req):
    for news in await fetch_all_news(news_Category_helper):
        if news["news_id"] == data.news_id:
            temp = new_user_category=update_interest_vector(data.user_category, news["category_array"])
            response_data = UserUpdateDTO_Res(
                news_user_category=temp
            )
            return response_data
    raise HTTPException(status_code=404, detail="News not found")









if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
