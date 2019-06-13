from typing import List, Tuple


class Content(object):
    def match(self, tokens: List[str], tindex: int, **kwargs) -> Tuple:
        return True, tindex + 1

    def help(self, tokens: List[str], tindex: int, **kwargs) -> List[str]:
        return [""]

    def complete(self, tokens: List[str], tindex: int, **kwargs) -> List[str]:
        return [""]
