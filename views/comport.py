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
def e_setup_device(comport, baudrate, flow_control, data_bits, stop_bits, parity):
    status = 'success'
    msg = ''
    if not comport:
        msg = 'Не указан COM порт'
        status = 'fail'
    if not baudrate:
        msg = 'Не указана скорость'
        status = 'fail'
    if not flow_control:
        msg = 'Не указан режим контроля потока'
        status = 'fail'
    if not data_bits:
        msg = 'Не указан COM порт'
        status = 'fail'
    if not stop_bits:
        msg = 'Не указан COM порт'
        status = 'fail'
    if not parity:
        msg = 'Не указан COM порт'
        status = 'fail'

    if status == 'success':
        try:
            context.device.setup_device(comport, baudrate, flow_control, data_bits, stop_bits, parity)
        except ComSetupError as e:
            msg = f'Не удалось применить настройки COM порта: {e}'
            status = 'fail'

    if status == 'success':
        try:
            context.device.connect()
        except ComConnectError as e:
            msg = f'Не удалось подключиться к COM порту: {e}'
            status = 'fail'

    return {'status': status, 'msg': msg}

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
        msg = context.device.read()
    except ComCommunicationError as e:
        status = 'fail'
        msg = f'Ошибка связи: {e}'

    return {'status': status, 'msg': msg}
