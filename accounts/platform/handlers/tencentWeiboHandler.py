'''
Created on 2013年12月18日

@author: july

description:接口说明文档中,参数名前带星号(*)的表示必要参数,不带的表示可选参数
'''

#腾讯微博相关
client_id = "801453781"
client_secret = "c2ee75038d707a610c7a4a10c0377c2e"
api_url = "https://open.t.qq.com/api/%s"
api_common_parm = "oauth_consumer_key=%s&access_token=%s&openid=%s&oauth_version=2.a&scope=all"

import json
from urllib.request import urlopen
from urllib.parse import urlencode
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist

from accounts.platform.viewModels import *
from accounts.platform.handlers.baseHandler import *


class ts_utils(object):
    @staticmethod
    def get_api_data(api_name, token, method = "get", **params):
        """
        返回api的数据
        api_name:api名称
        token:用户access_token
        method:请求方式  get或post
        params:参数
        """

        base_url = api_url % api_name
        common_parm = api_common_parm % (client_id, token.access_token, token.openid)
        if method.lower() == "get":
            base_url += "?"
            api_param = ""
            for key in params:
                api_param += "&%s=%s" % (key, params[key])
            target_url = base_url + common_parm + api_param
            print(target_url)
            ret = urlopen(target_url).read().decode("utf-8")
        else:
            querystring = common_parm + "&" + urlencode(params)
            ret = urlopen(base_url, data = bytes(querystring.encode('utf8'))).read().decode('utf8')
        return json.loads(ret)


class TencentWeiboHandler(BaseHandler):
    """
    腾讯微博handler
    """

    def __init__(self, user):
        """
        初始化腾讯微博handler
        """
        super(BaseHandler, self).__init__()

        try:
            token = user.token_set.get(site = "tw")
        except ObjectDoesNotExist:
            raise Exception("用户'%s'未绑定'腾讯微博'平台" % user.username)

        self.statusService = TencentWeiboStatusService(user, token)
        self.commentsService = TencentWeiboCommentService(user, token)
        self.favouritesService = TencentWeiboFavoriteService(user, token)

        print("%sinitial succeed" % self.__class__)


