from random import random
from typing import Optional

import numpy as np
import uvicorn
from fastapi import FastAPI, Query, HTTPException
from sklearn.metrics.pairwise import cosine_similarity

from dto.RecommendDTO import NewsRecommendationDTO_Req, recommend_news_similarity_InputData
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
@app.get("/news", response_model=List[Dict])
async def get_news():
    return await fetch_all_news(news_item_helper)

# retrun category of each news
@app.get("/news_category", response_model=List[Dict])
async def get_news_category():
    return await fetch_all_news(news_Category_helper)

# @app.get("/news_recommendation", response_model=List[Dict])
# async def get_news_recommendation(data : NewsRecommendationDTO_Req):
#     #할일 : 현재 어떤 사용자의 어떤 부분을 반영할지를 정하지 않음. 이부분을 다시 반영해야할듯.
#
#     result=fetch_all_news(news_Category_helper)
#     #할일 : 위의 결과를 처리해서 벡터만 있는 list로 변환해야함.
#
#     similar_item_indices, similar_item_scores= find_similar_items(data.user_category, result, top_n=data.num)
#
#     # 할일 : similar_item_indices로 뉴스 순서에 대한 검색을 진행해서 검색된 결과를 반환.
#
#     return

@app.post("/news/recommend/similarity")
async def recommend_news_similarity(input_data: recommend_news_similarity_InputData):
    news_data=await fetch_all_news(news_Category_helper);
    input_vector = np.array(input_data.category_array).reshape(1, -1)
    news_vectors = np.array([news['category_array'] for news in news_data])
    similarities = cosine_similarity(input_vector, news_vectors).flatten()
    similar_news = sorted(zip(news_data, similarities), key=lambda x: x[1], reverse=True)
    top_similar_news = similar_news[:input_data.top_n]
    return [
        {
            "news_id": news[0]["news_id"],
            "similarity": news[1]
        } for news in top_similar_news
    ]

@app.get("/news/{news_id}/")
async def get_news_by_id(news_id: str):
    # news_id를 기반으로 뉴스 데이터 검색
    for news in await fetch_all_news(news_item_helper):
        if news["news_id"] == news_id:
            return news
    raise HTTPException(status_code=404, detail="News not found")

# 사용자 카테고리 벡터와 뉴스 id를 기반으로 카테고리 벡터를 업데이트
# 뉴스 아이디에서 벡터 추출과정 추가해야됨.
@app.get("/news_user_update", response_model=UserUpdateDTO_Res)
async def get_news_recommendation(data: UserUpdateDTO_Req):
    response_data = UserUpdateDTO_Res(
        new_user_category=update_interest_vector(data.user_category, data.new_category)
    )
    return response_data





if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
