"""
	各位程序猿注意啦，老板说这个类是所有社交网站的接口类，也就是说你们写的各家社交网站模块要实现这些接口。
	只是个纸老虎，其实这个文件是没有用的。
"""
#模块顶层服务
class SNSService(object):
	Site = ''					#社交网站名称
	Domain = 'www.weibo.com' 	#域名

	StatusesService = ""
	CommentsService = ""
	FavouritesService = ""
	ShortUrlsService = ""

	def __init__(self, user):
		self.StatusesService = IStatusesService(user)
		self.CommentsService = ICommentsService(user)
		self.FavouritesService = IFavouritesService(user)
		self.ShortUrlsService = IShortUrlsService(user)
		
#微博服务
class IStatusesService(object):
	def GetFriendsStatuses(self, **parms):			#获取好友动态列表
		pass

	def Repost(self, statusid, **parms):		#转发：微博ID
		pass
	
	def Destroy(self, statusid, **parms):		#删除：微博ID
		pass
	
	def Update(self, content, **parms):		#发微博：微博内容
		pass

#评论服务
class ICommentsService(object):	
	def GetComments(self, statusid, **parms):		#获取指定ID的微博的所有评论
		pass

	def Create(self, statusid, comment, **parms):	#新建一条评论:微博ID，评论内容
		pass

	def Destory(self, commentid, **parms):			#删除一条评论：评论ID
		pass

	def Reply(self, statusid, commentid, comment,**parms):	#回复一条评论，微博ID，评论ID，回复内容
		pass

#收藏服务
class IFavouritesService(object): 
	def GetFavorites(self, **parms):				#获取所有收藏
		pass

	def GetFavorite(self, statusid, **parms):		#获取单条收藏：微博ID
		pass

	def Create(self, statusid, **parms):			#添加收藏：微博ID
		pass

	def Destory(self, statusid, **parms):			#取消收藏：微博ID
		pass

#长短链转化
class IShortUrlsService(object):	
	def Shorten(self, longurl, **parms):			#长链转短链：长链接
		pass

	def Expand(self, shorturl, **parms):			#短链转长链：短链接
		pass