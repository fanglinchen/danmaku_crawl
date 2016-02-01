from .const import NOT_SUPPORT


class BaseDanmaku(object):
    def __init__(self):

        self.start = 0

        self.style = NOT_SUPPORT

        self.color = 0xFFFFFF

        self.commenter = ''

        self.content = ''

        self.size_ratio = 1

        self.is_guest = False
        
        self.publish = ''