#!/usr/bin/env python
# -*- coding=utf-8 -*-
# 哔哩哔哩历史弹幕 (XML) 下载器
# 使用：bilibili.py av314

import StringIO
import datetime
import gzip
import json
import os
import re
import urllib2
import zlib
import sys

# 接受参数 av****** 并创建 xml 保存目录
av_number = sys.argv[1]
xml_folder = r'./%s' % av_number
if os.path.exists(xml_folder):
    pass
else:
    os.makedirs(xml_folder)

# 处理 bilibili 视频页面
video_page_url = 'http://www.bilibili.tv/video/%s' % av_number
video_page_request = urllib2.Request(video_page_url)
video_page_gz = urllib2.urlopen(video_page_request).read()
# gzip 解压
# 方法来自 http://stackoverflow.com/a/3947241
video_page_buffer = StringIO.StringIO(video_page_gz)
video_page_html = gzip.GzipFile(fileobj = video_page_buffer).read()

# 获取视频 cid
cid_number = re.findall(r'cid=(\d+)', video_page_html)[0]

# 获取视频所有历史弹幕
comments_page_url = 'http://comment.bilibili.tv/rolldate,%s' % cid_number
comments_page_request = urllib2.Request(comments_page_url)
comments_page_zip = urllib2.urlopen(comments_page_request).read()
# deflate 解压
# 方法来自 http://stackoverflow.com/a/9583564
comments_page_json = zlib.decompressobj(-zlib.MAX_WBITS).decompress(comments_page_zip)

# 解析历史弹幕信息
comments_python_object = json.loads(comments_page_json)
for i in range(0, len(comments_python_object)):
    comment_timestamp = comments_python_object[i]['timestamp']
    comment_date = datetime.datetime.fromtimestamp(int(comment_timestamp)).strftime('%Y%m%d')
    comment_then_url = 'http://comment.bilibili.tv/dmroll,%s,%s' % (comment_timestamp, cid_number)
    comment_then_request = urllib2.Request(comment_then_url)
    comment_then_zip = urllib2.urlopen(comment_then_request).read()
    comment_then_xml = zlib.decompressobj(-zlib.MAX_WBITS).decompress(comment_then_zip)
    comment_file = open('%s/%s.xml' % (xml_folder, comment_date), 'wb')
    comment_file.write(comment_then_xml)
    comment_file.close()
else:
    pass