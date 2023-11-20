import asyncio
import random

# 全局变量
tts_texts = []

# 模仿模型处理流程
def model_procession():
    while True:
        tts_text = 'Hello, Class ' + str(random.randint(1, 10))
        print(tts_text)
        add_tts_task(tts_text)


def add_tts_task(text):
    asyncio.create_task(func(), name="创建的任务别名1")


def callback_func(task):
    # 回调函数, 希望 task 执行结束后执行
    print(task.result())


async def func():
    # 协程函数中有耗时操作直接 await 掉, 把 CPU 让给其他人
    await asyncio.sleep(2)  # 睡两秒, 模拟 IO 操作, CPU 给其他协程
    return "返回值"


async def main():
    task_list = [
        # 当这两个 Task 对象创建时, 对应的协程函数逻辑就被放入了事件循环中, 如果此时事件循环不存在会报错
        asyncio.create_task(func(), name="创建的任务别名1"),
        asyncio.create_task(func(), name="创建的任务别名2")
    ]

    # 将两个 Task 绑定回调函数, 回调函数在 Task 完成后自动执行
    task_list[0].add_done_callback(callback_func)
    task_list[1].add_done_callback(callback_func)

    # asyncio.wait 可以接受 Coroutines/Tasks 作为参数, 用于同时等待多个协程/任务的完成
    # await 等待列表任务的完成, timeout 为超时时间;
    # 超时后没完成的任务被放在 pending 中, 完成的被放在 done 中
    done, pending = await asyncio.wait(task_list, timeout=None)


# 创建并启动事件循环
asyncio.run(main())
