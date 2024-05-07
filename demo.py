#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/3/1 16:26
# @Author   : 冉勇
# @File     : test_001.py
# @Software : PyCharm
# @Desc     :
import asyncio

import atomic_bomb_engine
from apscheduler.schedulers.blocking import BlockingScheduler
from atomic_bomb_engine import server


@server.ui(port=8000)
async def run_batch():
    result = await atomic_bomb_engine.batch_async(
        # 测试持续时间
        test_duration_secs=60,
        # 并发量
        concurrent_requests=200,
        # 阶梯设置（每5秒增加30个并发）
        step_option=atomic_bomb_engine.step_option(increase_step=30, increase_interval=5),
        # 接口超时时间
        timeout_secs=10,
        # 是否开启客户端启用持久性cookie存储
        cookie_store_enable=True,
        # 全局初始化
        # setup_options=[
        #     atomic_bomb_engine.setup_option(
        #         name="初始化-1",
        #         url="https://www.baidu.com",
        #         method="get",
        #         jsonpath_extract=[
        #             atomic_bomb_engine.jsonpath_extract_option(key="test-msg", jsonpath="$.msg"),
        #             atomic_bomb_engine.jsonpath_extract_option(key="test-code", jsonpath="$.code"),
        #         ]
        #     )],
        # 是否开启详细日志
        verbose=False,
        # 被压接口设置
        api_endpoints=[
            atomic_bomb_engine.endpoint(
                # 接口任务命名
                name="test-1",
                # 针对每个接口初始化
                setup_options=[
                    atomic_bomb_engine.setup_option(
                        name="api-初始化-1",
                        url="https://www.baidu.com",
                        method="get",
                        jsonpath_extract=[
                            # atomic_bomb_engine.jsonpath_extract_option(key="api-test-msg-1", jsonpath="$.msg"),
                            # atomic_bomb_engine.jsonpath_extract_option(key="api-test-code-1", jsonpath="$.code"),
                        ]
                    )
                ],
                # 被压接口url
                url="https://www.baidu.com",
                # 请求方式
                method="get",
                # 权重
                weight=1,
                # 发送json请求
                json={"name": "{{api-test-msg-1}}", "number": 1},
                # 断言选项
                assert_options=[
                    atomic_bomb_engine.assert_option(jsonpath="$.number", reference_object=1),
                ],
                # 思考时间选项（在最大和最小之间随机，单位毫秒）
                think_time_option=atomic_bomb_engine.think_time_option(min_millis=500, max_millis=1200),
            ),
        ]
    )
    print(result)
    return result


scheduler = BlockingScheduler()
scheduler.add_job(run_batch, 'interval', minutes=1)
scheduler.start()

if __name__ == '__main__':
    asyncio.run(run_batch())

