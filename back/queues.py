from queue import Queue


class TasksQueue():
    """Tasks queue.
    Each element is 2 elements tuple:
    - string - AT command
    - func - callback
    """
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(TasksQueue, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.__queue = Queue()

    def put(self, data, timeout=1):
        self.__queue.put(data, timeout=timeout)

    def get(self, timeout=1):
        return self.__queue.get(timeout=timeout)

    def clear(self):
        with self.__queue.mutex:
            self.__queue.queue.clear()

class AnsQueue():
    """Deivce answers queue
    """
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(AnsQueue, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.__queue = Queue()

    def put(self, data, timeout=1):
        self.__queue.put(data, timeout=timeout)

    def get(self, timeout=1):
        return self.__queue.get(timeout=timeout)