class TencentWeiboStatusService(IStatusService):
    """
    用户动态相关服务
    """

    def __init__(self, user, token):
        """
        初始化
        """
        super(IStatusService, self).__init__()
        self.user = user
        self.token = token


    def get_friends_statuses(self, **params):
        """
        获取好友动态列表
        *format:     返回数据的格式（json或xml）
        *pageflag:   分页标识（0：第一页，1：向下翻页，2：向上翻页
        *pagetime:   本页起始时间（第一页：填0，向上翻页：填上一次请求返回的第一条记录时间，向下翻页：填上一次请求返回的最后一条记
                    录时间）
        *reqnum:     每次请求记录的条数（1-70条）
        *type:       拉取类型（需填写十进制数字） 0x1 原创发表 0x2 转载 如需拉取多个类型请使用|，如(0x1|0x2)得到3,则type=3即可，
                    填零表示拉取所有类型
        *contenttype:内容过滤。0-表示所有类型，1-带文本，2-带链接，4-带图片，8-带视频，0x10-带音频 建议不使用contenttype为1的类
                    型，如果要拉取只有文本的微博，建议使用0x80
        """
        _params = {
            'clientip':self.user.ip_address,
            'format':'json',
            'pageflag':'0',
            'pagetime':'0',
            'reqnum':'20',
            'type':'3',
            'contenttype':'0'
        }

        api_name = "statuses/home_timeline"

        #翻页标识 0 首页  1 下一页  2 上一页
        if 'page_flag' in params:
            _params['pageflag'] = params['page_flag']
        if 'last_data' in params:
            _params['pagetime'] = params['last_data'].created_at.timestamp()
        if 'size' in params:
            _params['reqnum'] = params['size']

        #下面时可选参数
        if 'tx_format' in params:
            _params['format'] = params['tx_format']
        if 'tx_pageflag' in params:
            _params['pageflag'] = params['tx_pageflag']
        if 'tx_pagetime' in params:
            _params['pagetime'] = params['tx_pagetime']
        if 'tx_reqnum' in params:
            _params['reqnum'] = params['tx_reqnum']
        if 'tx_type' in params:
            _params['type'] = params['tx_type']
        if 'tx_contenttype' in params:
            _params['contenttype'] = params['tx_contenttype']

        ret_data = ts_utils.get_api_data(api_name, self.token, **_params)

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

        return DataResponse(ret,code,message,site="tw",data=status_data)

    def repost_status(self, statusid, content, **params):
        """
        转发微博
        *format	 	 返回数据的格式（json或xml）
        *content	 微博内容（若在此处@好友，需正确填写好友的微博账号，而非昵称），不超过140字
                     注意：若转播的是源消息，则content中不需要带源消息的内容，即不要写成xxx||@yy:zzz的形式，只需要直接输入转播内容即可！
        *reid	  	 转播父节点微博id
        *clientip	 用户ip（必须正确填写用户侧真实ip，不能为内网ip及以127或255开头的ip，以分析用户所在地）

        longitude	 经度，为实数，如113.421234（最多支持10位有效数字，可以填空）
        latitude	 纬度，为实数，如22.354231（最多支持10位有效数字，可以填空）
        compatibleflag	 容错标志，支持按位操作，默认为0。
                         0x20-微博内容长度超过140字则报错
                         0-以上错误做容错处理，即发表普通微博
        """

        api_name = "t/re_add"

        _params = {
            'format':'json',
            'content':content,
            'reid':statusid,
            "clientip":self.user.ip_address
        }

        if 'longitude' in params:
            _params['longitude'] = params['longitude']
        if 'latitude' in params:
            _params['latitude'] = params['latitude']
        if 'compatibleflag' in params:
            _params['compatibleflag'] = params['compatibleflag']

        ret_data = ts_utils.get_api_data(api_name, self.token, method = "post", **_params)

        return make_response_data(ret_data)

    def destory_status(self, statusid, **params):
        """
        删除微博

        *format	  返回数据的格式（json或xml）
        *id	  	  微博id
        """

        api_name = "t/del"

        _params = {"format": 'json', 'id': statusid}

        ret_data = ts_utils.get_api_data(api_name, self.token, method = "post", **_params)

        return make_response_data(ret_data)

    def update_status(self, content, **params):
        """
        发微博：微博内容

        *format	  	        返回数据的格式（json或xml）
        *content	  	    微博内容（若在此处@好友，需正确填写好友的微博账号，而非昵称），不超过140字
        *clientip	  	    用户ip（必须正确填写用户侧真实ip，不能为内网ip及以127或255开头的ip，以分析用户所在地）

        longitude	  	    经度，为实数，如113.421234（最多支持10位有效数字，可以填空）
        latitude	  	    纬度，为实数，如22.354231（最多支持10位有效数字，可以填空）
        compatibleflag	 	容错标志，支持按位操作，默认为0。
                            0x20-微博内容长度超过140字则报错
                            0-以上错误做容错处理，即发表普通微博
        """

        api_name = "t/add"
        _params = {
            'clientip':self.user.ip_address,
            'format':'json',
            'content':content,
        }

        if 'longitude' in params:
            _params['longitude'] = params['longitude']
        if 'latitude' in params:
            _params['latitude'] = params['latitude']
        if 'compatibleflag' in params:
            _params['compatibleflag'] = params['compatibleflag']

        ret_data = ts_utils.get_api_data(api_name, self.token, method = "post", **_params)
        return make_response_data(ret_data)


