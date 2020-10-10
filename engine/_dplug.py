__active_plug = None


def set_plugin(plug):
    global __active_plug
    __active_plug = plug


def get_plugin():
    return __active_plug
