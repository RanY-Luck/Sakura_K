#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/5 11:42
# @Author  : 冉勇
# @Site    :
# @File    : get_scheduler.py
# @Software: PyCharm
# @desc    : 定时任务相关操作
import json
import module_task  # noqa: F401
from apscheduler.events import EVENT_ALL
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Union
from config.database import AsyncSessionLocal, quote_plus
from config.env import DataBaseConfig, RedisConfig
from module_admin.dao.job_dao import JobDao
from module_admin.entity.vo.job_vo import JobLogModel, JobModel
from module_admin.service.job_log_service import JobLogService
from utils.log_util import logger


# 重写Cron定时
class MyCronTrigger(CronTrigger):
    @classmethod
    def from_crontab(cls, expr: str, timezone=None):
        values = expr.split()
        if len(values) != 6 and len(values) != 7:
            raise ValueError('Wrong number of fields; got {}, expected 6 or 7'.format(len(values)))

        second = values[0]
        minute = values[1]
        hour = values[2]
        if '?' in values[3]:
            day = None
        elif 'L' in values[5]:
            day = f"last {values[5].replace('L', '')}"
        elif 'W' in values[3]:
            day = cls.__find_recent_workday(int(values[3].split('W')[0]))
        else:
            day = values[3].replace('L', 'last')
        month = values[4]
        if '?' in values[5] or 'L' in values[5]:
            week = None
        elif '#' in values[5]:
            week = int(values[5].split('#')[1])
        else:
            week = values[5]
        if '#' in values[5]:
            day_of_week = int(values[5].split('#')[0]) - 1
        else:
            day_of_week = None
        year = values[6] if len(values) == 7 else None
        return cls(
            second=second,
            minute=minute,
            hour=hour,
            day=day,
            month=month,
            week=week,
            day_of_week=day_of_week,
            year=year,
            timezone=timezone,
        )

    @classmethod
    def __find_recent_workday(cls, day: int):
        now = datetime.now()
        date = datetime(now.year, now.month, day)
        if date.weekday() < 5:
            return date.day
        else:
            diff = 1
            while True:
                previous_day = date - timedelta(days=diff)
                if previous_day.weekday() < 5:
                    return previous_day.day
                else:
                    diff += 1


SQLALCHEMY_DATABASE_URL = (
    f'mysql+pymysql://{DataBaseConfig.db_username}:{quote_plus(DataBaseConfig.db_password)}@'
    f'{DataBaseConfig.db_host}:{DataBaseConfig.db_port}/{DataBaseConfig.db_database}'
)
if DataBaseConfig.db_type == 'postgresql':
    SQLALCHEMY_DATABASE_URL = (
        f'postgresql+psycopg2://{DataBaseConfig.db_username}:{quote_plus(DataBaseConfig.db_password)}@'
        f'{DataBaseConfig.db_host}:{DataBaseConfig.db_port}/{DataBaseConfig.db_database}'
    )
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=DataBaseConfig.db_echo,
    max_overflow=DataBaseConfig.db_max_overflow,
    pool_size=DataBaseConfig.db_pool_size,
    pool_recycle=DataBaseConfig.db_pool_recycle,
    pool_timeout=DataBaseConfig.db_pool_timeout,
)
# 数据库连接
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 任务存储
job_stores = {
    'default': MemoryJobStore(),  # 默认内存存储
    'sqlalchemy': SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URL, engine=engine),  # 数据库存储
    'redis': RedisJobStore(
        **dict(
            host=RedisConfig.redis_host,
            port=RedisConfig.redis_port,
            username=RedisConfig.redis_username,
            password=RedisConfig.redis_password,
            db=RedisConfig.redis_database,
        )
    )  # redis存储
}
# 配置调度器的执行器和任务默认设置
# 线程池执行器
executors = {'default': ThreadPoolExecutor(20), 'processpool': ProcessPoolExecutor(5)}
# 任务默认设置
job_defaults = {'coalesce': False, 'max_instance': 1}
# 实例化调度器
scheduler = BackgroundScheduler()
# 配置调度器
scheduler.configure(jobstores=job_stores, executors=executors, job_defaults=job_defaults)


