from queue import Empty
import yaml
import os

import eel

from back.context import Context
from back.queues import AnsQueue, TasksQueue
from back.utils import get_cmd_callbacks

from views.terminal import execute_operation


c = Context()
aq = AnsQueue()
q = TasksQueue()


@eel.expose
def select_operator(operator_code):
    if not operator_code:
        return

    cmd = f'AT+COPS?'
    callbacks = get_cmd_callbacks('AT+COPS')
    q.put((cmd, callbacks))

    cmd = f'AT+COPS=1,2,"{operator_code}"'
    callbacks = get_cmd_callbacks('AT+COPS')
    q.put((cmd, callbacks))

    execute_operation('select_operator')

@eel.expose
def deselect_operator():
    execute_operation('deregister_operator')

@eel.expose
def autoselect_operator():
    execute_operation('auto_set_operator')