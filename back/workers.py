from queue import Empty
import time

from datetime import datetime

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
            ret['datetime'] = str(datetime.now())
            ret['hex'] = ' '.join([str.encode(a).hex() for a in ret.get('ans', '')])

            if callbacks:
                for callback in callbacks:
                    if callback:
                        res = callback(cmd, ret)
                        if res:
                            eel.update_field(res)

            aq.put(ret)
            time.sleep(0.1)
        except Empty:
            time.sleep(0.1)

def log_processing_worker():
    while not c.exit:
        try:
            data = get_log_msgs()
            if data:
                eel.process_logs(data)
        except Empty:
            pass

        time.sleep(0.1);

def answers_processing_worker():
    while not c.exit:
        try:
            data = aq.get(timeout=1)
            if data:
                eel.process_answers(data)
            time.sleep(0.1);
        except Empty:
            time.sleep(0.1);
