from typing import List, Union, Any


class ContentKlass(object):
    NONE = 0
    COMMAND = 1
    MODE = 2
    STR = 10
    INT = 11
    KEYWORD = 20

    @staticmethod
    def to_str(klass: int) -> str:
        if klass == ContentKlass.NONE:
            return "none"
        elif klass == ContentKlass.COMMAND:
            return "command"
        elif klass == ContentKlass.MODE:
            return "mode"
        elif klass == ContentKlass.STR:
            return "string"
        elif klass == ContentKlass.INT:
            return "int"
        elif klass == ContentKlass.KEYWORD:
            return "keyword"
        else:
            return "unknowm"


class Content(object):
    def __init__(self, vault: Any, **kwargs):
        self._vault: Any = vault
        self.klass: int = ContentKlass.NONE

    def match(self, tokens: List[str], tindex: int, **kwargs) -> Union[bool, int]:
        return True, tindex + 1

    def help(self, tokens: List[str], tindex: int, **kwargs) -> List[str]:
        return [""]

    def complete(self, tokens: List[str], tindex: int, **kwargs) -> List[str]:
        return [""]


class StrContent(Content):
    def __init__(self, vault: str, **kwargs):
        super(StrContent, self).__init__(vault, **kwargs)
        self.klass: int = ContentKlass.STR


class KeywordContent(Content):
    def __init__(self, vault: str, **kwargs):
        super(KeywordContent, self).__init__(vault, **kwargs)
        self.klass: int = ContentKlass.KEYWORD

    def match(self, tokens: List[str], tindex: int, **kwargs) -> Union[bool, int]:
        if tokens[tindex] == self._vault:
            return True, tindex + 1
        return False, tindex


class IntContent(Content):
    def __init__(self, vault: int, **kwargs):
        super(IntContent, self).__init__(vault, **kwargs)
        self.klass: int = ContentKlass.INT

    def match(self, tokens: List[str], tindex: int, **kwargs) -> Union[bool, int]:
        if tokens[tindex] == str(self._vault):
            return True, tindex + 1
        return False, tindex


class CommandContent(Content):
    def __init__(self, vault: str, **kwargs):
        super(CommandContent, self).__init__(vault, **kwargs)
        self.klass: int = ContentKlass.COMMAND
        self.command = kwargs.get("command", None)

    def call(self, **kwargs):
        return self.command(**kwargs)

    def match(self, tokens: List[str], tindex: int, **kwargs) -> Union[bool, int]:
        if tokens[tindex] == self._vault:
            return True, tindex + 1
        return False, tindex
