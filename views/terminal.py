from queue import Empty
import yaml
import os

import tkinter
from tkinter import filedialog as fd

import eel

from back.consts.cmds.mri import operations
from back.context import Context
from back.queues import AnsQueue, TasksQueue
from back.utils import get_cmd_callbacks


c = Context()
aq = AnsQueue()
q = TasksQueue()

def get_file_path():
    root = tkinter.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    filename = fd.askopenfilename()
    return filename

def get_dir_path():
    root = tkinter.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    directory_path = fd.askdirectory()
    return directory_path

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
def select_scripts_folder():
    c.scripts_folder = get_dir_path()

@eel.expose
def get_scripts_list():
    if not c.scripts_folder:
        return {'data': []}
    
    return {'data': os.listdir(c.scripts_folder)}

@eel.expose
def import_cmds():
    file_path = get_file_path()
    if not file_path:
        return

    try:
        with open(file_path) as f:
            cmds = yaml.safe_load(f)

            c.device.set_cmds(cmds)
    except Exception:
        return

@eel.expose
def load_cmds():
    file_path = get_file_path()
    if not file_path:
        return

    try:
        with open(file_path) as f:
            cmds = yaml.safe_load(f)
        old_cms = c.device.cmds
        for cmd_group in cmds:
            if not list(filter(lambda g: g['name'] == cmd_group['name'], old_cms)):
                old_cms.append(cmd_group)
                continue
            
            for g in old_cms:
                if g['name'] == cmd_group['name']:
                    for cmd in cmd_group['items']:
                        if not list(filter(lambda g: g['name'] == cmd['name'], g['items'])):
                            g['items'].append(cmd)

        c.device.set_cmds(old_cms)

    except Exception:
        return

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
