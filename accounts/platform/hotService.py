"""

    HotService是传说中微辣网最高层的服务类，直接面向UI，超犀利

    add by july:所有接口除了必要参数以外,次要的参数都表现为 **params,只是为了接口看起来简洁一些
    具体有哪些参数最好是写在接口的__doc__里面

"""

from accounts.platform.handlers.sinaHandler import SinaHandler
from accounts.platform.handlers.tencentWeiboHandler import TencentWeiboHandler
from accounts.platform.viewModels import DataResponse,HotData
from accounts.platform.core import data_integration


#todo 所有Service接口都没有去实现排序功能,所以之后要补上

class BaseHotService(object):
    """
    面向UI层的Service基类
    """

    site_handlers = {}

    def __init__(self, user, *site):
        """
        初始化
        """

        self.site_handlers = {}

        if not site:
            site = [oauth.site for oauth in user.token_set.all()]
        for sname in site:
            if sname.lower() == "sina": #新浪微博
                handler = SinaHandler(user)
            elif sname.lower() == 'tw': #腾讯微博
                handler = TencentWeiboHandler(user)
            elif sname.lower() == 'dd': #点点
                continue
                #...
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

        services = {}

        for sname in self.site_handlers:
            #如果site为空,或者sname在site列表里面
            if (not site) or (sname in site):
                services[sname] = self.site_handlers[sname].statusService

        retdata = data_integration(
            services,
            "get_friends_statuses",
            key="created_at",
            data_size=size,
            **params
        )

        return retdata

    def repost_status(self, site, statusid, content, **params):
        """
        转发
        """

        retdata = HotData()

        if not site in self.site_handlers:
            msg = "未绑定%s平台或绑定已过期" % site
            response = DataResponse(ret=1,message=msg,site=site)
            retdata.set_error_flag(response)
        else:
            handler = self.site_handlers[site]
            response = handler.statusService.repost_status(statusid, content, **params)
            if response.ret == 0:
                pass
            else:
                retdata.set_error_flag(response)
        return retdata

    def destory_status(self, site, statusid, **params):
        """
        删除动态
        """

        retdata = HotData()

        if not site in self.site_handlers:
            msg = "未绑定%s平台或绑定已过期" % site
            response = DataResponse(ret=1,message=msg,site=site)
            retdata.set_error_flag(response)
        else:
            handler = self.site_handlers[site]
            response = handler.statusService.destory_status(statusid,**params)
            if response.ret == 0:
                pass
            else:
                retdata.set_error_flag(response)
        return retdata

    def update_status(self, *site, content, **params):
        """
        发表动态
        """

        retdata = HotData()

        for sname in self.site_handlers:
            if sname.lower() in [s.lower() for s in site]:
                response = self.site_handlers[sname].statusService.update_status(content, **params)
                if response.ret == 0:
                    pass
                else:
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
        '''
        获取某条微博的评论
        '''

        retdata = HotData()

        if not site in self.site_handlers:
            msg = "未绑定%s平台或绑定已过期" % site
            response = DataResponse(ret=1,message=msg,site=site)
            retdata.set_error_flag(response)
        else:
            handler = self.site_handlers[site]
            response = handler.commentService.get_comments(statusid,**params)
            if response.ret == 0:
                pass
            else:
                retdata.set_error_flag(response)
        return retdata

    def create_comment(self, site, statusid, content, **params):
        retdata = HotData()

        if not site in self.site_handlers:
            msg = "未绑定%s平台或绑定已过期" % site
            response = DataResponse(ret = 1, message = msg, site = site)
            retdata.set_error_flag(response)
        else:
            handler = self.site_handlers[site]
            response = handler.commentService.create_comment(statusid, content, **params)
            if response.ret == 0:
                pass
            else:
                retdata.set_error_flag(response)
        return retdata

    def destroy_comment(self, site, commentid, **params):
        retdata = HotData()

        if not site in self.site_handlers:
            msg = "未绑定%s平台或绑定已过期" % site
            response = DataResponse(ret = 1, message = msg, site = site)
            retdata.set_error_flag(response)
        else:
            handler = self.site_handlers[site]
            response = handler.commentService.destroy_comment(commentid, **params)
            if response.ret == 0:
                pass
            else:
                retdata.set_error_flag(response)
        return retdata

    def reply_comment(self, site, statusid, commentid, **params):
        retdata = HotData()

        if not site in self.site_handlers:
            msg = "未绑定%s平台或绑定已过期" % site
            response = DataResponse(ret = 1, message = msg, site = site)
            retdata.set_error_flag(response)
        else:
            handler = self.site_handlers[site]
            response = handler.commentService.reply_comment(statusid, commentid, **params)
            if response.ret == 0:
                pass
            else:
                retdata.set_error_flag(response)
        return retdata


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
        if 'size' in params:
            size = params['size']
        else:
            size = 40

        services = {}

        for sname in self.site_handlers:
            #如果site为空,或者sname在site列表里面
            if (not site) or (sname in site):
                services[sname] = self.site_handlers[sname].favoriteService

        retdata = data_integration(
            services,
            "get_favorites",
            key="created_at",
            data_size=size,
            **params
        )

        return retdata

    def get_topics(self, *site, **params):
        """
        获取所有订阅的话题
        """
        if 'size' in params:
            size = params['size']
        else:
            size = 15

        services = {}

        for sname in self.site_handlers:
            #如果site为空,或者sname在site列表里面
            if (not site) or (sname in site):
                services[sname] = self.site_handlers[sname].favoriteService

        retdata = data_integration(
            services,
            "get_topics",
            key="created_at",
            data_size=size,
            **params
        )

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

    def create_favorite(self, site, statusid, **params):
        """
        收藏某条动态
        """
        if not site in self.site_handlers:
            msg = "未绑定%s平台或绑定已过期" % site
            response = DataResponse(ret=1,message=msg)
        else:
            handler = self.site_handlers[site]
            response = handler.favoriteService.create_favorite(statusid,**params)
        return HotData(response)

    def create_topic(self, site, topicid,**params):
        '''
        订阅某个话题
        '''
        pass

    def destroy_favorite(self, site, statusid, **params):
        """
        取消收藏某条动态
        """
        if not site in self.site_handlers:
            msg = "未绑定%s平台或绑定已过期" % site
            response = DataResponse(ret=1,message=msg)
        else:
            handler = self.site_handlers[site]
            response = handler.favoriteService.destroy_favorite(statusid,**params)
        return HotData(response)

    def destroy_topic(self, site, topicid, **params):
        '''
        取消订阅某个话题
        '''
        pass



