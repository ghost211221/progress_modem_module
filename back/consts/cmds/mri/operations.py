"""lists of AT cmds for different operations"""

init = [
    'AT',
    'ATE0',
    'AT+CMEE=2',
    'AT+CGMI',
    'AT+CGMM',
    'AT+CGMR',
    'ATI',
    'AT+CGSN',
    'AT+COPS?',
    'AT+CREG=2',
    'AT+CREG?',
    'AT+CREG=0',
    'AT+CIMI',
    'AT+ZGETICCID',
    'AT+CSQ',
    'AT+CLCK="SC",2',
    'AT+CPIN?',
    'AT+CCLK?',
    'AT+CICCID',
    'AT+CIMI',
    'AT+EGMR=0,5',
    'AT+ERAT?'
]

refresh_network_info = [
    'AT+COPS?',
    'AT+CREG?',
    'AT+CSQ',
    'AT+CICCID',
    'AT+CIMI',
]

get_operators_list = [
    'AT+COPS=?'
]

send_sms = [
    'AT+CSCA?',
    'AT+CNMI?',
    'AT+CMGF=1'
]

auto_set_operator = [
    'AT+COPS?',
    'AT+CSQ',
    'AT+COPS=0',
    'AT+CGREG?',
    'AT+CEREG?',
]

deregister_operator = [
    'AT+COPS=2',
    'AT+COPS?',
    'AT+CSQ',
    'AT+CEREG?',
    'AT+CGREG?',
    'AT+CREG?',
]

select_operator = [
    'AT+COPS=3,2',
    'AT+COPS?',
    'AT+CSQ',
    'AT+CEREG?',
    'AT+CGREG?',
    'AT+CREG?',
]

get_phones_list = [
    'AT+CPBS="SM"',
    'AT+CPBR=?',
    'AT+CPBR=1,200',
]

get_calls_list = [
    'AT+CPBS="LD"',
    'AT+CPBR=?',
    'T+CPBR=1,20',
]

get_messages_list = [
    'AT+CMGF=1',
    'AT+CMGL="ALL"',
]

delete_all_sms = [
    'AT+CMGD=0,4',
    'AT+CMGF=1',
    'AT+CMGL="ALL"',
]

disable_sms_alert = [
    'AT+CNMI=1,0',
    'AT+CNMI?',
]