from threading import Thread

import eel

from back.context import Context
# from back.device.sara_u201 import SaraU201
from back.device.mri import MRI
from back.workers import task_processing_worker, log_processing_worker
from views.comport import *
from views.terminal import *

if __name__ == '__main__':
    context = Context()

    context.device = MRI()

    eel.init('front', allowed_extensions=['.js', '.html'],)

    tasks_thread = Thread(target=task_processing_worker)
    tasks_thread.start()

    log_thread = Thread(target=log_processing_worker)
    log_thread.start()

    eel.start(
        'templates/main.html',
        jinja_templates='templates',
        mode='chrome',
        size=(1160, 975),
        position=(0,0)
    )