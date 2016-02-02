# -*- coding: utf-8 -*-
"""
Created on Mon May 26 23:42:03 2014

@author: Vespa
"""


from support import *
import sys
import codecs
    
############################常量定义

#####排序方式
#收藏
TYPE_SHOUCANG = 'stow'
#评论数
TYPE_PINGLUN = 'review'
#播放数
TYPE_BOFANG = 'hot'
#硬币数
TYPE_YINGBI = 'promote'
#用户评分
TYPE_PINGFEN = 'comment'
#弹幕数
TYPE_DANMU = 'damku'
#拼音
TYPE_PINYIN = 'pinyin'
#投稿时间
TYPE_TOUGAO = 'default'
############################常量定义结束

def GetUserInfo(url):
    """
由GetUserInfoBymid(mid)或者GetUserInfoByName(name)调用
返回：
    用户信息
    """
    jsoninfo = JsonInfo(url)
    user = User(jsoninfo.Getvalue('mid'), jsoninfo.Getvalue('name'))
    user.isApprove = jsoninfo.Getvalue('approve')
    #b站现在空间名暂时不返回
    #user.spaceName = jsoninfo.Getvalue('spacename')
    user.sex = jsoninfo.Getvalue('sex')
    user.rank = jsoninfo.Getvalue('rank')
    user.avatar = jsoninfo.Getvalue('face')
    user.follow = jsoninfo.Getvalue('attention')
    user.fans = jsoninfo.Getvalue('fans')
    user.article = jsoninfo.Getvalue('article')
    user.place = jsoninfo.Getvalue('place')
    user.description = jsoninfo.Getvalue('description')
    user.friend = jsoninfo.Getvalue('friend')
    user.DisplayRank = jsoninfo.Getvalue('DisplayRank')
    user.followlist = []
    for fo in jsoninfo.Getvalue('attentions'):
        user.followlist.append(fo)
    return user

def GetUserInfoBymid(mid):
    """
输入：
    mid：查询的用户的id
返回：
    查看GetUserInfo()函数
    """
    mid = GetString(mid)
    url = 'http://api.bilibili.cn/userinfo'+"?mid="+mid
    return GetUserInfo(url)

def GetUserInfoByName(name):
    """
输入：
    mid：查询的用户的昵称
返回：
    查看GetUserInfo()函数
    """
    name = GetString(name)
    url = 'http://api.bilibili.cn/userinfo'+"?user="+name
    return GetUserInfo(url)

def GetVideoOfZhuanti(spid, season_id=None, bangumi=None):
    """
输入：
    spid:专题id
    season_id：分季ID
    bangumi：设置为1返回剧番，不设置或者设置为0返回相关视频
返回：
    视频列表，包含av号，标题，封面和观看数
    """
    url = ' http://api.bilibili.cn/spview?spid='+GetString(spid)
    if season_id:
        url += '&season_id='+GetString(season_id)
    if bangumi:
        url += '&bangumi='+GetString(bangumi)
    jsoninfo = JsonInfo(url)
    videolist = []
    for video_idx in jsoninfo.Getvalue('list'):
        video_idx = DictDecode2UTF8(video_idx)
        video = Video(video_idx['aid'],video_idx['title'])
        video.cover = video_idx['cover']
        video.guankan = video_idx['click']
        if video_idx.has_key('episode'):
            video.episode = video_idx['episode']
        video.src = video_idx["from"]
        video.cid = video_idx["cid"]
        video.page = video_idx["page"]
        videolist.append(video)
    return videolist

def GetComment(aid, page = None, pagesize = None, order = None):
    """
输入：
    aid：AV号
    page：页码
    pagesize：单页返回的记录条数，最大不超过300，默认为10。
    order：排序方式 默认按发布时间倒序 可选：good 按点赞人数排序 hot 按热门回复排序
返回：
    评论列表
    """
    url = 'http://api.bilibili.cn/feedback?aid='+GetString(aid)
    if page:
        url += '&page='+GetString(page)
    if pagesize:
        url += '&pagesize='+GetString(pagesize)
    if order:
        url += '&order='+GetString(order)
    jsoninfo = JsonInfo(url)
    commentList = CommentList()
    commentList.comments = []
    commentList.commentLen = jsoninfo.Getvalue('totalResult')
    commentList.page = jsoninfo.Getvalue('pages')
    idx = 0
    while jsoninfo.Getvalue(str(idx)):
        liuyan = Comment()
        liuyan.lv = jsoninfo.Getvalue(str(idx),'lv')
        liuyan.fbid = jsoninfo.Getvalue(str(idx),'fbid')
        liuyan.msg = jsoninfo.Getvalue(str(idx),'msg')
        liuyan.ad_check = jsoninfo.Getvalue(str(idx),'ad_check')
        liuyan.post_user.mid = jsoninfo.Getvalue(str(idx),'mid')
        liuyan.post_user.avatar = jsoninfo.Getvalue(str(idx),'face')
        liuyan.post_user.rank = jsoninfo.Getvalue(str(idx),'rank')
        liuyan.post_user.name = jsoninfo.Getvalue(str(idx),'nick')
        commentList.comments.append(liuyan)
        idx += 1
    return commentList

