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
]

send_recieve_sms = [
    'AT+CSCA?',
    'AT+CNMI?',
    'AT+CMGF=1',
    'AT+CMGS="+70123456789"',

]