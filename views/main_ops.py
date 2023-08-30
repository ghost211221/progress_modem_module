from sys import exit
import eel
import time

from back.context import Context


context = Context()

@eel.expose
def close_app():
    context.exit = True
    time.sleep(0.2)
    if context.device and context.device.port:
        context.device.port.close()

    exit(0)
