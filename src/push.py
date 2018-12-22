from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler


def pushList():
    print('The current time is:', datetime.now())
