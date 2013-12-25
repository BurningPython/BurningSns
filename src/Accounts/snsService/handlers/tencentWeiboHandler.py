'''
Created on 2013年12月18日

@author: july
'''

#腾讯微博相关
client_id = "801453781"
client_secret = "c2ee75038d707a610c7a4a10c0377c2e"
api_url = "https://open.t.qq.com/api/%s"
api_common_parm = "oauth_consumer_key=%s&access_token=%s&openid=%s&oauth_version=2.a&scope=all"

import json
from urllib.request import urlopen
from urllib.parse import urlencode

from django.core.exceptions import ObjectDoesNotExist

from .baseHandler import *


class ts_utils(object):
    @staticmethod
    def get_api_data(api_name, token, method = "get", **params):

        base_url = api_url % api_name
        common_parm = api_common_parm % (token.access_token, token.openid, client_id)
        if method.lower() == "get":
            base_url += "?"
            api_param = ""
            for key, value in params:
                api_param += "&%s=%s" % (key, value)
            target_url = base_url + common_parm + api_param
            ret = urlopen(target_url).read().decode("utf-8")
        else:
            querystring = common_parm + "&" + urlencode(params)
            ret = urlopen(base_url, data = bytes(querystring.encode('utf8'))).read().decode('utf8')
        return json.loads(ret)


class TencentWeiboHandler(BaseHandler):
    """

    """

    def __init__(self, user):
        """
        """
        super(BaseHandler, self).__init__()
        self.statusService = StatusService(user)
        self.commentsService = CommentsService(user)
        self.favouritesService = FavouritesService(user)


class StatusService(IStatusService):
    """
    动态服务
    """

    def __init__(self, user):
        super(IStatusService, self).__init__()
        self.user = user
        try:
            self.token = user.openauth_set.get(site = "腾讯微博")
        except ObjectDoesNotExist:
            self.token = None

    def GetFriendsStatuses(self, **params):
        """
        获取好友动态列表
        """
        api_name = "statuses/home_timeline"
        params["clientip"] = self.user.ip_address

        ret_data = ts_utils.get_api_data(api_name, self.token, method = "post", **params)
        return ret_data

    def Repost(self, statusid, **params):
        """
        转发微博
        """

        api_name = "t/re_add"

        params["clientip"] = self.user.ip_address

        ret_data = ts_utils.get_api_data(api_name, self.token, method = "post", **params)

        return ret_data

    def Destroy(self, statusid, **params):
        """
        删除微博
        """

        api_name = "t/del"

        params["clientip"] = self.user.ip_address

        ret_data = ts_utils.get_api_data(api_name, self.token, method = "post", **params)

        return ret_data

    def Update(self, content, **params):
        """
        发微博：微博内容
        """

        api_name = "t/add"
        params["clientip"] = self.user.ip_address

        ret_data = ts_utils.get_api_data(api_name, self.token, method = "post", **params)
        return ret_data

#评论服务
class CommentsService(ICommentService):
    """

    """

    def __init__(self, user):
        super(ICommentService, self).__init__()
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
class FavouritesService(IFavoriteService):
    """

    """

    def __init__(self, user):
        super(IFavoriteService, self).__init__()

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


if __name__ == '__main__':
    pass