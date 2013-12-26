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

from accounts.snsService.handlers.baseHandler import *


class ts_utils(object):
    @staticmethod
    def get_api_data(api_name, token, method = "get", **params):

        base_url = api_url % api_name
        common_parm = api_common_parm % (client_id, token.access_token, token.openid)
        if method.lower() == "get":
            base_url += "?"
            api_param = ""
            for key in params:
                api_param += "&%s=%s" % (key, params[key])
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
        self.statusService = TencentWeiboStatusService(user)
        self.commentsService = TencentWeiboCommentService(user)
        self.favouritesService = TencentWeiboFavoriteService(user)


class TencentWeiboStatusService(IStatusService):
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
        format:     返回数据的格式（json或xml）
        pageflag:   分页标识（0：第一页，1：向下翻页，2：向上翻页
        pagetime:   本页起始时间（第一页：填0，向上翻页：填上一次请求返回的第一条记录时间，向下翻页：填上一次请求返回的最后一条记
                    录时间）
        reqnum:     每次请求记录的条数（1-70条）
        type:       拉取类型（需填写十进制数字） 0x1 原创发表 0x2 转载 如需拉取多个类型请使用|，如(0x1|0x2)得到3,则type=3即可，
                    填零表示拉取所有类型
        contenttype:内容过滤。0-表示所有类型，1-带文本，2-带链接，4-带图片，8-带视频，0x10-带音频 建议不使用contenttype为1的类
                    型，如果要拉取只有文本的微博，建议使用0x80
        """
        api_name = "statuses/home_timeline"
        params["clientip"] = self.user.ip_address

        if not 'format' in params:
            params['format'] = 'json'
        if not 'pageflag' in params:
            params['pageflag'] = '0'
        if not 'pagetime' in params:
            params['pagetime'] = '0'
        if not 'reqnum' in params:
            params['reqnum'] = '25'
        if not 'type' in params:
            params['type'] = '3'
        if not 'contenttype' in params:
            params['contenttype'] = '0'

        ret_data = ts_utils.get_api_data(api_name, self.token, **params)

        ret = ret_data['ret']
        code = ret_data['errcode']
        message = ret_data['msg']
        status_data = []

        #ret=0 即为请求成功
        if ret == 0:
            data = ret_data['data']
            for item in data:
                try:
                    status = data_to_status(item)
                except:
                    continue
                else:
                    status_data.append(status)
        else:
            pass

        return DataResponse(ret,code,message,site="腾讯微博",data=status_data)

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
class TencentWeiboCommentService(ICommentService):
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
class TencentWeiboFavoriteService(IFavoriteService):
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

def data_to_status(item):
    return item
if __name__ == '__main__':
    pass