

class Context():
    """ Class that contains all states of program"""

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Context, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        # entity of device
        self.device = None
        self.selected_com = None
        self.selected_baudrate = None
        self.selected_flow_control = None
        self.selected_data_bits = None
        self.selected_stop_bits = None
        self.selected_parity = None

    def get_device(self, device_name):
        for device in self.devices:
            if device['dev_name'] == device_name:
                return device