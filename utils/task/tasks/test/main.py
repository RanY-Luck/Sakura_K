import datetime
import time


class Test:

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def main(self) -> str:
        """
        主入口函数

        :return:
        """
        print(f'{datetime.datetime.now()}, 定时任务测试实例，参数为: {self.name}, {self.age}')
        time.sleep(3)
        return '任务执行完成'
