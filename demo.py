#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/20 21:03
# @Author  : 冉勇
# @Site    : 
# @File    : demo.py
# @Software: PyCharm
# @desc    :
import atomic_bomb_engine
import asyncio


async def batch_async():
  runner = atomic_bomb_engine.BatchRunner()
  runner.run(
    test_duration_secs=30,
    concurrent_requests=30,
    step_option=atomic_bomb_engine.step_option(increase_step=3, increase_interval=3),
    timeout_secs=15,
    cookie_store_enable=True,
    verbose=False,
    api_endpoints=[
      atomic_bomb_engine.endpoint(
        name="test-1",
        url="http://127.0.0.1:9099/docs",
        method="POST",
        json={"name": "test-1", "number": 1},
        weight=100,
        assert_options=[
          atomic_bomb_engine.assert_option(jsonpath="$.msg", reference_object="操作成功"),
        ],
      ),
    ])
  return runner


async def main():
  results = await batch_async()
  for res in results:
    if res.get("should_wait"):
      await asyncio.sleep(0.1)
    print(res)


if __name__ == '__main__':
  asyncio.run(main())
