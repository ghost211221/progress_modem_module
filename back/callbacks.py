import re

from back.consts.cops import ACT, STAT
from back.consts.operators import MAP_CODE_OPERTOR
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
    pass
    # return [{'field': 'firmware_version', 'data': response['ans']  or ''}]

@clear_ok
def cgsn(cmd, response):
    """imei"""
    return [
            {'field': 'imei', 'data': response['ans']  or ''},
            {'field': 'codes-imei', 'data': response['ans']  or ''},
        ]

@clear_ok
@clear_premessage
def egmr(cmd, response):
    """imei"""
    if 'EGMR=0,5' in cmd:
        # read serial nu,ber
        return [
                {'field': 'codes-sn', 'data': response['ans'].replace('"', '')  or ''},
            ]

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
    try:
        firmware_version = re.search(r'(?<=Revision\:)([\w\d\.]+)', response['ans'] ).group(0)
    except Exception:
        revision = ''

    return [
            {'field': 'model', 'data': model or ''},
            {'field': 'revision', 'data': revision or ''},
            {'field': 'firmware_version', 'data': firmware_version or ''},
        ]

# @clear_ok
@clear_premessage
def cops(cmd, response):
    """Set command forces an attempt to select and register the GSM/UMTS network operator."""
    # (2,"25001","25001","25001",2),(1,"25001","25001","25001",0),(1,"25099","25099","25099",2),(1,"25020","25020","25020",2),(1,"25002","25002","25002",2),(1,"25002","25002","25002",0),(1,"25099","25099","25099",0),,(0-3),(0-2)
    if 'COPS?' in cmd:
        if response['ans']:
            op_code = response['ans'].replace('OK', '').split(',')[-1]  or ''
            mode_dec = int(response['ans'].replace('OK', '').split(',')[0])
            mode = ''
            if mode_dec == 0:
                mode = 'Автоматический'
            elif mode_dec == 1:
                mode = 'Ручной'
            elif mode_dec == 2:
                mode = 'Выход из сети'
            elif mode_dec == 3:
                mode = 'Установить формат'

            op_name = MAP_CODE_OPERTOR.get(int(op_code), '')
            data = f'{op_code} ({op_name})'

            return [
                {'field': 'operator', 'data': data},
                {'field': 'network-operator', 'data': data},
                {'field': 'network-operator_select_mode', 'data': mode},
            ]

    if 'COPS=?' in cmd:
        # get list of operators
        operators = []
        # line = '(2,"25001","25001","25001",2),(1,"25001","25001","25001",0),(1,"25099","25099","25099",2),(1,"25020","25020","25020",2),(1,"25002","25002","25002",2),(1,"25002","25002","25002",0),(1,"25099","25099","25099",0),,(0-3),(0-2)'
        # for i, op_str in enumerate(re.findall(r'\(([\w\d",]+)\)', line)):
        for i, op_str in enumerate(re.findall(r'\(([\w\d",]+)\)', response.get('ans', '').replace('OK', ''))):
            op_data = op_str.split(',')

            status_code = int(op_data[0])
            long_oprt = int(op_data[1].replace('"', ''))
            short_oprt = int(op_data[2].replace('"', ''))
            numeric_oprt = int(op_data[3].replace('"', ''))
            act_code = int(op_data[4])

            op_dict = dict(
                i=i+1,
                operator_name=MAP_CODE_OPERTOR.get(numeric_oprt, ''),
                operator_code=numeric_oprt,
                status=STAT.get(status_code, ''),
                act=ACT.get(act_code, '')
            )

            operators.append(op_dict)

        return [
            {'field': 'network-operators_table', 'table_data': operators, 'close_spinner': True}
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
                {'field': 'network-lac', 'data': arr[2] if len(arr) == 3 else ''},
                {'field': 'network-ci', 'data': arr[3] if len(arr) == 4 else ''},
            ]

@clear_ok
@clear_premessage
def ciccid(cmd, response):
    if 'CICCID' in cmd:
        return [{'field': 'sim-iccd', 'data': response['ans']  or ''}]

@clear_ok
@clear_premessage
def imsi(cmd, response):
    if 'CIMI' in cmd:
        return [{'field': 'sim-imsi', 'data': response['ans']  or ''}]

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

@clear_ok
@clear_premessage
def cpbr(cmd, response):
    """get phone book or calls"""
    if 'CPBR=1,200' in cmd:
        phones = []
        lines = response['ans'].split('\r\n\r\n+CPBR: ')
        for line in lines:
            arr = line.split(', ')

            idx = int(arr[0])
            phone_number = arr[1].replace('"', '')
            phone_type = int(arr[2])
            phone_name = arr[3].replace('"', '')
            phones.append(dict(
                i=idx,
                phone_number=phone_number,
                phone_name=phone_name,
            ))

        return [
            {
                'field': 'phonebook-contact_table',
                'table_data': phones,
                'table_row_style': {
                    'width': '100%',
                    'display': 'inline-table',
                    'table-layout': 'fixed'
                }
            }

        ]

    if 'CPBR=1,20' in cmd:
        phones = []
        lines = response['ans'].split('\r\n\r\n+CPBR: ')
        for line in lines:
            if not line:
                continue
            arr = line.split(', ')

            idx = int(arr[0])
            phone_number = arr[1].replace('"', '')
            phone_type = int(arr[2])
            phone_name = arr[3].replace('"', '')
            phones.append(dict(
                i=idx,
                phone_number=phone_number,
                phone_name=phone_name,
            ))

        return [
            {
                'field': 'phonebook-last_calls',
                'table_data': phones,
                'table_row_style': {
                    'width': '100%',
                    'display': 'inline-table',
                    'table-layout': 'fixed'
                }

            }
        ]
