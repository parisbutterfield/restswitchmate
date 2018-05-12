import Queue
from multiprocessing.managers import SyncManager


class MyManager(SyncManager):
    pass


syncdict = {}
job_q = Queue.Queue()

def get_dict():
    return syncdict

if __name__ == "__main__":
    MyManager.register("syncdict", get_dict)
    MyManager.register("get_job_q", callable=lambda: job_q)
    manager = MyManager(("0.0.0.0", 6000), authkey="password")
    manager.start()
    manager.join()