class TencentWeiboCommentService(ICommentService):
    """
    评论服务
    """

    def __init__(self, user, token):
        """
        初始化
        """

        super(ICommentService, self).__init__()
        self.user = user
        self.token = token

        pass

    def get_comments(self, statusid, **parms):
        """
        获取动态的评论列表
        *format	  	 返回数据的格式（json或xml）
        *flag	  	 类型标识。0－转播列表，1－点评列表，2－点评与转播列表
        *rootid	  	 转发或回复的微博根结点id（源微博id）
        *pageflag	 分页标识，用于翻页（0：第一页，1：向下翻页，2：向上翻页）
        *pagetime	 本页起始时间，与pageflag、twitterid共同使用，实现翻页功能（第一页：填0，向上翻页：填上一次请求返回的第一条记录时间，向下翻页：填上一次请求返回的最后一条记录时间）
        *reqnum	  	 每次请求记录的条数（1-100条）,默认为20条
        *twitterid	 微博id，与pageflag、pagetime共同使用，实现翻页功能（第1页填0，继续向下翻页，填上一次请求返回的最后一条记录id）
        """

        api_name = 't/re_list'

        _params={
            'format':'json',
            'flag':'1',
            'rootid':statusid,
            'pageflag':'0',
            'pagetime':'0',
            'reqnum':'20',
            'twitterid':'0',
        }

        if 'page_flag' in parms:
            _params['pageflag'] = parms['page_flag']
        if 'last_data' in parms:
            last_data = parms['last_data']
            _params['twitterid'] = last_data.id
            _params['pagetime'] = last_data.created_at.timestamp()
        if 'size' in parms:
            _params['reqnum'] = parms['size']

        ret_data = ts_utils.get_api_data(api_name, self.token, **_params)

        ret = ret_data['ret']
        code = ret_data['errcode']
        message = ret_data['msg']
        status_data = []

        #ret=0 即为请求成功
        if ret == 0:
            data = ret_data['data']
            for item in data['info']:
                try:
                    status = data_to_comment(item)
                except:
                    continue
                else:
                    status_data.append(status)
        else:
            pass

        return DataResponse(ret,code,message,site="腾讯微博",data=status_data)

    def create_comment(self, statusid, content, **parms):
        """
        创建评论

        *format	  	     返回数据的格式（json或xml）
        *content	  	 微博内容（若在此处@好友，需正确填写好友的微博账号，而非昵称），不超过140字
        *clientip	  	 用户ip（必须正确填写用户侧真实ip，不能为内网ip及以127或255开头的ip，以分析用户所在地）
        *reid	  	     点评父节点微博id
        longitude	  	 经度，为实数，如113.421234（最多支持10位有效数字，可以填空）
        latitude	  	 纬度，为实数，如22.354231（最多支持10位有效数字，可以填空）
        compatibleflag	 容错标志，支持按位操作，默认为0。
                         0x20-微博内容长度超过140字则报错
                         0-以上错误做容错处理，即发表普通微博
        """

        api_name = 't/comment'
        _params = {
            'format':'json',
            'content':content,
            'clientip':self.user.ip_address,
            'reid':statusid,
        }

        if 'longitude' in parms:
            _params['longitude'] = parms['longitude']
        if 'latitude' in parms:
            _params['latitude'] = parms['latitude']
        if 'compatibleflag' in parms:
            _params['compatibleflag'] = parms['compatibleflag']

        ret_data = ts_utils.get_api_data(api_name, self.token, method = "post", **_params)
        return make_response_data(ret_data)

    def destroy_comment(self, commentid, **parms):
        """
        删除评论
        """

        return DataResponse(ret=1,message="腾讯微博暂不支持删除评论功能")

    def reply_comment(self, statusid, commentid, content, **parms):
        """
        回复评论

        *format	  	 返回数据的格式（json或xml）
        *content	 微博内容（若在此处@好友，需正确填写好友的微博账号，而非昵称），不超过140字
        *clientip	 用户ip（必须正确填写用户侧真实ip，不能为内网ip及以127或255开头的ip，以分析用户所在地）
        *reid	  	 回复的父节点微博id
        longitude	 经度，为实数，如113.421234（最多支持10位有效数字，可以填空）
        latitude	 纬度，为实数，如22.354231（最多支持10位有效数字，可以填空）
        compatibleflag	 容错标志，支持按位操作，默认为0。
                         0x20-微博内容长度超过140字则报错
                         0-以上错误做容错处理，即发表普通微博
        """

        api_name = 't/reply'

        _params={
            'format':'json',
            'content':content,
            'clientip':self.user.ip_address,
            'reid':commentid,
        }

        if 'longitude' in parms:
            _params['longitude'] = parms['longitude']
        if 'latitude' in parms:
            _params['latitude'] = parms['latitude']
        if 'compatibleflag' in parms:
            _params['compatibleflag'] = parms['compatibleflag']

        ret_data = ts_utils.get_api_data(api_name, self.token, method = "post", **_params)
        return make_response_data(ret_data)

