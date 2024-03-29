from threading import Thread
import time
from sys import exit
import eel

from back.context import Context
# from back.device.sara_u201 import SaraU201
from back.device.mri import MRI
from back.workers import task_processing_worker, script_running_worker
from views.comport import *
from views.main_ops import *
from views.sms import *
from views.terminal import *
from views.network import *
from views.phonebook import *
from views.version import *


VERSION = '0.3.1'

context = Context()

def close_callback(route, websockets):
    context.exit = True
    time.sleep(0.2)
    if context.device and context.device.port:
        context.device.port.close()

    exit(0)


if __name__ == '__main__':
    context = Context()

    context.device = MRI()

    eel.init('front', allowed_extensions=['.js', '.html'],)

    tasks_thread = Thread(target=task_processing_worker)
    tasks_thread.start()

    script_thread = Thread(target=script_running_worker)
    script_thread.start()

    eel.start(
        'templates/main.html',
        jinja_templates='templates',
        mode='chrome',
        size=(1150, 975),
        position=(0,0),
        close_callback=close_callback
    )