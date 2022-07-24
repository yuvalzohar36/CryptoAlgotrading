import time
from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler


def add_scheduler_job(func, args, start_time):
    scheduler.add_job(
        func=func,
        args=args,
        trigger="date",
        run_date=start_time,
        name="new_indicator_job",
        misfire_grace_time=600,
        coalesce=True,
    )


def printOk():
    p =datetime.now().timestamp() + 60
    print(p)


scheduler = BackgroundScheduler()
b = datetime.now().timestamp() + 60.0
dt_obj = datetime.fromtimestamp(b)
add_scheduler_job(printOk, None, dt_obj)
scheduler.start()
time.sleep(80)
