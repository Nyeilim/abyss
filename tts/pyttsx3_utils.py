import logging
import time

import pyttsx3

# 日志
LOGGER = logging.getLogger("tts")
LOGGER.setLevel(level=logging.INFO)  # INFO 级别以上的报错会被传递到 Handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # INFO 级别以上的报错会被输出到特定文件
LOGGER.addHandler(console_handler)  # 将处理器添加到日志器，指定日志输出的地方

# TTS 设置
# https://www.jb51.net/article/283155.htm
rate = 200  # 速率
volume = 0.9  # 音量
engine = pyttsx3.init()
engine.setProperty('rate', rate)
engine.setProperty('volume', volume)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # voices[0].id 是中文, voices[1].id 是英文


def say(text):
    # engine.say(text)
    # engine.runAndWait()
    # engine.stop()
    LOGGER.info(f"[TTS] speak: {text}")


# 监控进程的函数
def monitor(texts):
    while True:
        # 检查文本列表是否有数据
        if not texts.empty():
            # 从文本列表读取数据并处理
            text = texts.get()
            LOGGER.info(f"[TTS] pop text: {text}")
            say(text)
            LOGGER.info(f"[TTS] text left: {texts.qsize()}")
        else:
            # 如果文本列表为空，可以选择挂起一段时间再继续检查
            LOGGER.info(f"[TTS] sleeping...")
            time.sleep(1)
