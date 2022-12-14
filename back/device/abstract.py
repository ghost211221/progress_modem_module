from abc import ABCMeta, abstractmethod
import logging
import yaml

from serial import Serial, SerialException

from back.device.consts import DATABITS_MAP, PARITY_MAP, STOPBITS_MAP
from back.context import Context
from back.exceptions import ComSetupError, ComConnectError, ComCommunicationError, UnknownDeviceError

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
    dev_type = None

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

        self.port.setRTS(True)
        self.port.setDTR(True)
        if self.flow_control == 'hardware':
            self.port.setRTS(False)

        if self.flow_control == 'xon-xoff':
            self.port.setRTS(False)
            self.port.setDTR(False)

    def get_mode(self):
        return {
            'cd': self.port.cd if self.connected else False,
            'ri': self.port.ri if self.connected else False,
            'dsr': self.port.dsr if self.connected else False,
            'cts': self.port.cts if self.connected else False,
            'dtr': self.port.dtr if self.connected else False,
            'rts': self.port.rts if self.connected else False,
        }

    def connect(self):
        try:
            self.port.open()
            self.connected = True
            print('connected!')
        except Exception as e:
            raise ComConnectError(f'???????????? ???????????????? ?????????? {self.comport}: {e}')

    def disconnect(self):
        try:
            self.port.close()
            self.connected = False
        except Exception as e:
            raise ComConnectError(f'???????????? ???????????????? ?????????? {self.comport}: {e}')

    def get_cmds(self):
        if not self.dev_type:
            raise UnknownDeviceError('dev_type ???? ????????????')

        if self.dev_type not in ('sara', 'mri'):
            raise UnknownDeviceError(f'?????????????????????? ????????????: {self.dev_type}')

        with open(f'cmds/{self.dev_type}/cmd.yml') as f:
            cmds = yaml.safe_load(f)

            return cmds


    def send(self, data):
        try:
            self.port.write(f'{data}\r\n'.encode('utf-8'))
        except SerialException as e:
            raise ComCommunicationError(f'???????????? ???????????? ?? ???????? {self.comport}: {e}')

    def read(self):
        try:
            echo = context.device.port.readline().decode('utf-8')
            ans = ''.join([val.decode('utf-8') for val in context.device.port.readlines()])
            return {'echo': echo, 'ans': ans}
        except SerialException as e:
            raise ComCommunicationError(f'???????????? ???????????? ?????????? {self.comport}: {e}')
