import os
import re
import json
from libcore.const import NOT_SUPPORT, SCROLL, TOP, BOTTOM
from libcore.utils import extract_params
from libcore.fetcher import fetch
from libcore.danmaku import BaseDanmaku
from libcore.video import BaseVideo
import time
import sys
import codecs

class Danmaku(BaseDanmaku):

    def __init__(self, entry):
        self.entry = entry
        self.raw = self._raw()
        self.start = self._start()
        self.style = self._style()
        self.color = self._color()
        self.commenter = self._commenter()
        self.content = self._content()
        self.size_ratio = self._size_ratio()
        self.is_guest = self._is_guest()
        self.publish = self._publish()
        
    def _raw(self):
        attr_string = self.entry['c']
        content_string = self.entry['m']
        attrs = attr_string.split(',')
        props = {
            'start': float(attrs[0]),
            'color': int(attrs[1]),
            'style': int(attrs[2]),
            'size': int(attrs[3]),
            'commenter': attrs[4],
            # time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(p[4])))
            'publish': time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(float(attrs[5]))),
            'content': content_string
        }
        return props

    def _start(self):
        return self.raw['start']

    def _publish(self):
        return self.raw['publish']
        
    def _style(self):
        MAPPING = {
            1: SCROLL,
            2: NOT_SUPPORT,
            3: NOT_SUPPORT,
            4: BOTTOM,
            5: TOP,
            6: NOT_SUPPORT,
            7: NOT_SUPPORT,
            8: NOT_SUPPORT,
        }
        return MAPPING.get(self.raw['style'], NOT_SUPPORT)

    def _color(self):
        return self.raw['color']

    def _commenter(self):
        return self.raw['commenter']

    def _content(self):
        return self.raw['content']

    def _size_ratio(self):
        FLASH_PLAYER_FONT_SIZE = 25
        return self.raw['size'] / FLASH_PLAYER_FONT_SIZE

    def _is_guest(self):
        return len(self.raw['commenter']) == 14

     
        
def extract_params_from_normal_page(url):
    aid_reg = re.compile('/ac([0-9]+)')
    vid_reg = re.compile('data-vid="(.+?)" .+ active')
    h1_reg = re.compile('<h1 id="txt-title-view">(.+?)</h1>')
    text = fetch(url)

    params = {}
    params['aid'] = aid_reg.findall(url)[0]
    params['vid'] = vid_reg.findall(text)[0]
    params['h1'] = h1_reg.findall(text)[0]
    return params
    
def CrawlVideo(ac_number, folder):
    normal_prefix = 'http://www.acfun.tv/v/'
    url = normal_prefix + ac_number
    if '_' not in url:
        url += '_1'
    params = extract_params_from_normal_page(url)

    
    aid=params['aid']
    vid=params['vid']
    h1=params['h1']
    print aid
    print vid
    print h1

    page_size = 1000
    page_max = 100
    tpl = 'http://danmu.aixifan.com/V2/{}?pageSize={}&pageNo={}'

    entries = []
    for i in range(1, page_max):
        url = tpl.format(vid, page_size, i)
        text = fetch(url)
        page_entries = json.loads(text)[2]
        entries.extend(page_entries)

        if len(page_entries) < page_size:
            break

    orignal_danmakus = map(Danmaku, entries)
    ordered_danmakus = sorted(orignal_danmakus, key=lambda d: d.start)
    danmu_file = codecs.open('%s/danmu.csv' % folder, 'w', 'utf-8')
    for danmaku in ordered_danmakus:
        danmu_line = str(danmaku.start) + "," + str(danmaku.publish) + "," + danmaku.content + "," + str(danmaku.commenter) + ","  + str(danmaku.color) + "\n"
        danmu_file.write(danmu_line)
    danmu_file.close()

if __name__ == "__main__":
    # python acfun.py ac1552414
    ac_number = sys.argv[1]
    ac_folder = r'./%s' % ac_number
    if os.path.exists(ac_folder):
        pass
    else:
        os.makedirs(ac_folder)
    
    CrawlVideo(ac_number,ac_folder)