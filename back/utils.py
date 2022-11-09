import yaml

import serial.tools.list_ports

def get_comports_list():
    coms = []
    for com in sorted(serial.tools.list_ports.comports(), reverse=True, key=lambda d: d.name):
        coms.append({'name': com.name, 'description': com.description})

    return coms

def comport_pars():
    with open('data/com_pars.yml') as f:
        parameters = yaml.safe_load(f)

        return parameters