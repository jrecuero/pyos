from typing import Any


class Content:
    def __init__(self, clearance: Any):
        self.clearance: Any = clearance

    def call(self, **kwargs):
        return self.clearance(**kwargs) if self.clearance else [None, False]
