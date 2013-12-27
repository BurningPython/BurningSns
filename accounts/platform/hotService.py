"""

    HotService是传说中微辣网最高层的服务类，直接面向UI，超犀利

    add by july:所有接口除了必要参数以外,次要的参数都表现为 **params,只是为了接口看起来简洁一些
    具体有哪些参数最好是写在接口的__doc__里面

"""

from accounts.platform.handlers.sinaHandler import SinaHandler
from accounts.platform.handlers.tencentWeiboHandler import TencentWeiboHandler
from accounts.platform.handlers.baseHandler import DataResponse


#todo 所有Service接口都没有去实现排序功能,所以之后要补上

class BaseHotService(object):
    """
    面向UI层的Service基类
    """

    site_handlers = {}

    def __init__(self, user, *site):
        if not site:
            site = [oauth.site for oauth in user.openauth_set.all()]
        for sname in site:
            handler = None

            if sname.lower() == "sina" or sname == "新浪微博":
                handler = SinaHandler(user)
            elif sname == "腾讯微博":
                handler = TencentWeiboHandler(user)
            else:
                continue

            self.site_handlers[sname] = handler


class StatusService(BaseHotService):
    """
    用户动态服务
    """

    def __init__(self, user, *site):
        """
        初始化用户社交网络动态相关服务
        user : 用户实例对象
        *site : 社交网络列表
        """

        BaseHotService.__init__(self, user, *site)

    def get_friends_statuses(self, *site, **params):
        """
        获取好友的动态信息

        params里面要定义好size字段来指定要获取的内容数量,默认为40

        **params:请求参数
        
        """
        if 'size' in params:
            size = params['size']
        else:
            size = 40

        retdata = HotData()
        data_store = {}
        for sname in self.site_handlers:
            #如果site为空,或者sname在site列表里面
            if (not site) or (sname in site):
                service = self.site_handlers[sname].statusService
                response_data = service.get_friends_statuses(**params)
                #获取第一批数据
                if response_data.ret == 0 and len(response_data.data) > 0:
                    data_store[sname] = response_data.data
                #如果第一批数据获取失败,则认为该绑定可能已经失效,之后不再获取
                else:
                    retdata.set_error_flag(response_data)
            else:
                continue

        while len(retdata.data) <= size and data_store:
            to_insert = None
            this_site = ""
            for sname in data_store:
                d = data_store[sname][0]
                if (not to_insert) or (d.created_at > to_insert.created_at):
                    to_insert = d
                    this_site = sname
            retdata.data.append(to_insert)
            ds = data_store[this_site]
            #删除这个已插入的数据
            del ds[0]
            #如果数据已经取完了,则再获取一批数据
            if not ds:
                #向下翻页标识
                params['page_flag'] = 1
                #最后一次插入的数据,各自的接口中可以根据这里的数据来进行分页
                params['last_data'] = to_insert

                service = self.site_handlers[this_site].statusService
                response_data = service.get_friends_statuses(**params)
                if response_data.ret == 0 and len(response_data.data) > 0:
                    data_store[this_site] = response_data.data
                #如果此时获取数据失败,则不再继续尝试获取该平台的数据
                else:
                    del data_store[this_site]


        return retdata

    def repost_status(self, site, statusid, **params):
        """
        转发
        """

        if not site in self.site_handlers:
            msg = "未绑定%s平台或绑定已过期" % site
            response = DataResponse(ret=1,message=msg)
        else:
            handler = self.site_handlers[site]
            response = handler.statusService.repost_status(statusid,**params)
        return HotData(response)

    def destory_status(self, site, statusid, **params):
        """
        删除动态
        """

        if not site in self.site_handlers:
            msg = "未绑定%s平台或绑定已过期" % site
            response = DataResponse(ret=1,message=msg)
        else:
            handler = self.site_handlers[site]
            response = handler.statusService.destory_status(statusid,**params)
        return HotData(response)

    def update_status(self, *site, **params):
        """
        发表动态
        """
        retdata = HotData()
        for sname in self.site_handlers:
            if sname.lower() in [s.lower() for s in site]:
                response = self.site_handlers[sname].StatusService.update_status(**params)
                retdata.set_error_flag(response)
            else:
                continue

        return retdata


