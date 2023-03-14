from queue import Empty

import eel

from back.consts.cmds.mri import operations
from back.context import Context
from back.queues import AnsQueue, TasksQueue
from back.utils import get_cmd_callbacks


c = Context()
aq = AnsQueue()
q = TasksQueue()

@eel.expose
def send_sms(phone_number, text):
    ops_list = [v for v in dir(operations) if v[:2] != "__"]

    for op_t in ops_list:
        if op_t == 'send_sms':
            ops = getattr(operations, op_t, [])
            if ops:
                for o in ops:
                    callbacks = get_cmd_callbacks(o)
                    q.put((o, callbacks))
                cmd = f'AT+CMGS="{phone_number}"\r'
                callbacks = get_cmd_callbacks('AT+CMGS')
                q.put((cmd, callbacks))
                cmd = f'{text}\x1A'  # ctrl + Z for terminator
                callbacks = get_cmd_callbacks([])
                q.put((cmd, callbacks))

                return

            raise Exception(f'Method {op_t} is not implemented')