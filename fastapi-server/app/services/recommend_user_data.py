# 유저의 관심 카테고리 업데이트
import numpy as np
from sklearn.neighbors import NearestNeighbors


#update interest Category
def update_interest_vector(interest_vector, new_interests, increment=0.1, decrement=0.1):
    interest_vector = np.array(interest_vector)  # numpy 배열로 변환
    new_interests = np.array(new_interests)  # numpy 배열로 변환

    for i in range(len(new_interests)):
        if new_interests[i] == 1:
            interest_vector[i] += increment

    interest_vector = np.minimum(interest_vector, 1.0)

    for i in range(len(interest_vector)):
        if new_interests[i] == 0:
            interest_vector[i] = (interest_vector[i] - decrement) ** 2

    return [round(value, 2) for value in interest_vector.tolist()]


# user_based recommendation, content_based recommendation
def combine_vectors(keyword_vector, field_vector, media_vector):
    keyword_vector_squared = np.square(keyword_vector)
    field_vector_squared = np.square(field_vector)
    media_vector_squared = np.square(media_vector)
    return np.concatenate((keyword_vector, field_vector, media_vector))


def find_similar_items(target_item_vectors, all_item_vectors, top_n=5):
    combined_all_item_vectors = [combine_vectors(*item_vectors) for item_vectors in all_item_vectors]
    combined_target_item_vector = combine_vectors(*target_item_vectors)

    nbrs = NearestNeighbors(n_neighbors=top_n, algorithm='auto', metric='cosine').fit(combined_all_item_vectors)
    distances, indices = nbrs.kneighbors([combined_target_item_vector])
    similar_item_scores = 1 - distances[0]

    return indices[0], similar_item_scores

# ------update_interest_vector 사용예시

# interest_vector = np.array([1.0, 0.5, 0.8])
# new_interests = np.array([0, 1, 0])
# interest_vector = update_interest_vector(interest_vector, new_interests)
# print(interest_vector)  # [0.81, 0.6, 0.49]

# new_interests = np.array([1, 0, 1])
# interest_vector = update_interest_vector(interest_vector, new_interests)
# print(interest_vector)  # [0.91, 0.25, 0.59]


#------combine_vectors, find_similar_items 사용예시
# target_keyword_vector = np.random.rand(5)
# target_field_vector = np.random.rand(3)
# target_media_vector = np.random.rand(4)

# all_item_vectors = [
#     (np.random.rand(5), np.random.rand(3), np.random.rand(4)) for _ in range(1000)
# ]

# similar_item_indices, similar_item_scores = find_similar_items(
#     (target_keyword_vector, target_field_vector, target_media_vector),
#     all_item_vectors,
#     top_n=5
# )

# print("유사한 아이템 인덱스 (유사도 순):", similar_item_indices)
# print("유사한 아이템들의 유사도 점수:", similar_item_scores)

# target_keyword_vector = np.random.rand(5)
# target_field_vector = np.random.rand(3)
# target_media_vector = np.random.rand(4)

# all_item_vectors = [
#     (np.random.rand(5), np.random.rand(3), np.random.rand(4)) for _ in range(1000)
# ]

# similar_item_indices, similar_item_scores = find_similar_items(
#     (target_keyword_vector, target_field_vector, target_media_vector),
#     all_item_vectors,
#     top_n=5
# )

# print("유사한 아이템 인덱스 (유사도 순):", similar_item_indices)
# print("유사한 아이템들의 유사도 점수:", similar_item_scores)
