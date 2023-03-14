import re

from back.context import Context
from back.decorators import clear_ok, clear_premessage

c = Context()

@clear_ok
def cgmi(cmd, response):
    """get manufacturer id"""
    return [{'field': 'manufacturer_id', 'data': response['ans'] or ''}]

@clear_ok
def cgmm(cmd, response):
    """get device decimal number"""
    return [{'field': 'decimal_number', 'data': response['ans']  or ''}]

@clear_ok
@clear_premessage
def cgmr(cmd, response):
    """get firmware version"""
    return [{'field': 'firmware_version', 'data': response['ans']  or ''}]

@clear_ok
def cgsn(cmd, response):
    """imei"""
    return [{'field': 'imei', 'data': response['ans']  or ''}]

@clear_ok
def ati(cmd, response):
    """device info"""
    try:
        model = re.search(r'(?<=Model\:)([\w\d]+)', response['ans'] ).group(0)
    except Exception:
        model = ''
    try:
        revision = re.search(r'(?<=Revision\:)([\w\d]+)', response['ans'] ).group(0)
    except Exception:
        revision = ''

    return [
            {'field': 'model', 'data': model or ''},
            {'field': 'revision', 'data': revision or ''},
        ]

@clear_ok
@clear_premessage
def cops(cmd, response):
    """Set command forces an attempt to select and register the GSM/UMTS network operator."""
    if 'COPS?' in cmd:
        if response['ans']:
            data = response['ans'].split(',')[-1]  or ''
            mode_dec = int(response['ans'].split(',')[0])
            mode = ''
            if mode_dec == 0:
                mode = 'Автоматический'
            elif mode_dec == 1:
                mode = 'Ручной'
            elif mode_dec == 2:
                mode = 'Выход из сети'
            elif mode_dec == 3:
                mode = 'Установить формат'
            return [
                {'field': 'operator', 'data': data},
                {'field': 'network-operator', 'data': data},
                {'field': 'network-operator_select_mode', 'data': mode},
            ]

@clear_ok
def creg(cmd, response):
    if 'CREG?' in cmd:
        if response['ans']:
            arr = response['ans'].split(',')
            ans = int(arr[1])
            val = ''
            if ans == 0:
                val = 'Не зарагистирована, поиск оператора'
            elif ans == 1:
                val = 'Зарегистрирована'
            elif ans == 2:
                val = 'Не зарагистирована, поиск оператора'
            elif ans == 3:
                val = 'Регистрация запрещена'
            elif ans == 4:
                val = 'Неизвестно'

            return [
                {'field': 'sim-status', 'data': val},
                {'field': 'network-reg_status', 'data': val},
                {'field': 'network-lac', 'data': arr[2]},
                {'field': 'network-ci', 'data': arr[3]},
            ]

@clear_ok
@clear_premessage
def csq(cmd, response):
    """get firmware version"""
    try:
        val = int(response['ans'].split(',')[0])
    except ValueError:
        return

    if val == 0:
        return [{'field': 'signal_power', 'img': 'signals/signal_5.svg'}]
    elif val == 1:
        return [{'field': 'signal_power', 'img': 'signals/signal_4.svg'}]
    elif 2 <= val <= 30:
        return [{'field': 'signal_power', 'img': 'signals/signal_3.svg'}]
    elif val == 31:
        return [{'field': 'signal_power', 'img': 'signals/signal_2.svg'}]
    elif 32 <= val <= 98:
        return [{'field': 'signal_power', 'img': 'signals/signal_1.svg'}]
    elif val == 99:
        return [{'field': 'signal_power', 'img': 'signals/no_signal.svg'}]