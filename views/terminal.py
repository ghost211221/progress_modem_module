import eel

from back.context import Context


c = Context()

@eel.expose
def e_get_cmds():
    return c.device.get_cmds()