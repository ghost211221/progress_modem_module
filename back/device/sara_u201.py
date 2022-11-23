

from back.device.abstract import AbstractDevice

class SaraU201(AbstractDevice):

    def __init__(self):
        super().__init__()
        self.dev_type = 'sara'