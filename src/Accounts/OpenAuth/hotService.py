"""
	HotService是传说中微辣网最高层的服务类，直接面向UI，超犀利

    add by july:所有接口除了必要参数以外,次要的参数都表现为 **params,只是为了接口看起来简洁一些
                具体有哪些参数最好是写在接口的__doc__里面
"""

from sns.sinaService import SinaService

#class HotService(object):
#	"""Interface Of SNS Module"""
#	user = ""										#HTTP包中的用户
#	StatusService = ""
#	ICommentsService = ""
#	IFavouritesService = ""
#	RemindService = ""

#	def __init__(self, user):
#		self.StatusService = StatusService(user)
#		self.ICommentsService = ICommentsService(user)
#		self.IFavouritesService = IFavouritesService(user)
#		self.RemindService = RemindService(user)

class StatusService(object):	#微博服务
    """
    社交网络用户动态操作服务
    """

    __siteServices = {}

	def init(self, user, *site):
        """
        初始化用户社交网络动态相关服务
        user : 用户实例对象
        *site : 社交网络列表
        """
        if not site:
            site = [oauth.site for oauth in user.openauth_set.all()]
	    for s in site:
            #匹配到site名称,就创建相应的服务
	    	if s.lower() == 'sina' or s == "新浪微博":
	            service = SinaService(user)
            elif:
	    		pass
            else:
                pass
            #将服务放入字典中
            __siteServices[s] = service

	def GetFriendsStatuses(self, *site, **parms):			
        """
        获取好友的动态信息

        **params:请求参数
        
        """
        statuses = []
        
        
        for sname in self.__siteServices:
            #如果site为空,或者sname在site列表里面
            if (not site) or (sname in site):  
                service = self.__siteServices[sname].StatusService
                for status in service.GetFriendsStatuses(parms):
                statuses.append(status)
            else:
                continue
            

        if not statuses:
            return DataResponse(code = 0,message = "未获取任何动态")
        else:
            return DataResponse(data = statuses)

	def Repost(self, site, statusid, **parms):	
        """
        转发
        """
        if not site in self.__siteServices:
            return DataResponse(code = 0,message = "未绑定该平台(%s)或绑定已过期" % site)

		service.StatusService.Repost(statusid)
        return DataResponse()

	def Destroy(self, site, statusid, **parms):	
		 """
        删除动态
        """
        if not site in self.__siteServices:
            return DataResponse(code = 0,message = "未绑定该平台(%s)或绑定已过期" % site)

		service.StatusService.Destroy(statusid)
        return DataResponse()		

	def Update(self, *site, **params):
        """
        发表动态
        """
        for sname in self.__siteServices:
            if sname.lower() in [_s.lower() for s in site]:
                service = self.__siteServices[sname].StatusService
                service.Update(params)
            else:
                continue

        return DataResponse()


class CommentsService(object):
    """
    评论服务
    """

    def init(self, user, *site, **parms):
        pass

	def GetComments(self, site, statusid, **parms):
		pass

	def Create(self, site, statusid, content, **parms):
		pass

	def Destory(self, site, commentid, **parms):
		pass

	def Reply(self, site, statusid, commentid, **parms):
		pass


class FavouritesService(object):			
    """
    收藏服务
    """

    def init(self,user,*site, **parms):
        pass

	def GetFavorites(self, *site, **parms):
        """
        获取所有收藏
        """
		pass

	def GetFavorite(self, site, favoriteid, **parms):
        """
        获取单条收藏
        """
		pass

	def Create(self, site, statusid, **parms):
        """
        收藏某条动态
        """
		pass

    def Destory(self, site, statusid, **parms):
        """
        取消收藏某条动态
        """
		pass


class DataResponse(object):
    """
    请求相应数据包类
    """
    def init(self,code = 1,message = "",data = None):
        self.code = code
        self.message = message
        self.data = data

