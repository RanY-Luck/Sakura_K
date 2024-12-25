#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/20 21:03
# @Author  : 冉勇
# @Site    : 
# @File    : demo.py
# @Software: PyCharm
# @desc    :
import asyncio
import atomic_bomb_engine
from atomic_bomb_engine import server


@server.ui(port=8000)
async def batch_async():
    runner = atomic_bomb_engine.BatchRunner()
    runner.run(
        # 测试持续时间
        test_duration_secs=5,
        # 并发量
        concurrent_requests=5,
        # 阶梯设置（每5秒增加30个并发）
        # step_option=atomic_bomb_engine.step_option(increase_step=5, increase_interval=5),
        # 接口超时时间
        timeout_secs=10,
        # 是否开启客户端启用持久性cookie存储
        cookie_store_enable=True,
        # 全局初始化
        # setup_options=[
        #     atomic_bomb_engine.setup_option(
        #       name="初始化-登录",
        #       url="http://127.0.0.1:9099/login",
        #       method="POST",
        #       form_data={"username": "admin", "password": "admin123", "code": "0", "uuid": "ranyong"},
        #       jsonpath_extract=[
        #         atomic_bomb_engine.jsonpath_extract_option(key="token", jsonpath="$.token")
        #       ]
        #     )
        # ],
        # 是否开启详细日志
        verbose=True,
        # 被压接口设置
        api_endpoints=[
            atomic_bomb_engine.endpoint(
                # 接口任务命名
                name="登录压测",
                # 针对每个接口初始化
                setup_options=[
                    atomic_bomb_engine.setup_option(
                        name="登录初始化",
                        url="http://127.0.0.1:9099/login",
                        method="POST",
                        form_data={"username": "admin", "password": "admin123", "code": "0", "uuid": "ranyong"},
                        jsonpath_extract=[
                          atomic_bomb_engine.jsonpath_extract_option(key="token", jsonpath="$.token"),
                        ]
                    )
                ],
                # 被压接口url
                url="http://127.0.0.1:9099/getInfo",
                # 请求方式
                method="GET",
                # 权重
                weight=1,
                # 发送json请求
                headers={"Authorization": f"Bearer {{token}}"},
                # 断言选项
                assert_options=[
                    atomic_bomb_engine.assert_option(jsonpath="$.msg", reference_object="操作成功"),
                ],
                # 思考时间选项（在最大和最小之间随机，单位毫秒）
                think_time_option=atomic_bomb_engine.think_time_option(min_millis=500, max_millis=1200),
            ),
        ]
    )
    return runner


if __name__ == '__main__':
    asyncio.run(batch_async())
