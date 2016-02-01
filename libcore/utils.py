import re
import colorsys
from math import ceil
from urlparse import unquote
from unicodedata import east_asian_width


def intceil(number):
    return int(ceil(number))


def display_length(text):
    width = 0
    for char in text:
        width += east_asian_width(char) == 'Na' and 1 or 2
    return width


def correct_typos(text):
    text = text.replace('/n', '\\N')
    text = text.replace('&gt;', '>')
    text = text.replace('&lt;', '<')

    return text


def s2hms(seconds):
    if seconds < 0:
        return '0:00:00.00'

    i, d = divmod(seconds, 1)
    m, s = divmod(i, 60)
    h, m = divmod(m, 60)
    (h, m, s, d) = map(int, (h, m, s, d * 100))
    return '{:d}:{:02d}:{:02d}.{:02d}'.format(h, m, s, d)


def hms2s(hms):

    nums = hms.split(':')
    seconds = 0
    for i in range(len(nums)):
        seconds += int(nums[-i - 1]) * (60 ** i)
    return seconds


def xhms2s(xhms):

    args = xhms.replace('+', ' +').replace('-', ' -').split(' ')
    result = 0
    for hms in args:
        seconds = hms2s(hms)
        result += seconds
    return result


def int2rgb(integer):
    return hex(integer).upper()[2:].zfill(6)


def int2bgr(integer):
    rgb = int2rgb(integer)
    bgr = rgb[4:6] + rgb[2:4] + rgb[0:2]
    return bgr


def int2hls(integer):
    rgb = int2rgb(integer)
    rgb_decimals = map(lambda x: int(x, 16), (rgb[0:2], rgb[2:4], rgb[4:6]))
    rgb_coordinates = map(lambda x: x // 255, rgb_decimals)
    hls_corrdinates = colorsys.rgb_to_hls(*rgb_coordinates)
    hls = (
        hls_corrdinates[0] * 360,
        hls_corrdinates[1] * 100,
        hls_corrdinates[2] * 100
    )
    return hls


def is_dark(integer):
    if integer == 0:
        return True

    hls = int2hls(integer)
    hue, lightness = hls[0:2]

    if (hue > 30 and hue < 210) and lightness < 33:
        return True
    if (hue < 30 or hue > 210) and lightness < 66:
        return True

    return False


def extract_params(argv):
    argv = unquote(argv)
    params = {}
    for arg in argv.split(','):
        key, value = arg.split('=')
        params[key] = value
    return params


def play_url_fix(url):
    if url.startswith('http://videoctfs.tc.qq.com/'):
        return url.replace('http://videoctfs.tc.qq.com/',
                           'http://183.60.73.103/', 1)

    if url.startswith('http://vhot2.qqvideo.tc.qq.com/'):
        key_part = re.findall(
            'http://vhot2.qqvideo.tc.qq.com/(.+?)\?.*', url)[0]
        url = 'http://vsrc.store.qq.com/{}?'.format(key_part)
        url += 'channel=vhot2&sdtfrom=v2&r=256&rfc=v10'
        return url

    return url
