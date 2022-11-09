from abc import ABCMeta, abstractmethod
import logging

from serial import Serial, SerialException

from back.device.consts import DATABITS_MAP, PARITY_MAP, STOPBITS_MAP
from back.context import Context
from back.exceptions import ComSetupError, ComConnectError, ComCommunicationError

log = logging.getLogger(__name__)
context = Context()

class AbstractDevice(metaclass=ABCMeta):
    comport = None
    baudrate = None
    flow_control = None
    data_bits = None
    stop_bits = None
    parity = None
    timeout = 1

    cmd_groups = []

    def __init__(self):
        self.port = None

    def setup_device(self, comport, baudrate, flow_control, data_bits, stop_bits, parity):
        if not comport or not baudrate or not flow_control or not data_bits or not stop_bits or not parity:
            raise ComSetupError('One of parameters not provided')

        self.comport = comport
        self.baudrate = baudrate
        self.flow_control = flow_control
        self.data_bits = data_bits
        self.stop_bits = stop_bits
        self.parity = parity

    def connect(self):
        self.port = Serial()
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
            return self.port.readline().decode('utf-8').replace('\r', '')
        except SerialException as e:
            raise ComCommunicationError(f'Ошибка чтения порта {self.comport}: {e}')
