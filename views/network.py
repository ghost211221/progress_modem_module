from queue import Empty
import yaml
import os

import eel

from back.consts.cmds.mri import operations
from back.context import Context
from back.queues import AnsQueue, TasksQueue
from back.utils import get_cmd_callbacks


c = Context()
aq = AnsQueue()
q = TasksQueue()

@eel.expose
def e_get_cmds():
    return c.device.get_cmds()

@eel.expose
def get_log_msgs():
    data = []
    while not c.exit:
        try:
            data.append(aq.get(timeout=1))
        except Empty:
            break

    return data

@eel.expose
def execute_operation(op):
    ops_list = [v for v in dir(operations) if v[:2] != "__"]

    for op_t in ops_list:
        if op == op_t:
            ops = getattr(operations, op, None)
            if ops:
                for o in ops:
                    callbacks = get_cmd_callbacks(o)
                    q.put((o, callbacks))

                return

            raise Exception(f'Method {op} is not implemented')

@eel.expose
def save_cmds(cmds):
    c.device.set_cmds(cmds)

@eel.expose
def save_cmd_group(group_name, file_name):
    if not file_name:
        raise Exception('Не указано имя файла для сохранения')

    if not group_name:
        raise Exception('Не выбрано имя группы для сохранения')

    for group in c.device.cmds:
        if group.get('name', '') == group_name:
            if not os.path.exists('dumped'):
                os.mkdir('dumped')

            with open(f'dumped/{file_name}.yml', 'w') as f:
                yaml.dump(group, f)

@eel.expose
def register_operator(operator_code):
    if not operator_code:
        return

    cmd = f'AT+COPS=1,2"{operator_code}"'
    callbacks = get_cmd_callbacks('AT+COPS')
    q.put((cmd, callbacks))
