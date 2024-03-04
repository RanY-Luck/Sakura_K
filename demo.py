#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/3/1 16:26
# @Author   : 冉勇
# @File     : demo.py
# @Software : PyCharm
# @Desc     :
import asyncio
import time

import atomic_bomb_engine


async def listen_for_messages():
    iterator = atomic_bomb_engine.StatusListenIter()
    for message in iterator:
        if message:
            print(message)
        else:
            await asyncio.sleep(0.3)


async def run_performance_test():
    print("开始压测")
    result = await atomic_bomb_engine.run_async(
        url="http://127.0.0.1:9000/docs",
        method="GET",
        test_duration_secs=300,
        concurrent_requests=200,
        timeout_secs=10,
        verbose=False,
        should_prevent=True,
        assert_options=[atomic_bomb_engine.assert_option("$.code", 200)]
    )
    print(time.ctime(), result)


async def main():
    await asyncio.gather(
        listen_for_messages(),
        run_performance_test(),
    )


if __name__ == "__main__":
    asyncio.run(main())
