import cv2
import requests
import numpy as np
import mytools as util

# 获取配置
data = util.read_config()

# 后端服务器的URL
backend_url = "http://{}:{}/{}".format(
    data["backend_server_host"],
    data["backend_server_port"],
    data["capture_url"]
)

# 根据设备号捕获摄像头画面
cap = cv2.VideoCapture(0)

while True:
    # 从摄像头捕获画面
    ret, frame = cap.read()

    # 将捕获的帧编码为JPEG格式
    _, img_encoded = cv2.imencode('.jpg', frame)

    # 将图像数据转换为字节流
    image_data = img_encoded.tobytes()

    # # 发送图像数据到后端服务器
    # response = requests.post(backend_url, data=image_data)

    # 在窗口中显示捕获的画面（可选）
    cv2.imshow('Camera Feed', frame)

    # 按下'q'键退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头资源和关闭窗口
cap.release()
cv2.destroyAllWindows()
