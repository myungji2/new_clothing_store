from PIL import Image
import os
import tqdm
from tqdm import tqdm
import numpy as np
import pickle
import os
import natsort
import cv2
file_path = './VITON-HD/test/cloth_mask'

file_names = os.listdir(file_path)
file_names = natsort.natsorted(file_names)


i = 1
a=1
for name in file_names:
    src = os.path.join(file_path, name)
    print(src)
    img_color = cv2.imread(src, 1)
    if img_color.shape[0] != 256 or img_color.shape[1] != 192:
        img_color = cv2.resize(img_color, (192, 256))
        cv2.imwrite(src, img_color)

    dst = str(i).zfill(4) + "_" + str(a) + '.jpg'
    dst = os.path.join(file_path, dst)
    os.rename(src, dst)
    print(dst)
    i += 1
    if a==4:
        a=1
    else:
        a+=1

file_path = './VITON-HD/test/cloth'

file_names = os.listdir(file_path)
file_names = natsort.natsorted(file_names)


i = 1
a=1
for name in file_names:
    src = os.path.join(file_path, name)
    print(src)
    img_color = cv2.imread(src, 1)
    if img_color.shape[0] != 256 or img_color.shape[1] != 192:
        img_color = cv2.resize(img_color, (192, 256))
        cv2.imwrite(src, img_color)

    dst = str(i).zfill(4) + "_" + str(a) + '.jpg'
    dst = os.path.join(file_path, dst)
    os.rename(src, dst)
    print(dst)
    i += 1
    if a==4:
        a=1
    else:
        a+=1

# 1번 디렉토리와 2번 디렉토리 경로
directory1 = './VITON-HD/test/cloth_mask'
directory2 = './VITON-HD/test/cloth'

# 1번 디렉토리의 이미지 파일 리스트
image_files1 = sorted([f for f in os.listdir(directory1) if os.path.isfile(os.path.join(directory1, f))])

# 2번 디렉토리의 이미지 파일 리스트
image_files2 = sorted([f for f in os.listdir(directory2) if os.path.isfile(os.path.join(directory2, f))])

# 이미지 파일 개수 확인
num_images = len(image_files1)

# 결과 이미지 이름 배열
result_image_names = []

# RGB 평균값 배열
rgb_averages_list = []

# 이미지 파일 순회
for i in tqdm(range(num_images)):
    # 1번 이미지 로드
    image1_path = os.path.join(directory1, image_files1[i])
    image1 = Image.open(image1_path).convert('RGB')

    # 2번 이미지 로드
    image2_path = os.path.join(directory2, image_files2[i])
    image2 = Image.open(image2_path).convert('RGB')

    # 이미지 크기 확인
    width, height = image1.size

    # 결과 이미지 생성
    result_image = Image.new('RGB', (width, height))

    # RGB 평균값 초기화
    r_sum, g_sum, b_sum = 0, 0, 0
    pixel_count = 0

    # 이미지 픽셀 반복
    for x in range(width):
        for y in range(height):
            # 1번 이미지에서 해당 픽셀 가져오기
            pixel1 = image1.getpixel((x, y))

            # 1번 이미지 픽셀이 흰색인 경우에만 2번 이미지에서 해당 픽셀 가져와 결과 이미지에 설정
            if pixel1 == (255, 255, 255):
                pixel2 = image2.getpixel((x, y))
                result_image.putpixel((x, y), pixel2)

                # RGB 값 더하기
                r_sum += pixel2[0]
                g_sum += pixel2[1]
                b_sum += pixel2[2]
                pixel_count += 1

    # 결과 이미지 저장

    result_image_names.append(image2_path)

    # RGB 평균값 계산
    r_average = r_sum // pixel_count
    g_average = g_sum // pixel_count
    b_average = b_sum // pixel_count
    rgb_averages_list.append([r_average, g_average, b_average])

# rgb_averages_file = 'rgb_averages.txt'
# with open(rgb_averages_file, 'w') as f:
#     for rgb_average in rgb_averages_list:
#         f.write(f'{rgb_average[0]},{rgb_average[1]},{rgb_average[2]}\n')

with open('rgb_averages2.pkl', 'wb') as f:
    pickle.dump(rgb_averages_list, f, protocol=pickle.HIGHEST_PROTOCOL)
with open('result_image_names2.pkl', 'wb') as f:
    pickle.dump(result_image_names, f, protocol=pickle.HIGHEST_PROTOCOL)
# # 결과 이미지 이름 리스트 저장
# result_image_names_file = 'result_image_names.txt'
# with open(result_image_names_file, 'w') as f:
#     for result_image_name in result_image_names:
#         f.write(f'{result_image_name}\n')
