import asyncio
import random

from edge_tts_utils import gen_ssml
from edge_tts_utils import get_tts_text
from edge_tts_utils import put_tts_text
from edge_tts_utils import transfer_data
from edge_tts_utils import LOGGER


# 模仿模型处理流程
def model_procession():
    while True:
        tts_text = 'Hello, Class ' + str(random.randint(1, 10))
        LOGGER.info(f"tts text: {tts_text}")
        put_tts_text(tts_text)


async def main_seq():
    while True:
        # 持续获取标签文本
        LOGGER.info("continue next loop")
        tts_text = get_tts_text()
        if tts_text is None:
            continue

        LOGGER.info("send request")
        ssml = gen_ssml(tts_text)
        await transfer_data(ssml)  # 发起请求


# main
if __name__ == '__main__':
    LOGGER.info("test")
    # asyncio.run(main_seq())
    # model_procession()