class CommentService(BaseHotService):
    """
    评论服务
    """

    def __init__(self, user, *site):
        BaseHotService.__init__(self, user, *site)

    def get_comments(self, site, statusid, **params):
        if not site in self.site_handlers:
            msg = "未绑定%s平台或绑定已过期" % site
            response = DataResponse(ret=1,message=msg)
        else:
            handler = self.site_handlers[site]
            response = handler.commentService.get_comments(statusid,**params)
        return HotData(response)

    def create_comment(self, site, statusid, content, **params):
        if not site in self.site_handlers:
            msg = "未绑定%s平台或绑定已过期" % site
            response = DataResponse(ret=1,message=msg)
        else:
            handler = self.site_handlers[site]
            response = handler.commentService.create_comment(statusid,content,**params)
        return HotData(response)

    def destroy_comment(self, site, commentid, **params):
        if not site in self.site_handlers:
            msg = "未绑定%s平台或绑定已过期" % site
            response = DataResponse(ret=1,message=msg)
        else:
            handler = self.site_handlers[site]
            response = handler.commentService.destroy_comment(commentid,**params)
        return HotData(response)

    def replay_comment(self, site, statusid, commentid, **params):
        if not site in self.site_handlers:
            msg = "未绑定%s平台或绑定已过期" % site
            response = DataResponse(ret=1,message=msg)
        else:
            handler = self.site_handlers[site]
            response = handler.commentService.replay_comment(statusid,commentid,**params)
        return HotData(response)


class FavoriteService(BaseHotService):
    """
    收藏服务
    """

    def __init__(self, user, *site):
        BaseHotService.__init__(self, user, *site)

    def get_favorites(self, *site, **params):
        """
        获取所有收藏
        """
        retdata = HotData()
        for sname in self.site_handlers:
            #如果site为空,或者sname在site列表里面
            if (not site) or (sname in site):
                service = self.site_handlers[sname].favoriteService
                data = service.get_favorites(**params)
                retdata.set_error_flag(data)
            else:
                continue

        return retdata

    def get_favorite(self, site, favoriteid, **params):
        """
        获取单条收藏
        """
        if not site in self.site_handlers:
            msg = "未绑定%s平台或绑定已过期" % site
            response = DataResponse(ret=1,message=msg)
        else:
            handler = self.site_handlers[site]
            response = handler.favoriteService.get_favorite(favoriteid,**params)
        return HotData(response)

    def create_comment(self, site, statusid, **params):
        """
        收藏某条动态
        """
        if not site in self.site_handlers:
            msg = "未绑定%s平台或绑定已过期" % site
            response = DataResponse(ret=1,message=msg)
        else:
            handler = self.site_handlers[site]
            response = handler.favoriteService.create_comment(statusid,**params)
        return HotData(response)

    def destroy_comment(self, site, statusid, **params):
        """
        取消收藏某条动态
        """
        if not site in self.site_handlers:
            msg = "未绑定%s平台或绑定已过期" % site
            response = DataResponse(ret=1,message=msg)
        else:
            handler = self.site_handlers[site]
            response = handler.favoriteService.destroy_comment(statusid,**params)
        return HotData(response)


class HotData(object):
    """
    这是面向UI层的请求相应数据包类
    由于请求有可能面向多个平台,因此每个请求都可能同时存在 失败 和 成功,
    所以把请求失败的错误记录放在一个errors列表中,列表中的每个元素都是
    一个字典,记录错误来源(site),错误码(code)和描述(message),以便对
    用户做出提醒或是其他操作.
    所有成功的请求数据均以统一的模型存放在data列表中
    """

    data = []
    errors = []

    def __init__(self):
        """
        初始化
        """
        self.data = []
        self.errors = []

    def set_error_flag(self, response):
        """
        合并DataResponse
        """
        if not isinstance(response,DataResponse):
            raise Exception("合并类型必须为DataResponse")

        error = {
            'code':response.code,
            'site':response.site,
            'message':response.message
        }
        self.errors.append(error)

        return self


