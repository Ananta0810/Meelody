class Timer:
    timeShutDownInSec: int
    timeCounterInSec: float
    intervalInSec: float

    def __init__(
        self,
        intervalInSec=0.25,
        time_shutdown_in_sec=0,
        timeCounterInSec=0,
    ):
        self.intervalInSec = intervalInSec
        self.timeShutDownInSec = time_shutdown_in_sec
        self.timeCounterInSec = timeCounterInSec

    def setInterval(self, interval):
        self.intervalInSec = interval

    def setTime(self, time):
        self.timeShutDownInSec = time

    def isEnabled(self):
        return self.timeShutDownInSec != 0

    def count(self):
        self.timeCounterInSec += self.intervalInSec

    def isActive(self):
        return self.timeShutDownInSec <= self.timeCounterInSec

    def reset(self):
        self.timeShutDownInSec = 0
        self.timeCounterInSec = 0
