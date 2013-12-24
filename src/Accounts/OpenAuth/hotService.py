"""

    HotService是传说中微辣网最高层的服务类，直接面向UI，超犀利

    add by july:所有接口除了必要参数以外,次要的参数都表现为 **params,只是为了接口看起来简洁一些
    具体有哪些参数最好是写在接口的__doc__里面

"""

from .sns.sinaHandler import SinaHandler
from .sns.tencentWeiboHandler import TencentWeiboHandler

class BaseHotService(object):
    """

    """
    __siteHandlers = {}

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

            self.__siteHandlers[sname] = handler

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

        BaseHotService.__init__(self,user,*site)

    def GetFriendsStatuses(self, *site, **params):
        """
        获取好友的动态信息

        **params:请求参数
        
        """

        statuses = []

        for sname in self.__siteHandlers:
            #如果site为空,或者sname在site列表里面
            if (not site) or (sname in site):
                service = self.__siteHandlers[sname].statusService
                for status in service.GetFriendsStatuses(**params):
                    statuses.append(status)
            else:
                continue

        if not statuses:
            return DataResponse(code = 0, message = "未获取任何动态")
        else:
            return DataResponse(data=statuses)

    def Repost(self, site, statusid, **params):
        """
        转发
        """

        code = 0
        msg = ""

        if not site in self.__siteHandlers:
            msg = "未绑定%s平台或绑定已过期" % site
        else:
            handler = self.__siteHandlers[site]
            try:
                handler.statusService.Repost(statusid)
            except Exception as e:
                msg = str(e)
            else:
                code = 1

        return DataResponse(code=code,message=msg)

    def Destroy(self, site, statusid, **params):
        """
        删除动态
        """

        code = 0
        msg = ""

        if not site in self.__siteHandlers:
            msg = "未绑定%s平台或绑定已过期" % site
        else:
            service = self.__siteHandlers[site]
            try:
                service.StatusService.Destroy(statusid)
            except Exception as e:
                msg = str(e)
            else:
                code = 1

        return DataResponse(code=code,message=msg)

    def Update(self, *site, **params):
        """
        发表动态
        """

        code = 0
        msg = ""
        success_sites = []

        for sname in self.__siteHandlers:
            if sname.lower() in [s.lower() for s in site]:
                service = self.__siteHandlers[sname].StatusService
                try:
                    service.Update(params)
                except Exception as e:
                    msg = str(e)
                else:
                    code = 1
                    success_sites.append(sname)
            else:
                continue

        return DataResponse(code=code,message=msg,data=success_sites)


class CommentService(BaseHotService):
    """
    评论服务
    """

    def __init__(self, user, *site):
        BaseHotService.__init__(self, user, *site)

    def GetComments(self, site, statusid, **params):
        data = []
        service = self.__siteHandlers[site].commentService

        comments = service.GetComments(statusid, **params)
        return DataResponse(data=data)

    def Create(self, site, statusid, content, **params):
        service = self.__siteHandlers[site].commentService
        service.Create(statusid, content, **params)
        return DataResponse()

    def Destory(self, site, commentid, **params):
        service = self.__siteHandlers[site].commentService
        service.Destory(commentid,**params)
        return DataResponse()

    def Reply(self, site, statusid, commentid, **params):
        service = self.__siteHandlers[site].commentService
        service.Reply(statusid, commentid, **params)
        return DataResponse()

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

        favorites = []

        for sname in self.__siteHandlers:
            #如果site为空,或者sname在site列表里面
            if (not site) or (sname in site):
                service = self.__siteHandlers[sname].favoriteService
                for favorite in service.GetFavorites(**params):
                    favorites.append(favorite)
            else:
                continue

        if not favorites:
            return DataResponse(code = 0, message = "未获取任何收藏")
        else:
            return DataResponse(data = favorites)

    def GetFavorite(self, site, favoriteid, **params):
        """
        获取单条收藏
        """

        service = self.__siteHandlers[site].favoriteService
        favorite = service.GetFavorite(favoriteid,**params)

        return DataResponse(data = favorite)

    def Create(self, site, statusid, **params):
        """
        收藏某条动态
        """
        service = self.__siteHandlers[site].favoriteService
        service.Create(statusid, **params)

        return DataResponse()

    def Destory(self, site, statusid, **params):
        """
        取消收藏某条动态
        """
        service = self.__siteHandlers[site].favoriteService
        service.Destory(statusid, **params)

        return DataResponse()


class DataResponse(object):
    """
    请求相应数据包类
    """

    def __init__(self, code = 1, message = "", data = None):
        """
        code:返回1为正常,0为非正常
        message:错误描述
        data:数据
        """
        self.code = code
        self.message = message
        self.data = data