#收藏服务
class TencentWeiboFavoriteService(IFavoriteService):
    """
    收藏服务
    """

    def __init__(self, user, token):
        super(IFavoriteService, self).__init__()

        self.user = user
        self.token = token
        pass

    def get_favorites(self, **params):
        """
        获取所有收藏列表

        *format	 	 返回数据的格式（json或xml）
        *pageflag	 是	 分页标识（0：第一页，1：向下翻页，2：向上翻页）
        *pagetime	 是	 翻页用，第一页时：填0；向上翻页：填上一次请求返回的第一条记录时间；向下翻页：填上一次请求返回的最后一条记录时间
        *reqnum	 	 每次请求记录的条数（1-100条）
        *lastid	 	 翻页用，第一页时：填0；继续向上翻页：填上一次请求返回的第一条记录id；继续向下翻页：填上一次请求返回的最后一条记录id
        """

        api_name = 'fav/list_t'

        _params = {
            'format':'json',
            'pageflag':'0',
            'pagetime':'0',
            'reqnum':'20',
            'lastid':'0',
        }

        #翻页标识 0 首页  1 下一页  2 上一页
        if 'page_flag' in params:
            _params['pageflag'] = params['page_flag']
        if 'last_data' in params:
            last_data = params['last_data']
            _params['pagetime'] = last_data.created_at.timestamp()
            _params['lastid'] = last_data.id
        if 'size' in params:
            _params['reqnum'] = params['size']

        #下面时可选参数
        if 'tx_format' in params:
            _params['format'] = params['tx_format']
        if 'tx_pageflag' in params:
            _params['pageflag'] = params['tx_pageflag']
        if 'tx_pagetime' in params:
            _params['pagetime'] = params['tx_pagetime']
        if 'tx_reqnum' in params:
            _params['reqnum'] = params['tx_reqnum']
        if 'tx_lastid' in params:
            _params['lastid'] = params['tx_lastid']

        ret_data = ts_utils.get_api_data(api_name, self.token, **_params)

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

        return DataResponse(ret,code,message,site="tw",data=status_data)

    def get_topics(self, **params):
        """
        获取订阅的话题列表

        *format	 	 返回数据的格式（json或xml）
        *reqnum	 	 请求数（最多15）
        *pageflag	 翻页标识（0：首页 1：向下翻页 2：向上翻页）
        *pagetime	 翻页用，第一页时：填0；向上翻页：填上一次请求返回的第一条记录时间；向下翻页：填上一次请求返回的最后一条记录时间
        *lastid	 	 翻页用，第一页时：填0；继续向上翻页：填上一次请求返回的第一条记录id；继续向下翻页：填上一次请求返回的最后一条记录id
        """

        api_name = 'fav/list_ht'

        _params = {
            'format':'json',
            'pageflag':'0',
            'pagetime':'0',
            'reqnum':'15',
            'lastid':'0',
        }

        #翻页标识 0 首页  1 下一页  2 上一页
        if 'page_flag' in params:
            _params['pageflag'] = params['page_flag']
        if 'last_data' in params:
            last_data = params['last_data']
            _params['pagetime'] = last_data.created_at.timestamp()
            _params['lastid'] = last_data.id
        if 'size' in params:
            _params['reqnum'] = params['size']

        #下面时可选参数
        if 'tx_format' in params:
            _params['format'] = params['tx_format']
        if 'tx_pageflag' in params:
            _params['pageflag'] = params['tx_pageflag']
        if 'tx_pagetime' in params:
            _params['pagetime'] = params['tx_pagetime']
        if 'tx_reqnum' in params:
            _params['reqnum'] = params['tx_reqnum']
        if 'tx_lastid' in params:
            _params['lastid'] = params['tx_lastid']

        ret_data = ts_utils.get_api_data(api_name, self.token, **_params)

        ret = ret_data['ret']
        code = ret_data['errcode']
        message = ret_data['msg']
        status_data = []

        #ret=0 即为请求成功
        if ret == 0:
            data = ret_data['data']
            for item in data['info']:
                try:
                    topic = data_to_topic(item)
                except:
                    continue
                else:
                    status_data.append(topic)
        else:
            pass

        return DataResponse(ret,code,message,site="tw",data=status_data)

    def get_favorite(self, statusid, **parms):
        raise Exception("接口(%s)未实现" % self.__name__)

    def create_favorite(self, statusid, **parms):            #添加收藏：微博ID
        """
        收藏一条微博

        *format	 返回数据的格式（json或xml）
        *id	 	 需要收藏的微博id
        """

        api_name = 'fav/addt'

        _params={
            'format':'json',
            'id':statusid,
        }

        ret_data = ts_utils.get_api_data(api_name, self.token, method = "post", **_params)
        return make_response_data(ret_data)

    def create_topic(self, topicid, **parms):            #添加收藏：微博ID
        """
        订阅一个话题

        *format	 返回数据的格式（json或xml）
        *id	 	 话题id
        """

        api_name = 'fav/addht'

        _params={
            'format':'json',
            'id':topicid,
        }

        ret_data = ts_utils.get_api_data(api_name, self.token, method = "post", **_params)
        return make_response_data(ret_data)

    def destroy_favorite(self, statusid, **parms):            #取消收藏：微博ID
        """
        取消收藏一条微博

        *format	 返回数据的格式（json或xml）
        *id	 	 需要收藏的微博id
        """

        api_name = 'fav/delt'

        _params={
            'format':'json',
            'id':statusid,
        }

        ret_data = ts_utils.get_api_data(api_name, self.token, method = "post", **_params)
        return make_response_data(ret_data)

    def destroy_topic(self, topicid, **parms):            #取消收藏：微博ID
        """
        取消订阅一个话题

        *format	 返回数据的格式（json或xml）
        *id	 	 话题的id
        """

        api_name = 'fav/delht'

        _params={
            'format':'json',
            'id':topicid,
        }

        ret_data = ts_utils.get_api_data(api_name, self.token, method = "post", **_params)
        return make_response_data(ret_data)

