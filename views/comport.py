import eel

from back.context import Context
from back.exceptions import ComSetupError, ComConnectError, ComCommunicationError
from back.utils import get_comports_list, comport_pars


context = Context()

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
    try:
        context.device.send(cmd)
        ans = context.device.read()
    except ComCommunicationError as e:
        status = 'fail'
        msg = f'Ошибка связи: {e}'

    return {'status': status, 'msg': msg, 'ans': ans}

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