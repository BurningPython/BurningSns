"""

    各位程序猿注意啦，老板说这个类是所有社交网站的接口类，也就是说你们写的各家社交网站模块要实现这些接口。
    只是个纸老虎，其实这个文件是没有用的。

"""
#模块顶层服务
class BaseHandler(object):
    site = ''                    #社交网站名称
    domain = ''    #域名

    statusesService = ""
    commentsService = ""
    favouritesService = ""
    shortUrlsService = ""

    def __init__(self, user):
        # self.StatusesService = IStatusService(user)
        # self.TencentWeiboCommentService = ICommentsService(user)
        # self.TencentWeiboFavoriteService = IFavouritesService(user)
        # self.ShortUrlsService = IShortUrlsService(user)
        pass


class IStatusService(object):
    """
    动态服务
    """

    def __init__(self, user):
        self.user = user
        pass

    def GetFriendsStatuses(self, **parms):            #获取好友动态列表
        raise Exception("接口(%s)未实现" % self.__name__)
        pass

    def Repost(self, statusid, **parms):        #转发：微博ID
        raise Exception("接口(%s)未实现" % self.__name__)
        pass

    def Destroy(self, statusid, **parms):        #删除：微博ID
        raise Exception("接口(%s)未实现" % self.__name__)
        pass

    def Update(self, content, **parms):        #发微博：微博内容
        raise Exception("接口(%s)未实现" % self.__name__)
        pass

#评论服务
class ICommentService(object):
    """

    """

    def __init__(self, user):
        self.user = user
        pass

    def GetComments(self, statusid, **parms):        #获取指定ID的微博的所有评论
        raise Exception("接口(%s)未实现" % self.__name__)
        pass

    def Create(self, statusid, comment, **parms):    #新建一条评论:微博ID，评论内容
        raise Exception("接口(%s)未实现" % self.__name__)
        pass

    def Destory(self, commentid, **parms):            #删除一条评论：评论ID
        raise Exception("接口(%s)未实现" % self.__name__)
        pass

    def Reply(self, statusid, commentid, content, **parms):    #回复一条评论，微博ID，评论ID，回复内容
        raise Exception("接口(%s)未实现" % self.__name__)
        pass

#收藏服务
class IFavoriteService(object):
    """

    """

    def __init__(self, user):
        self.user = user
        pass

    def GetFavorites(self, **parms):                #获取所有收藏
        raise Exception("接口(%s)未实现" % self.__name__)
        pass

    def GetFavorite(self, statusid, **parms):        #获取单条收藏：微博ID
        raise Exception("接口(%s)未实现" % self.__name__)
        pass

    def Create(self, statusid, **parms):            #添加收藏：微博ID
        raise Exception("接口(%s)未实现" % self.__name__)
        pass

    def Destory(self, statusid, **parms):            #取消收藏：微博ID
        raise Exception("接口(%s)未实现" % self.__name__)
        pass

#长短链转化
class IShortUrlService(object):
    """
    """

    def __init__(self, user):
        self.user = user
        pass

    def Shorten(self, longurl, **parms):            #长链转短链：长链接
        raise Exception("接口(%s)未实现" % self.__name__)
        pass

    def Expand(self, shorturl, **parms):            #短链转长链：短链接
        raise Exception("接口(%s)未实现" % self.__name__)
        pass

class DataResponse(object):
    """
    请求响应数据包
    """

    data = []
    code = ""
    message = ""
    site = ""

    def __init__(self, ret = 0, code = 0, message = "", site="unknow", data = None):
        """
        ret:0为正常,1为错误
        code:错误编码
        message:错误描述
        data:数据
        """
        self.ret = ret
        self.code = code
        self.message = message
        self.site = ""
        if data:
            self.data = data