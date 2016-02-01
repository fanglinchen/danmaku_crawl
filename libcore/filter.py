import re
from .const import BOTTOM


class BaseFilter(object):

    def match(self, danmaku):
        return False


class GuestFilter(BaseFilter):
    def match(self, danmaku):
        return danmaku.is_guest


class BottomFilter(BaseFilter):
    def match(self, danmaku):
        if danmaku.is_applaud:
            return False
        return danmaku.style == BOTTOM


class CustomFilter(BaseFilter):
    def __init__(self, lines):
        self.lines = lines
        self.regexps = self._regexps()

    def _regexps(self):
        return list(map(re.compile, self.lines))

    def match(self, danmaku):
        for regexp in self.regexps:
            if regexp.search(danmaku.content):
                return True
        return False

guest_filter = GuestFilter()
bottom_filter = BottomFilter()