def GetAllComment(aid, order = None):
    """
获取一个视频全部评论，有可能需要多次爬取，所以会有较大耗时
输入：
    aid：AV号
    order：排序方式 默认按发布时间倒序 可选：good 按点赞人数排序 hot 按热门回复排序
返回：
    评论列表
    """
    MaxPageSize = 300
    commentList = GetComment(aid=aid, pagesize=MaxPageSize, order=order)
    if commentList.page == 1:
        return commentList
    for p in range(2,commentList.page+1):
        t_commentlist = GetComment(aid=aid,pagesize=MaxPageSize,page=p,order=order)
        for liuyan in t_commentlist.comments:
            commentList.comments.append(liuyan)
        time.sleep(0.5)
    return commentList

def GetVideoInfo(aid, appkey,page = 1, AppSecret=None, fav = None):
    """
获取视频信息
输入：
    aid：AV号
    page：页码
    fav：是否读取会员收藏状态 (默认 0)
    """
    paras = {'id': GetString(aid),'page': GetString(page)}
    if fav:
        paras['fav'] = fav
    url =  'http://api.bilibili.cn/view?'+GetSign(paras,appkey,AppSecret)
    jsoninfo = JsonInfo(url)
    video = Video(aid,jsoninfo.Getvalue('title'))
    video.guankan = jsoninfo.Getvalue('play')
    video.commentNumber = jsoninfo.Getvalue('review')
    video.danmu = jsoninfo.Getvalue('video_review')
    video.shoucang = jsoninfo.Getvalue('favorites')
    video.description = jsoninfo.Getvalue('description')
    video.tag = []
    taglist = jsoninfo.Getvalue('tag')
    if taglist:
        for tag in taglist.split(','):
            video.tag.append(tag)
    video.cover = jsoninfo.Getvalue('pic')
    video.author = User(jsoninfo.Getvalue('mid'),jsoninfo.Getvalue('author'))
    video.page = jsoninfo.Getvalue('pages')
    video.date = jsoninfo.Getvalue('created_at')
    video.credit = jsoninfo.Getvalue('credit')
    video.coin = jsoninfo.Getvalue('coins')
    video.spid = jsoninfo.Getvalue('spid')
    video.cid = jsoninfo.Getvalue('cid')
    video.offsite = jsoninfo.Getvalue('offsite')
    video.partname = jsoninfo.Getvalue('partname')
    video.src = jsoninfo.Getvalue('src')
    video.tid = jsoninfo.Getvalue('tid')
    video.typename = jsoninfo.Getvalue('typename')
    video.instant_server = jsoninfo.Getvalue('instant_server')
    # video.created = jsoninfo.Getvalue('created')
    return video


def GetBangumi(appkey, btype = None, weekday = None, AppSecret=None):
    """
获取新番信息
输入：
    btype：番剧类型 2: 二次元新番 3: 三次元新番 默认(0)：所有
    weekday:周一:1 周二:2 ...周六:6
    """
    paras = {}
    if btype != None and btype in [2,3]:
        paras['btype'] = GetString(btype)
    if weekday != None:
        paras['weekday'] = GetString(weekday)
    url =  'http://api.bilibili.cn/bangumi?' + GetSign(paras, appkey, AppSecret)
    jsoninfo = JsonInfo(url)
    bangumilist = []
    if jsoninfo.Getvalue('code') != 0:
        print jsoninfo.Getvalue('error')
        return bangumilist
    for bgm in jsoninfo.Getvalue('list'):
        bangumi = Bangumi()
        bgm = DictDecode2UTF8(bgm)
        bangumi.typeid = bgm['typeid']
        bangumi.lastupdate = bgm['lastupdate']
        bangumi.areaid = bgm['areaid']
        bangumi.bgmcount = getint(bgm['bgmcount'])
        bangumi.title = bgm['title']
        bangumi.lastupdate_at = bgm['lastupdate_at']
        bangumi.attention = bgm['attention']
        bangumi.cover = bgm['cover']
        bangumi.priority = bgm['priority']
        bangumi.area = bgm['area']
        bangumi.weekday = bgm['weekday']
        bangumi.spid = bgm['spid']
        bangumi.new = bgm['new']
        bangumi.scover = bgm['scover']
        bangumi.mcover = bgm['mcover']
        bangumi.click = bgm['click']
        bangumi.season_id = bgm['season_id']
        bangumi.click = bgm['click']
        bangumi.video_view = bgm['video_view']
        bangumilist.append(bangumi)
    return bangumilist

def GetDanmukuContent(cid):
    """
    获取弹幕内容
    """
    content = GetRE(GetDanmuku(cid),r'<d p=[^>]*>([^<]*)<')
    return content

def GetDanmuku(cid):
    """
    获取弹幕xml内容
    """
    cid = getint(cid)
    url = "http://comment.bilibili.cn/%d.xml"%(cid)
    content = zlib.decompressobj(-zlib.MAX_WBITS).decompress(getURLContent(url))
    return content

