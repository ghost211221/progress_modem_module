from queue import Empty
import time

import eel

from back.context import Context
from back.queues import TasksQueue, AnsQueue
from back.utils import get_log_msgs


c = Context()
q = TasksQueue()
aq = AnsQueue()

def task_processing_worker():
    while not c.exit:
        try:
            cmd, callbacks = q.get(timeout=1)
            c.device.send(cmd)
            ret = c.device.read()
            ret['cmd'] = cmd

            if callbacks:
                for callback in callbacks:
                    if callback:
                        res = callback(cmd, ret)
                        eel.update_field(res)

            aq.put(ret)
            time.sleep(1)
        except Empty:
            time.sleep(0.1)

def log_processing_worker():
    while not c.exit:
        data = get_log_msgs()
        if data:
            eel.process_logs(data)

        time.sleep(0.1);

def answers_processing_worker():
    while not c.exit:
        data = aq.get(timeout=1)
        if data:
            eel.process_answers(data)

        time.sleep(0.1);
