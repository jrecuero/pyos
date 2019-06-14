from typing import List, Union, Any


class Kontent(object):
    NONE = 0
    END = 1
    COMMAND = 10
    MODE = 11
    STR = 20
    INT = 21
    KEYWORD = 30

    @staticmethod
    def to_str(klass: int) -> str:
        if klass == Kontent.NONE:
            return "none"
        elif klass == Kontent.END:
            return "end"
        elif klass == Kontent.COMMAND:
            return "command"
        elif klass == Kontent.MODE:
            return "mode"
        elif klass == Kontent.STR:
            return "string"
        elif klass == Kontent.INT:
            return "int"
        elif klass == Kontent.KEYWORD:
            return "keyword"
        else:
            return "unknowm"


class EndToken(object):
    pass


END_TOKEN = EndToken()


class Content(object):
    def __init__(self, vault: Any, **kwargs):
        self._vault: Any = vault
        self.klass: int = Kontent.NONE

    @property
    def name(self):
        return self._vault

    def match(self, tokens: List[str], tindex: int, **kwargs) -> Union[bool, int]:
        token = tokens[tindex]
        if (token != END_TOKEN) and (token == self._vault):
            return True, tindex + 1
        return False, tindex

    def help(self, tokens: List[str], tindex: int, **kwargs) -> List[str]:
        return [""]

    def complete(self, tokens: List[str], tindex: int, **kwargs) -> List[str]:
        return [""]


class EndContent(Content):
    def __init__(self, **kwargs):
        super(EndContent, self).__init__(END_TOKEN, **kwargs)
        self.klass: int = Kontent.END

    def match(self, tokens: List[str], tindex: int, **kwargs) -> Union[bool, int]:
        if tokens[tindex] == self._vault:
            return True, tindex + 1
        return False, tindex


class StrContent(Content):
    def __init__(self, vault: str, **kwargs):
        super(StrContent, self).__init__(vault, **kwargs)
        self.klass: int = Kontent.STR

    def match(self, tokens: List[str], tindex: int, **kwargs) -> Union[bool, int]:
        token = tokens[tindex]
        if token != END_TOKEN:
            return True, tindex + 1
        return False, tindex


class KeywordContent(Content):
    def __init__(self, vault: str, **kwargs):
        super(KeywordContent, self).__init__(vault, **kwargs)
        self.klass: int = Kontent.KEYWORD


class IntContent(Content):
    def __init__(self, vault: int, **kwargs):
        super(IntContent, self).__init__(vault, **kwargs)
        self.klass: int = Kontent.INT

    def match(self, tokens: List[str], tindex: int, **kwargs) -> Union[bool, int]:
        try:
            token = tokens[tindex]
            if (token != END_TOKEN) and int(token):
                return True, tindex + 1
        except ValueError:
            pass
        return False, tindex


class CommandContent(Content):
    def __init__(self, vault: str, **kwargs):
        super(CommandContent, self).__init__(vault, **kwargs)
        self.klass: int = Kontent.COMMAND
        self.command = kwargs.get("command", None)

    def call(self, **kwargs):
        if self.command:
            return self.command(**kwargs)
