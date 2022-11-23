import eel

from back.context import Context
from back.device.sara_u201 import SaraU201
from views.comport import *
from views.terminal import *

if __name__ == '__main__':
    context = Context()

    context.device = SaraU201()

    eel.init('front', allowed_extensions=['.js', '.html'],)

    eel.start(
        'templates/main.html',
        jinja_templates='templates',
        mode='chrome',
        size=(1160, 975),
        position=(0,0)
    )