def ParseDanmuku(cid):
    """
    按时间顺序返回每一条弹幕
    """
    Danmuku = []
    Danmuku.extend(ParseComment(GetDanmuku(cid)))
    Danmuku.sort(key=lambda x:x.t_video)
    return Danmuku

    
def CrawlVideo(av_number, appkey, folder, AppSecret=None):
    
    url = "http://www.bilibili.com/video/"+av_number+"/"
    overseas=False
    url_get_media = 'http://interface.bilibili.com/playurl?' if not overseas else 'http://interface.bilibili.com/v_cdn_play?'
    regex_match = re.findall('http:/*[^/]+/video/av(\\d+)(/|/index.html|/index_(\\d+).html)?(\\?|#|$)',url)
    if not regex_match:
        raise ValueError('Invalid URL: %s' % url)
    aid = regex_match[0][0]
    pid = regex_match[0][2] or '1'
    
    video = GetVideoInfo(aid,appkey,pid,AppSecret)
    cid = video.cid
    print "aid:"+str(aid)
    print "cid:"+str(cid)
    print "pid:"+str(pid)
    
    meta_file = codecs.open('%s/meta.csv' % folder, 'w', 'utf-8')
    
    meta_line = str(video.title) + "," + str(video.guankan) +"," + str(video.commentNumber) + "," + str(video.danmu) +"," + str(video.shoucang)+","+str(video.description)+"\n"
    meta_file.write(meta_line)
    meta_file.close()
    
    commentList = GetAllComment(aid)
    comment_file = codecs.open('%s/comment.csv' % folder, 'w', 'utf-8')
    for liuyan in commentList.comments:
        comment_line = str(liuyan.lv)+","+str(liuyan.post_user.name)+','+str(liuyan.msg)+"\n"
        comment_file.write(comment_line)
        
    comment_file.close()
    
    print "片名:"+video.title
    print "播放数:"+ video.guankan
    print "评论数:"+video.commentNumber
    print "收藏数:"+video.shoucang
    print "介绍:"+video.description
    
    # single video
    if video.page == 1:
        danmu_file = codecs.open('%s/danmu.csv' % folder, 'w', 'utf-8')
        for danmu in ParseDanmuku(cid):
            # print danmu.t_video,danmu.t_stamp,danmu.content, danmu.mid_crc, danmu.danmu_type, danmu.danmu_color
            danmu_line = str(danmu.t_video) + "," + str(danmu.t_stamp) + "," + str(danmu.content) + "," + str(danmu.mid_crc) + "," + str(danmu.danmu_type) + "," + str(danmu.danmu_color) + "\n"
            danmu_file.write(danmu_line)
        danmu_file.close()
        
        
    # multiple videos     
    else:
        for i in range(0,video.page):
            danmu_file = codecs.open('%s/danmu_%s.csv' % (folder, i), 'w', 'utf-8')
            for danmu in ParseDanmuku(cid):
                # print danmu.t_video,danmu.t_stamp,danmu.content, danmu.mid_crc, danmu.danmu_type, danmu.danmu_color
                danmu_line = str(danmu.t_video) + "," + str(danmu.t_stamp) + "," + str(danmu.content) + "," + str(danmu.mid_crc) + "," + str(danmu.danmu_type) + "," + str(danmu.danmu_color) + "\n"
                danmu_file.write(danmu_line)
            danmu_file.close()
            cid = str(int(cid)+1)
    

def GetVideoOfUploader(mid,pagesize=20,page=1):
    url = 'http://space.bilibili.com/ajax/member/getSubmitVideos?mid=%d&pagesize=%d&page=%d'%(getint(mid),getint(pagesize),getint(page))
    jsoninfo = JsonInfo(url)
    videolist = []
    for video_t in jsoninfo.Getvalue('data','list'):
        video = Video(video_t['aid'],video_t['title'])
        video.Iscopy = video_t['copyright']
        video.tid = video_t['typeid']
        video.typename = video_t['typename']
        video.subtitle = video_t['subtitle']
        video.guankan = video_t['play']
        video.commentNumber = video_t['review']
        video.shoucang = video_t['favorites']
        video.author = User(video_t['mid'],video_t['author'])
        video.description = video_t['description']
        video.date = video_t['create']
        video.cover = video_t['pic']
        video.credit = video_t['credit']
        video.coin = video_t['coins']
        video.duration = video_t['duration']
        video.danmu = video_t['comment']
        videolist.append(video)
    return videolist

    
if __name__ == "__main__":
    
    # python bilibili.py av314
    
    av_number = sys.argv[1]
    av_folder = r'./%s' % av_number
    if os.path.exists(av_folder):
        pass
    else:
        os.makedirs(av_folder)
    
    appkey = '85eb6835b0a1034e'
    secretkey = '2ad42749773c441109bdc0191257a664'
    
    url = "http://www.bilibili.com/video/"+av_number+"/"
    # print GetVideoPages(av_number,appkey,secretkey)
    CrawlVideo(av_number,appkey = appkey,folder=av_folder, AppSecret=secretkey)