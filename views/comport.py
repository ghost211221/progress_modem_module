import eel

from back.context import Context
from back.exceptions import ComSetupError, ComConnectError, ComCommunicationError
from back.utils import get_comports_list, comport_pars, get_cmd_callbacks
from back.queues import TasksQueue


context = Context()
q = TasksQueue()

@eel.expose
def e_get_comports_list():
    return get_comports_list()

@eel.expose
def e_get_comport_pars():
    return comport_pars()

@eel.expose
def e_setup_device(comport, description, baudrate, flow_control, data_bits, stop_bits, parity):
    status = 'success'
    msg = ''
    response = {'status': status, 'msg': msg}

    if status == 'success':
        try:
            context.device.setup_device(comport, description, baudrate, flow_control, data_bits, stop_bits, parity)
        except ComSetupError as e:
            msg = f'Не удалось применить настройки COM порта: {e}'
            status = 'fail'

    return response

@eel.expose
def e_connect_device():
    status = 'success'
    msg = ''
    response = {'status': status, 'msg': msg}
    try:
        context.device.connect()
        response.update(context.device.get_mode())
    except ComConnectError as e:
        response['msg'] = f'Не удалось подключиться к COM порту: {e}'
        response['status'] = 'fail'

    return response

@eel.expose
def e_close_connection():
    try:
        context.device.disconnect()
        return {'status': 'success'}
    except ComConnectError as e:
        return {'status': 'fail', 'msg': f'Возникла проблема при отключении: {e}'}

@eel.expose
def e_communicate(cmd):
    msg = ''
    status = 'success'
    callbacks = get_cmd_callbacks(cmd)
    try:
        q.put((cmd, callbacks))
    except ComCommunicationError as e:
        status = 'fail'
        msg = f'Ошибка связи: {e}'

    return {'status': status, 'msg': msg,}

@eel.expose
def e_get_comport_data():
    ret_dict =  {
        'comport': context.device.comport,
        'baudrate': context.device.baudrate,
        'flow_control': context.device.flow_control,
        'data_bits': context.device.data_bits,
        'stop_bits': context.device.stop_bits,
        'parity': context.device.parity,
        'description': context.device.description,
        'connected': context.device.connected
    }

    ret_dict.update(context.device.get_mode())

    return ret_dict

@eel.expose
def e_get_log():
    return context.cmd_log