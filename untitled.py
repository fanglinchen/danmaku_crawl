    #获取最热视频
    # videoList = GetPopularVideo([2014,05,20],[2014,05,27],TYPE_BOFANG,0,1)
    # for video in videoList:
    #     print video.title
     #获取用户信息
    # user = GetUserInfoBymid('72960')
    # print user.name,user.DisplayRank
    # user = GetUserInfoByName('vespa')
    # print user.friend
    #获取专题视频信息
    videolist = GetVideoOfZhuanti('46465',bangumi=1)
    for video in videolist:
        print video.title
    #获取评论
    # commentList = GetAllComment('1154794')
    # for liuyan in commentList.comments:
    #     print liuyan.lv,'-',liuyan.post_user.name,':',liuyan.msg
    #获取视频信息

    
    
    video = GetVideoInfo(1152959,appkey=appkey,AppSecret=secretkey)
    
    for tag in video.tag:
        print tag
        
    print "播放数："+ video.guankan
    print "评论数:"+video.commentNumber
    print "弹幕数:"+video.danmu
    print "收藏数:"+video.danmu
    print "介绍:"+video.description
    
    

    #获取分类排行
    # [page,name,videolist] = GetRank(appkey,tid='0',order='hot',page=1,pagesize = 100,begin=[2014,1,1],end=[2014,2,1],click_detail='true')
    # for video in videolist:
    #     print video.title,video.play_site
    #获取弹幕
    # video = GetVideoInfo(1677082,appkey,AppSecret=secretkey)
    # for danmu in GetDanmukuContent(video.cid):
    #     print danmu
    #获取弹幕ASS文件
    # video = GetVideoInfo(1152959,appkey=appkey,AppSecret=secretkey)
    # Danmaku2ASS(GetDanmuku(video.cid),r'%s/Desktop/%s.ass'%(os.path.expanduser('~'),video.title.replace(r'/','')), 640, 360, 0, 'sans-serif', 15, 0.5, 10, False)
    # 分解弹幕
    # video = GetVideoInfo(2546876,appkey=appkey,AppSecret=secretkey)
    # for danmu in ParseDanmuku(4843281):
    #     print danmu.t_video,danmu.t_stamp,danmu.content, danmu.mid_crc, danmu.danmu_type, danmu.danmu_color
    # print "--------------"
    # for danmu in ParseDanmuku(4843280):
    #     print danmu.t_video,danmu.t_stamp,danmu.content, danmu.mid_crc, danmu.danmu_type, danmu.danmu_color
    #获取视频下载地址列表
    media_urls = GetBilibiliUrl('http://www.bilibili.com/video/av3087062/index_3.html',appkey = appkey,AppSecret=secretkey)
    print(media_urls)
    #视频搜索
    # for video in biliVideoSearch(appkey,secretkey,'rwby'):
    #     print video.title
    #专题搜索
    # for zhuanti in biliZhuantiSearch(appkey,secretkey,'果然'):
    #     print zhuanti.title
    # for video in GetVideoOfUploader(72960,300):
    #     print video.title
