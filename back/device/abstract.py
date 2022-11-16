from abc import ABCMeta, abstractmethod
import logging

from serial import Serial, SerialException

from back.device.consts import DATABITS_MAP, PARITY_MAP, STOPBITS_MAP
from back.context import Context
from back.exceptions import ComSetupError, ComConnectError, ComCommunicationError

log = logging.getLogger(__name__)
context = Context()

class AbstractDevice(metaclass=ABCMeta):
    comport = ''
    baudrate = 115200
    flow_control = 'hardware'
    data_bits = 8
    stop_bits = 1
    parity = 'none'
    timeout = 0.1
    description = ''
    connected = False

    rts = False
    dtr = False
    cts = False
    dsr = False
    ri = False
    cd = False

    cmd_groups = []

    def __init__(self):
        self.port = Serial()

    def setup_device(self, comport, description, baudrate, flow_control, data_bits, stop_bits, parity):
        self.comport = comport
        self.baudrate = baudrate
        self.flow_control = flow_control
        self.data_bits = data_bits
        self.stop_bits = stop_bits
        self.parity = parity
        self.description = description

        self.port.port = self.comport
        self.port.baudrate = self.baudrate
        self.port.bytesize  = DATABITS_MAP[self.data_bits]
        self.port.stopbits  = STOPBITS_MAP[self.stop_bits]
        self.port.parity  = PARITY_MAP[self.parity]
        self.port.timeout = self.timeout

        if self.flow_control == 'hardware':
            self.port.dtr = True
            # self.port.cts = True

        if self.flow_control == 'xon-xoff':
            # self.port.cts = True
            self.port.xonxoff = True

    def connect(self):
        try:
            self.port.open()
            self.connected = True
            print('connected!')
        except Exception as e:
            raise ComConnectError(f'Ошибка открытия порта {self.comport}: {e}')

    def disconnect(self):
        try:
            self.port.close()
            self.port = None
            self.connected = False
            print('disconnected!')
        except Exception as e:
            raise ComConnectError(f'Ошибка закрытия порта {self.comport}: {e}')

    @abstractmethod
    def get_cmds(self):
        pass

    def send(self, data):
        try:
            self.port.write(f'{data}\r\n'.encode('utf-8'))
        except SerialException as e:
            raise ComCommunicationError(f'Ошибка записи в порт {self.comport}: {e}')

    def read(self):
        try:
            lines = context.device.port.readlines()
            return '\n'.join([elem.decode('utf-8').replace('\r', '').replace('\n', '') for elem in lines])
        except SerialException as e:
            raise ComCommunicationError(f'Ошибка чтения порта {self.comport}: {e}')
