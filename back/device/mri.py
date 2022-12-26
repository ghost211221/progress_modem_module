

from back.device.abstract import AbstractDevice

class MRI(AbstractDevice):

    def __init__(self):
        super().__init__()
        self.dev_type = 'mri'