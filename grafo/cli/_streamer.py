class _Streamer(object):
    def __init__(self):
        self.__output = print
        self.__input = None

    @property
    def output(self):
        return self.__output

    @output.setter
    def output(self, new_output):
        self.__output = new_output

    @property
    def input(self):
        return self.__input

    @input.setter
    def input(self, new_input):
        self.__input = new_input

    def out(self, message: str):
        self.__output(message)

    def inp(self, message: str) -> str:
        return self.__input(message)


STREAM = _Streamer()
