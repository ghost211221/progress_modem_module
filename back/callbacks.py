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
def cops(cmd, response):
    if 'COPS?' in cmd:
        if response['ans']:
            return [{'field': 'operator', 'data': response['ans'].split(',')[-1]  or ''}]

@clear_ok
def creg(cmd, response):
    if 'CREG?' in cmd:
        if response['ans']:
            ans = int(response['ans'].split(',')[1])
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

            return [{'field': 'sim-status', 'data': val}]