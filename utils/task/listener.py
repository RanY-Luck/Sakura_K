import datetime
import json

import pytz
from apscheduler.events import JobExecutionEvent

from application.settings import SCHEDULER_TASK_RECORD, SCHEDULER_TASK
from core.logger import logger
from utils.task.Mongo import get_database


def before_job_execution(event: JobExecutionEvent):
    shanghai_tz = pytz.timezone("Asia/Shanghai")
    start_time: datetime.datetime = event.scheduled_run_time.astimezone(shanghai_tz)
    end_time = datetime.datetime.now(shanghai_tz)
    process_time = (end_time - start_time).total_seconds()
    job_id = event.job_id
    if "-temp-" in job_id:
        job_id = job_id.split("-")[0]
    result = {
        "job_id": job_id,
        "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
        "process_time": process_time,
        "retval": json.dumps(event.retval),
        "exception": json.dumps(event.exception),
        "traceback": json.dumps(event.traceback)
    }
    db = get_database()
    try:
        task = db.get_data(SCHEDULER_TASK, job_id, is_object_id=True)
        result["job_class"] = task.get("job_class", None)
        result["name"] = task.get("name", None)
        result["group"] = task.get("group", None)
        result["exec_strategy"] = task.get("exec_strategy", None)
        result["expression"] = task.get("expression", None)
    except ValueError as e:
        result["expression"] = str(e)
        logger.error(f"任务编号：{event.job_id}，报错：{e}")
    db.create_data(SCHEDULER_TASK_RECORD, result)
