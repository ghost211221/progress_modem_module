import yaml
from queue import Empty

import serial.tools.list_ports

import back.callbacks as callbacks
from back.context import Context
from back.consts.cmds.mri.map_cmd_callback import CMDS
from back.queues import AnsQueue

c = Context()
aq = AnsQueue()

def get_comports_list():
    coms = []
    for com in sorted(serial.tools.list_ports.comports(), reverse=True, key=lambda d: d.name):
        coms.append({'name': com.name, 'description': com.description})

    return coms

def comport_pars():
    with open('data/com_pars.yml') as f:
        parameters = yaml.safe_load(f)

        return parameters

def get_cmd_callbacks(cmd):
    callbacks = []
    for item in CMDS:
        if item.get('cmd') in cmd:
            callbacks.append(getattr(callbacks, item.get('callback'), None))

    return callbacks

def get_log_msgs():
    data = []
    while not c.exit:
        try:
            data.append(aq.get(timeout=1))
        except Empty:
            break

    return data