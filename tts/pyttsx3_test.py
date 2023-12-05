import random
import multiprocessing
import time
from pyttsx3_utils import LOGGER, monitor

if __name__ == '__main__':
    # 全局列表，用于存储来自其他进程的数据，注意普通的 queue.Queue 是不能在进程间共享的
    texts = multiprocessing.Queue()

    # 创建并启动监控进程
    monitor_process = multiprocessing.Process(target=monitor, args=(texts,))
    monitor_process.start()

    while True:
        tts_text = 'Hello, Class ' + str(random.randint(1, 2))
        LOGGER.info(f"[MAIN] add text: {tts_text}")
        texts.put(tts_text)
        LOGGER.info(f"[MAIN] text count: {texts.qsize()}")
        time.sleep(0.05)
