from queue import Empty
import time
import os

from datetime import datetime

import eel

from back.callbacks import stop_script_execution
from back.context import Context
from back.queues import TasksQueue, AnsQueue
from back.utils import get_log_msgs, get_cmd_callbacks


c = Context()
q = TasksQueue()
aq = AnsQueue()

def task_processing_worker():
    while not c.exit:
        try:
            cmd, callbacks = q.get(timeout=1)
            if cmd:
                c.device.send(cmd)
                ret = c.device.read()
                ret['cmd'] = cmd
                ret['datetime'] = str(datetime.now())
                ret['hex'] = ' '.join([str.encode(a).hex() for a in ret.get('ans', '')])
                eel.process_logs([ret,])
            if callbacks:
                for callback in callbacks:
                    if callback:
                        res = callback(cmd, ret)
                        if res:
                            eel.update_field(res)

            # aq.put(ret)
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

def script_running_worker():
    while not c.exit:
        if c.run_script:
            if not c.script_file:
                continue

            try:
                with open(os.path.join(c.scripts_folder, c.script_file)) as f:
                    cmds = f.readlines()

                c.device.set_timeout(c.script_port_timeout)
                iteration = 0
                while c.run_script and (c.script_iterations == 0 or iteration < c.script_iterations):
                    eel.set_iteration(iteration)
                    for cmd in cmds:
                        callbacks = get_cmd_callbacks(cmd)
                        q.put((cmd, callbacks))

                    iteration += 1

                # add stop script callback for end of script
                q.put((None, [stop_script_execution]))
            except Exception as e:
                print(e)

