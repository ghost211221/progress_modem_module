from back.callbacks import *

CMDS = [
    {'cmd': 'AT', 'callback': None},
    {'cmd': 'ATE0', 'callback': None},
    {'cmd': 'ATE1', 'callback': None},
    {'cmd': 'CMEE', 'callback': None},
    {'cmd': 'CGMI', 'callback': cgmi},
    {'cmd': 'CGMM', 'callback': cgmm},
    {'cmd': 'CGMR', 'callback': cgmr},
    {'cmd': 'ATI', 'callback': ati},
    {'cmd': 'CGSN', 'callback': cgsn},
    {'cmd': 'COPS', 'callback': cops},
    {'cmd': 'CREG', 'callback': creg},
    {'cmd': 'CIMI', 'callback': None},
    {'cmd': 'ZGETICCID', 'callback': None},
    {'cmd': 'CSQ', 'callback': csq},
    {'cmd': 'CLCK', 'callback': None},
    {'cmd': 'CPIN', 'callback': None},
]