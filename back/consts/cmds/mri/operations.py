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
    'AT+EGMR=0,5'
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