###################以下是模型转换###################

def data_to_status(data):
    status = Status()
    status.id = data['id']
    status.site = "tw"
    status.site_name = "腾讯微博"
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
    status.uid = data['openid']
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

def data_to_comment(data):

    comment = Comment()
    comment.site = 'tw'
    comment.site_name = '腾讯微博'
    comment.id = data['id']
    comment.created_at = datetime.fromtimestamp(data['timestamp'])

    comment.text = data['text']            #评论的内容
    comment.source = data['from']            #评论的来源
    comment.source_url = data['fromurl']
    comment.user = data['name']            #评论作者的用户信息字段 详细
    comment.uid = data['openid']
    comment.nick = data['nick']
    comment.mid = data['openid']            #评论的MID
    comment.idstr = data['openid']            #字符串型的评论ID
    comment.status = data['source ']            #评论的微博信息字段 详细
    comment.reply_comment = data['origtext']    #评论来源评论，当本评论属于对另一评论的回复时返回此字段
    return comment

def data_to_topic(data):
    topic = Topic()
    topic.id = data['id']
    topic.site = "tw"
    topic.site_name = "腾讯微博"
    topic.created_at = datetime.fromtimestamp(data['timestamp'])#微博创建时间

    topic.favorite_num = data['favnum']
    topic.status_num = data['tweetnum']
    topic.title = data['text']

    return topic

def make_response_data(data):
    """
    将返回的数据包装成DataResponse再返回
    """
    ret = DataResponse(data.ret,data.errcode,data.msg,site="tw")

    if data.ret == 0:
        ret.data = data.data

    return ret
if __name__ == '__main__':
    pass