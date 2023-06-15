import re

import eel

from back.consts.cops import ACT, STAT, RAT
from back.consts.operators import MAP_CODE_OPERTOR
from back.context import Context
from back.decorators import clear_ok, clear_premessage, clear_br
from back.queues import TasksQueue


c = Context()
q = TasksQueue()


def stop_script_execution(*args):
    q.clear()
    c.run_script = False
    c.device.set_timeout()
    eel.reinit_start_btn()

@clear_ok
@clear_br
def cgmi(cmd, response):
    """get manufacturer id"""
    return [{'field': 'manufacturer_id', 'data': response['cl_ans'] or ''}]

@clear_ok
@clear_br
def cgmm(cmd, response):
    """get device decimal number"""
    return [{'field': 'decimal_number', 'data': response['cl_ans']  or ''}]

@clear_ok
@clear_premessage
@clear_br
def cgmr(cmd, response):
    """get firmware version"""
    pass
    # return [{'field': 'firmware_version', 'data': response['cl_ans']  or ''}]

@clear_ok
@clear_br
def cgsn(cmd, response):
    """imei"""
    return [
            {'field': 'imei', 'data': response['cl_ans']  or ''},
            {'field': 'codes-imei', 'data': response['cl_ans']  or ''},
        ]

@clear_ok
@clear_premessage
@clear_br
def egmr(cmd, response):
    """imei"""
    if 'EGMR=0,5' in cmd:
        # read serial nu,ber
        return [
                {'field': 'codes-sn', 'data': response['cl_ans'].replace('"', '')  or ''},
            ]

@clear_ok
@clear_br
def ati(cmd, response):
    """device info"""
    try:
        model = re.search(r'(?<=Model\:)([\w\d]+)', response['cl_ans'] ).group(0)
    except Exception:
        model = ''
    try:
        revision = re.search(r'(?<=Revision\:)([\w\d]+)', response['cl_ans'] ).group(0)
    except Exception:
        revision = ''
    try:
        firmware_version = re.search(r'(?<=Revision\:)([\w\d\.]+)', response['cl_ans'] ).group(0)
    except Exception:
        revision = ''

    return [
            {'field': 'model', 'data': model or ''},
            {'field': 'revision', 'data': revision or ''},
            {'field': 'firmware_version', 'data': firmware_version or ''},
        ]

# @clear_ok
@clear_premessage
@clear_br
def cops(cmd, response):
    """Set command forces an attempt to select and register the GSM/UMTS network operator."""
    # (2,"25001","25001","25001",2),(1,"25001","25001","25001",0),(1,"25099","25099","25099",2),(1,"25020","25020","25020",2),(1,"25002","25002","25002",2),(1,"25002","25002","25002",0),(1,"25099","25099","25099",0),,(0-3),(0-2)
    if 'COPS?' in cmd:
        if response['cl_ans']:
            op_code = response['cl_ans'].replace('OK', '').split(',')[-1]  or ''
            mode_dec = int(response['cl_ans'].replace('OK', '').split(',')[0])
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
@clear_br
@clear_premessage
def creg(cmd, response):
    if 'CREG?' in cmd:
        if response['cl_ans']:
            arr = response['cl_ans'].split(',')
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
                {'field': 'network-lac', 'data': arr[2].replace('"', '') if len(arr) >= 3 else ''},
                {'field': 'network-ci', 'data': arr[3].replace('"', '') if len(arr) >= 4 else ''},
            ]

@clear_ok
@clear_premessage
@clear_br
def ciccid(cmd, response):
    if 'CICCID' in cmd:
        return [{'field': 'sim-iccd', 'data': response['cl_ans']  or ''}]

@clear_ok
@clear_premessage
@clear_br
def imsi(cmd, response):
    if 'CIMI' in cmd:
        return [{'field': 'sim-imsi', 'data': response['cl_ans']  or ''}]

@clear_ok
@clear_premessage
@clear_br
def csq(cmd, response):
    """get firmware version"""
    try:
        val = int(response['cl_ans'].split(',')[0])
    except ValueError:
        return

    img_dict = {}

    if val == 0:
        img_dict = {'field': 'signal_power', 'img': 'signals/signal_5.svg'}
    elif val == 1:
        img_dict = {'field': 'signal_power', 'img': 'signals/signal_4.svg'}
    elif 2 <= val <= 30:
        img_dict = {'field': 'signal_power', 'img': 'signals/signal_3.svg'}
    elif val == 31:
        img_dict = {'field': 'signal_power', 'img': 'signals/signal_2.svg'}
    elif 32 <= val <= 98:
        img_dict = {'field': 'signal_power', 'img': 'signals/signal_1.svg'}
    elif val == 99:
        img_dict = {'field': 'signal_power', 'img': 'signals/no_signal.svg'}

    return [
        img_dict,
        {'field': 'network-rssi', 'data': val}
    ]

@clear_ok
@clear_premessage
@clear_br
def cpbr(cmd, response):
    """get phone book or calls"""
    if 'CPBR=1,200' in cmd:
        phones = []
        lines = response['cl_ans'].split('\r\n\r\n+CPBR: ')
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
        lines = response['cl_ans'].split('\r\n\r\n+CPBR: ')
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


@clear_ok
@clear_premessage
@clear_br
def erat(cmd, response):
    """To get RAT mode status and GRRS/EDGE status or set RAT mode of MS"""
    if 'ERAT?' in cmd:
        arr = re.findall(r'\d', response['cl_ans'])

        act = int(arr[0])
        gprs_status = arr[1].replace('"', '')
        rat_mode = int(arr[2])
        prefer_rat = arr[3].replace('"', '')
    return [
        {'field': 'network-rat', 'data': RAT.get(rat_mode)},
        {'field': 'operator', 'add_data': RAT.get(rat_mode)},
    ]

@clear_ok
@clear_premessage
@clear_br
def cmgl(cmd, response):
    """get messages"""

    if 'CMGL="ALL"' in cmd:
        messages = []
        lines = response['cl_ans'].split('\r\n\r\n+CMGL: ')
        for line in lines:
            if not line:
                continue
            arr = line.split(',')

            idx = int(arr[0])
            phone_number = arr[2].replace('"', '')
            msg_date = arr[3]
            msg_status = arr[1].replace('"', '')
            messages.append(dict(
                i=idx,
                number=phone_number,
                date=msg_date,
                status=msg_status,
            ))

        return [
            {
                'field': 'sms-sms_table',
                'table_data': messages,
                'table_row_style': {
                    'width': '100%',
                    'display': 'inline-table',
                    'table-layout': 'fixed'
                }

            }
        ]
