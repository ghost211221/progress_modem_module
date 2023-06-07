import eel

from main import VERSION


@eel.expose
def get_version():
    return VERSION