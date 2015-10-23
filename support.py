# -*- coding: utf-8 -*-
"""
Created on Mon May 26 23:59:09 2014

@author: Vespa
"""
import urllib2
import urllib
import re
import json
import zlib
import gzip
import xml.dom.minidom
import hashlib
from biclass import *
import time
import sys
import os
from GetAssDanmaku import *
def GetRE(content,regexp):
    return re.findall(regexp, content)

def getURLContent(url):
    while True:
        flag = 1
        try:
            headers = {'User-Agent':'Mozilla/5.0 (Windows U Windows NT 6.1 en-US rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
            req = urllib2.Request(url = url,headers = headers)
            content = urllib2.urlopen(req).read()
        except:
        	flag = 0
        	time.sleep(5)
        if flag == 1:
        	break
    return content

class JsonInfo():
    def __init__(self,url):
        self.info = json.loads(getURLContent(url))
        if self.info.has_key('code') and self.info['code'] != 0:
            if self.info.has_key('message'):
                print "【Error】code=%d, msg=%s, url=%s"%(self.info['code'],self.Getvalue('message'),url)
            elif self.info.has_key('error'):
                print "【Error】code=%d, msg=%s, url=%s"%(self.info['code'],self.Getvalue('error'),url)
            error = True
    def Getvalue(self,*keys):
        if len(keys) == 0:
            return None
        if self.info.has_key(keys[0]):
            temp = self.info[keys[0]]
        else:
            return None
        if len(keys) > 1:
            for key in keys[1:]:
                if temp.has_key(key):
                    temp = temp[key]
                else:
                    return None
        if isinstance(temp,unicode):
            temp = temp.encode('utf8')
        return temp
    info = None
    error = False

def GetString(t):
    if type(t) == int:
        return str(t)
    return t

def getint(string):
    try:
        i = int(string)
    except:
        i = 0
    return i

def DictDecode2UTF8(dict):
    for keys in dict:
        if isinstance(dict[keys],unicode):
            dict[keys] = dict[keys].encode('utf8')
    return dict


def GetSign(params, appkey, AppSecret=None):
    
    params['appkey']=appkey
    data = ""
    paras = params.keys()
    paras.sort()
    for para in paras:
        if data != "":
            data += "&"
        data += para + "=" + str(urllib.quote(GetString(params[para])))
    if AppSecret == None:
        return data
    m = hashlib.md5()
    m.update(data+AppSecret)
    return data+'&sign='+m.hexdigest()

def ParseComment(danmu):
    dom = xml.dom.minidom.parseString(danmu)
    comment_element = dom.getElementsByTagName('d')
    for i, comment in enumerate(comment_element):
        p = str(comment.getAttribute('p')).split(',')
        danmu = Danmu()
        danmu.t_video = float(p[0])
        danmu.danmu_type = int(p[1])
        danmu.t_stamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(p[4])))
        danmu.mid_crc = p[6]
        danmu.danmu_color = ConvertColor(int(p[3]))
        if len(comment.childNodes) != 0:
            danmu.content = str(comment.childNodes[0].wholeText).replace('/n', '\n')
        else:
            danmu.content = ""
        yield danmu