"""

    HotService是传说中微辣网最高层的服务类，直接面向UI，超犀利

    add by july:所有接口除了必要参数以外,次要的参数都表现为 **params,只是为了接口看起来简洁一些
    具体有哪些参数最好是写在接口的__doc__里面

"""

from accounts.snsService.handlers.sinaHandler import SinaHandler
from accounts.snsService.handlers.tencentWeiboHandler import TencentWeiboHandler
from accounts.snsService.handlers.baseHandler import DataResponse


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

    def GetFriendsStatuses(self, *site, **params):
        """
        获取好友的动态信息

        **params:请求参数
        
        """
        retdata = HotData()
        for sname in self.site_handlers:
            #如果site为空,或者sname在site列表里面
            if (not site) or (sname in site):
                service = self.site_handlers[sname].statusService
                data = service.GetFriendsStatuses(**params)
                retdata.append(data)
            else:
                continue

        retdata.data.sort(key=lambda status : status.created_at,reverse=True)
        return retdata

    def Repost(self, site, statusid, **params):
        """
        转发
        """

        if not site in self.site_handlers:
            msg = "未绑定%s平台或绑定已过期" % site
            response = DataResponse(ret=1,message=msg)
        else:
            handler = self.site_handlers[site]
            response = handler.statusService.Repost(statusid,**params)
        return HotData(response)

    def Destroy(self, site, statusid, **params):
        """
        删除动态
        """

        if not site in self.site_handlers:
            msg = "未绑定%s平台或绑定已过期" % site
            response = DataResponse(ret=1,message=msg)
        else:
            handler = self.site_handlers[site]
            response = handler.statusService.Destroy(statusid,**params)
        return HotData(response)

    def Update(self, *site, **params):
        """
        发表动态
        """
        retdata = HotData()
        for sname in self.site_handlers:
            if sname.lower() in [s.lower() for s in site]:
                response = self.site_handlers[sname].StatusService.Update(**params)
                retdata.append(response)
            else:
                continue

        return retdata


class CommentService(BaseHotService):
    """
    评论服务
    """

    def __init__(self, user, *site):
        BaseHotService.__init__(self, user, *site)

    def GetComments(self, site, statusid, **params):
        if not site in self.site_handlers:
            msg = "未绑定%s平台或绑定已过期" % site
            response = DataResponse(ret=1,message=msg)
        else:
            handler = self.site_handlers[site]
            response = handler.commentService.GetComments(statusid,**params)
        return HotData(response)

    def Create(self, site, statusid, content, **params):
        if not site in self.site_handlers:
            msg = "未绑定%s平台或绑定已过期" % site
            response = DataResponse(ret=1,message=msg)
        else:
            handler = self.site_handlers[site]
            response = handler.commentService.Create(statusid,content,**params)
        return HotData(response)

    def Destory(self, site, commentid, **params):
        if not site in self.site_handlers:
            msg = "未绑定%s平台或绑定已过期" % site
            response = DataResponse(ret=1,message=msg)
        else:
            handler = self.site_handlers[site]
            response = handler.commentService.Destory(commentid,**params)
        return HotData(response)

    def Reply(self, site, statusid, commentid, **params):
        if not site in self.site_handlers:
            msg = "未绑定%s平台或绑定已过期" % site
            response = DataResponse(ret=1,message=msg)
        else:
            handler = self.site_handlers[site]
            response = handler.commentService.Reply(statusid,commentid,**params)
        return HotData(response)


class FavoriteService(BaseHotService):
    """
    收藏服务
    """

    def __init__(self, user, *site):
        BaseHotService.__init__(self, user, *site)

    def GetFavorites(self, *site, **params):
        """
        获取所有收藏
        """
        retdata = HotData()
        for sname in self.site_handlers:
            #如果site为空,或者sname在site列表里面
            if (not site) or (sname in site):
                service = self.site_handlers[sname].favoriteService
                data = service.GetFavorites(**params)
                retdata.append(data)
            else:
                continue

        return retdata

    def GetFavorite(self, site, favoriteid, **params):
        """
        获取单条收藏
        """
        if not site in self.site_handlers:
            msg = "未绑定%s平台或绑定已过期" % site
            response = DataResponse(ret=1,message=msg)
        else:
            handler = self.site_handlers[site]
            response = handler.favoriteService.GetFavorite(favoriteid,**params)
        return HotData(response)

    def Create(self, site, statusid, **params):
        """
        收藏某条动态
        """
        if not site in self.site_handlers:
            msg = "未绑定%s平台或绑定已过期" % site
            response = DataResponse(ret=1,message=msg)
        else:
            handler = self.site_handlers[site]
            response = handler.favoriteService.Create(statusid,**params)
        return HotData(response)

    def Destory(self, site, statusid, **params):
        """
        取消收藏某条动态
        """
        if not site in self.site_handlers:
            msg = "未绑定%s平台或绑定已过期" % site
            response = DataResponse(ret=1,message=msg)
        else:
            handler = self.site_handlers[site]
            response = handler.favoriteService.Destory(statusid,**params)
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

    def __init__(self,response = None):
        """
        初始化
        """
        if response:
            self.append(response)

    def append(self,response):
        """
        合并DataResponse
        """
        if not isinstance(response,DataResponse):
            raise Exception("合并类型必须为DataResponse")

        if response.ret == 0:
            for _data in response.data:
                self.data.append(_data)
        else:
            error = {
                'code':response.code,
                'site':response.site,
                'message':response.message
            }
            self.errors.append(error)

        return self


