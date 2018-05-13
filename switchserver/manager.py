from multiprocessing.managers import SyncManager

def getShared(host):
    manager = make_client_manager(host, 6000, "password")
    return manager

def make_client_manager(ip, port, authkey):

    class ServerQueueManager(SyncManager):
        pass

    ServerQueueManager.register("get_job_q")
    ServerQueueManager.register('syncdict')

    manager = ServerQueueManager(address=(ip, port), authkey=authkey)
    manager.connect()

    print
    'Client connected to %s:%s' % (ip, port)
    return manager