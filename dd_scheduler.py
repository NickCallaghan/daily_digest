import threading
import schedule


class DailyDigestScheduler(threading.Thread):
    def __init__(self, digest):
        super().__init__()
        self.__stop_running = threading.Event()

    def schedule_digest(self, hour, minute):
        scheduler.clear()
        schedule.every().day.at(f"{hour}:{minute}").do(self.run_digest)

    def run(self):
        self.stop_running.clear()
        while not self.stop_running.is_set():
            schedule.run_pending()
            time.sleep(1)

    def stop(self):
        self.__stop_running.set()
