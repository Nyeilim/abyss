import cv2
import json


# 计算图像的模糊度
# 拉普拉斯变换后的图像的方差越高, 通常表明图像越清晰
def calculate_blur(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var()


# 帧采样算法和帧缓冲
# 采样率越高, 缓冲数越小, 实时性越高
def frame_pick_and_cache():
    return


# 读取JSON配置文件
def read_config():
    with open('config.json', 'r') as config_file:
        data = json.load(config_file)

    return data
