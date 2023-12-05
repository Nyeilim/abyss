import random
import threading
from pyttsx3_utils import texts, LOGGER, monitor

if __name__ == '__main__':
    # 创建并启动监控线程
    monitor_thread = threading.Thread(target=monitor)
    monitor_thread.start()

    while True:
        tts_text = 'Hello, Class ' + str(random.randint(1, 2))
        LOGGER.info(f"Add Text: {tts_text}")
        texts.append(tts_text)
