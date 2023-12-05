import random
import multiprocessing
from pyttsx3_utils import texts, LOGGER, monitor_process

if __name__ == '__main__':
    # 创建并启动监控进程
    monitor_process = multiprocessing.Process(target=monitor_process)
    monitor_process.start()

    while True:
        tts_text = 'Hello, Class ' + str(random.randint(1, 10))
        LOGGER.info(f"Add Text: {tts_text}")
        texts.append(tts_text)