class SchedulerUtil:
    """
    定时任务相关方法
    """

    @classmethod
    async def init_system_scheduler(cls):
        """
        应用启动时初始化定时任务

        :return:
        """
        logger.info('开始启动定时任务...')
        # 启动定时任务
        scheduler.start()
        # 加载系统定时任务
        async with AsyncSessionLocal() as session:
            # 获取系统定时任务列表
            job_list = await JobDao.get_job_list_for_scheduler(session)
            # 移除系统定时任务
            for item in job_list:
                # 移除原有任务
                query_job = cls.get_scheduler_job(job_id=str(item.job_id))
                # 移除原有任务
                if query_job:
                    # 移除原有任务
                    cls.remove_scheduler_job(job_id=str(item.job_id))
                # 重新添加任务
                cls.add_scheduler_job(item)
        # 启动任务
        scheduler.add_listener(cls.scheduler_event_listener, EVENT_ALL)
        logger.info('系统初始定时任务加载成功')

    @classmethod
    async def close_system_scheduler(cls):
        """
        应用关闭时关闭定时任务

        :return:
        """
        # 关闭定时任务
        scheduler.shutdown()
        logger.info('关闭定时任务成功')

    @classmethod
    def get_scheduler_job(cls, job_id: Union[str, int]):
        """
        根据任务id获取任务对象

        :param job_id: 任务id
        :return: 任务对象
        """
        # 任务id转字符串
        query_job = scheduler.get_job(job_id=str(job_id))

        return query_job

    @classmethod
    def add_scheduler_job(cls, job_info: JobModel):
        """
        根据输入的任务对象信息添加任务

        :param job_info: 任务对象信息
        :return:
        """
        # 构造任务对象
        scheduler.add_job(
            # 任务执行函数
            func=eval(job_info.invoke_target),
            # 任务触发器
            trigger=MyCronTrigger.from_crontab(job_info.cron_expression),
            # 任务参数
            args=job_info.job_args.split(',') if job_info.job_args else None,
            # 任务关键字参数
            kwargs=json.loads(job_info.job_kwargs) if job_info.job_kwargs else None,
            # 任务id
            id=str(job_info.job_id),
            # 任务名称
            name=job_info.job_name,
            # 任务异常处理策略
            misfire_grace_time=1000000000000 if job_info.misfire_policy == '3' else None,
            # 任务并发策略
            coalesce=True if job_info.misfire_policy == '2' else False,
            # 任务最大实例数
            max_instances=3 if job_info.concurrent == '0' else 1,
            # 任务存储
            jobstore=job_info.job_group,
            # 任务执行器
            executor=job_info.job_executor
        )

    @classmethod
    def execute_scheduler_job_once(cls, job_info: JobModel):
        """
        根据输入的任务对象执行一次任务

        :param job_info: 任务对象信息
        :return:
        """
        # 构造任务对象
        scheduler.add_job(
            # 任务执行函数
            func=eval(job_info.invoke_target),
            # 任务触发器
            trigger='date',
            # 任务执行时间
            run_date=datetime.now() + timedelta(seconds=1),
            # 任务参数
            args=job_info.job_args.split(',') if job_info.job_args else None,
            # 任务关键字参数
            kwargs=json.loads(job_info.job_kwargs) if job_info.job_kwargs else None,
            # 任务id
            id=str(job_info.job_id),
            # 任务名称
            name=job_info.job_name,
            # 任务异常处理策略
            misfire_grace_time=1000000000000 if job_info.misfire_policy == '3' else None,
            # 任务并发策略
            coalesce=True if job_info.misfire_policy == '2' else False,
            # 任务最大实例数
            max_instances=3 if job_info.concurrent == '0' else 1,
            # 任务存储
            jobstore=job_info.job_group,
            # 任务执行器
            executor=job_info.job_executor
        )

    @classmethod
    def remove_scheduler_job(cls, job_id: Union[str, int]):
        """
        根据任务id移除任务

        :param job_id: 任务id
        :return:
        """
        scheduler.remove_job(job_id=str(job_id))

    @classmethod
    def scheduler_event_listener(cls, event):
        # 获取事件类型
        event_type = event.__class__.__name__
        # 获取任务状态
        status = '0'
        # 获取异常信息
        exception_info = ''
        # 获取任务id
        if event_type == 'JobExecutionEvent' and event.exception:
            # 任务执行异常
            exception_info = str(event.exception)
            # 任务执行失败
            status = '1'
        # 获取任务信息
        if hasattr(event, 'job_id'):
            # 任务执行成功
            job_id = event.job_id
            # 获取任务对象
            query_job = cls.get_scheduler_job(job_id=job_id)
            # 获取任务信息
            if query_job:
                # 获取任务信息
                query_job_info = query_job.__getstate__()
                # 获取任务名称
                job_name = query_job_info.get('name')
                # 获取任务组名
                job_group = query_job._jobstore_alias
                # 获取任务执行器
                job_executor = query_job_info.get('executor')
                # 获取调用目标字符串
                invoke_target = query_job_info.get('func')
                # 获取调用函数位置参数
                job_args = ','.join(query_job_info.get('args'))
                # 获取调用函数关键字参数
                job_kwargs = json.dumps(query_job_info.get('kwargs'))
                # 获取任务触发器
                job_trigger = str(query_job_info.get('trigger'))
                # 构造日志消息
                job_message = f"事件类型: {event_type}, 任务ID: {job_id}, 任务名称: {job_name}, 执行于{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                # 保存任务日志
                job_log = JobLogModel(
                    # 任务名称
                    jobName=job_name,
                    # 任务组名
                    jobGroup=job_group,
                    # 任务执行器
                    jobExecutor=job_executor,
                    # 调用目标字符串
                    invokeTarget=invoke_target,
                    # 调用函数位置参数
                    jobArgs=job_args,
                    # 调用函数关键字参数
                    jobKwargs=job_kwargs,
                    # 任务触发器
                    jobTrigger=job_trigger,
                    # 任务状态
                    jobMessage=job_message,
                    # 任务状态
                    status=status,
                    # 异常信息
                    exceptionInfo=exception_info,
                    # 创建时间
                    createTime=datetime.now()
                )
                # 保存任务日志
                session = SessionLocal()
                # 保存任务日志
                JobLogService.add_job_log_services(session, job_log)
                # 关闭数据库连接
                session.close()
