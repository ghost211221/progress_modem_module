from serial import FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS
from serial import PARITY_NONE, PARITY_EVEN, PARITY_ODD
from serial import STOPBITS_ONE, STOPBITS_TWO

DATABITS_MAP = {
    '5': FIVEBITS,
    '6': SIXBITS,
    '7': SEVENBITS,
    '8': EIGHTBITS,
}

PARITY_MAP = {
    'none': PARITY_NONE,
    'even': PARITY_EVEN,
    'odd': PARITY_ODD,
}

STOPBITS_MAP = {
    '1': STOPBITS_ONE,
    '2': STOPBITS_TWO,
}