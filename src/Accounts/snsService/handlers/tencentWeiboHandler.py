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
from accounts.snsService.viewModels import *
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

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
            for item in data['info']:
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

def data_to_status(data):
    status = Status(data['id'])

    status.site = "腾讯微博"
    status.created_at = datetime.fromtimestamp(data['timestamp'])#微博创建时间
    status.mid = 0                            #微博MID
    status.idstr = ''                        #字符串型的微博ID
    status.text = data['text']                       #微博信息内容
    status.source = data['from']                        #微博来源
    status.source_url = data['fromurl']
    status.favorited = None                #是否已收藏
    status.truncated = False                #是否被截断
    status.in_reply_to_status_id = ''        #回复ID
    status.in_reply_to_user_id = ''        #回复人UID
    status.in_reply_to_screen_name = ''    #回复人昵称
    status.thumbnail_pic = ''                #缩略图地址,没有时不返回此字段

    status.bmiddle_pic = ''                    #中等尺寸图片地址，没有时不返回此字段
    status.original_pic = ''                #原始图片地址，没有时不返回此字段
    status.geo = data['geo']                        #地理信息字段 详细
    status.user = data['name']                        #微博作者的用户信息字段 详细
    status.nick = data['nick']
    status.head_pic = data['head'] + "/50''"
    status.retweeted_status = data['origtext']            #被转发的原微博信息字段，当该微博为转发微博时返回 详细
    status.reposts_count = data['count']                 #转发数
    status.comments_count = data['mcount']               #评论数
    status.attitudes_count = 0                #表态数
    status.mlevel = 0                        #暂未支持
    status.visible = 0                    #微博的可见性及指定可见分组信息。该object中type取值，0：普通微博，1：私密微博，3：指定分组微博，4：密友微博；list_id为分组的组号
    status.pic_urls = data['image']                    #微博配图地址。多图时返回多图链接。无配图返回“[]”
    status.ad = []                            #微博流内的推广微博ID
    if data['self'] == 0:
        status.is_self =True
    return status
if __name__ == '__main__':
    pass