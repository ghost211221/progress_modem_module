from queue import Empty

import eel

from back.consts.cmds.mri import operations
from back.context import Context
from back.queues import AnsQueue, TasksQueue
from back.utils import get_cmd_callbacks

from views.terminal import execute_operation


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

@eel.expose
def set_sms_number(tel_num):
    cmd = f'AT+CSCA="{tel_num}"'
    callbacks = get_cmd_callbacks('AT+CMGS')
    q.put((cmd, callbacks))

    cmd = f'AT+CSCA?'
    callbacks = get_cmd_callbacks('AT+CSCA')
    q.put((cmd, callbacks))

@eel.expose
def get_sms_text(sms_num):
    cmd = f'AT+CMGR={sms_num}'
    callbacks = get_cmd_callbacks('AT+CMGR')
    q.put((cmd, callbacks))

@eel.expose
def delete_sms(sms_num):
    cmd = f'AT+CMGD={sms_num}'
    callbacks = get_cmd_callbacks('AT+CMGD')
    q.put((cmd, callbacks))

    execute_operation('get_messages_list')

@eel.expose
def delete_all_sms():
    execute_operation('delete_all_sms')

@eel.expose
def disable_sms_alert():
    execute_operation('disable_sms_alert')

@eel.expose
def get_sms_list():
    execute_operation('get_messages_list')
