import pickle
from sklearn.neighbors import NearestNeighbors
import numpy as np
import cv2


def smilar_images(rgb):
    with open("./result_image_names2.pkl","rb") as fr:
        names = pickle.load(fr)

    with open("./rgb_averages2.pkl","rb") as fr:
        avs = pickle.load(fr)
    # print(avs)
    def replace_char_in_list(lst, target_char, replacement_char):
        new_lst = [s.replace(target_char, replacement_char) for s in lst]
        return new_lst

    names = replace_char_in_list(names, "\\", "/")

    k_neighbors = 13

    # 이미지들의 평균 RGB 값 배열로 변환
    X = np.array(avs)

    # KNN 모델 훈련
    knn = NearestNeighbors(n_neighbors=k_neighbors)
    knn.fit(X)
    distances, indices = knn.kneighbors(rgb)
    similar_images = indices[0][1:]
    similar_file_names = [names[index] for index in similar_images]
    print(f"Similar images: {similar_file_names}")

    return similar_file_names

    # 유사한 사진 목록 출력
    # for i, image_rgb_average in enumerate(avs):
    #     distances, indices = knn.kneighbors([image_rgb_average])
    #     similar_images = indices[0][1:]
    #     similar_file_names = [names[index] for index in similar_images]
    #     print(f"Similar images for {names[i]}: {similar_file_names}")
