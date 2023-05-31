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
def get_phones_list():
    execute_operation('get_phones_list')

@eel.expose
def update_phone_record(phone_number, phone_name):
    if not phone_number or phone_name is None:
        return

    cmd = f'AT+CPBS="SM"'
    callbacks = get_cmd_callbacks('AT+CPBS')
    q.put((cmd, callbacks))

    cmd = f'AT+CPBW=1,"{phone_number}",,"{phone_name}"'
    callbacks = get_cmd_callbacks('AT+CPBW')
    q.put((cmd, callbacks))

    execute_operation('get_phones_list')

@eel.expose
def add_phone_record(phone_number, phone_name):
    if not phone_number or phone_name is None:
        return

    cmd = f'AT+CPBS="SM"'
    callbacks = get_cmd_callbacks('AT+CPBS')
    q.put((cmd, callbacks))

    cmd = f'AT+CPBW=,"{phone_number}",,"{phone_name}"'
    callbacks = get_cmd_callbacks('AT+CPBW')
    q.put((cmd, callbacks))

    execute_operation('get_phones_list')

@eel.expose
def delete_phone_record(pos):
    if not pos:
        return

    cmd = f'AT+CPBS="SM"'
    callbacks = get_cmd_callbacks('AT+CPBS')
    q.put((cmd, callbacks))

    cmd = f'AT+CPBW={pos}'
    callbacks = get_cmd_callbacks('AT+CPBW')
    q.put((cmd, callbacks))

    execute_operation('get_phones_list')

@eel.expose
def get_calls_list():
    execute_operation('get_calls_list')
