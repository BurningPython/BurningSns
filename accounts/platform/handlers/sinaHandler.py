'''
    少年，我知道这个传说中的封装真的很垃圾，但是我想了想还是觉得区域自治制度比较好，自己的区域还是归当地政府管，只要能向中央交钱就好了。
'''
__author__ = 'Mr.ELeven'
__email__ = 'iGod_eleven@163.com'
__maketime__ = '2013-12-9'
__AppKey = '2749469053'
__AppSecret = '22a991ef6b614ebc2bcb75555b5a1aec'
__sitename = 'GoodNightEleven'
__sitedomain = 'eleven.org.cn'

import urllib
import urllib.request
import json

from django.core.exceptions import ObjectDoesNotExist

from accounts.platform.handlers.baseHandler import *
from accounts.platform.viewModels import Status,DataResponse


def show_json(j):
    print(json.dumps(j, indent = 4, separators = (',', ':')))

#Sina微博顶层服务
class SinaHandler(BaseHandler):
    Site = 'Sina'                #社交网站名称
    Domain = 'www.weibo.com'

    """Interface Of SNS Module"""
    user = ""                    #HTTP包中的用户

    statusService = ""
    commentsService = ""
    favouritesService = ""
    shortUrlsService = ""

    def __init__(self, user):
        super(BaseHandler, self).__init__()
        self.statusService = StatusService(user)
        self.commentsService = CommentsService(user)
        self.favouritesService = FavouritesService(user)
        self.shortUrlsService = ShortUrlsService(user)

#微博服务
class StatusService(IStatusService):
    #api for get news
    __url_news_getpublicnews = 'https://api.weibo.com/2/statuses/public_timeline.json'
    __url_news_getfriendsnews = 'https://api.weibo.com/2/statuses/friends_timeline.json'
    __url_news_gethomenews = 'https://api.weibo.com/2/statuses/home_timeline.json'
    __url_news_getusernews = 'https://api.weibo.com/2/statuses/user_timeline.json'
    __url_news_getbatchnews = 'https://api.weibo.com/2/statuses/timeline_batch.json'
    __url_news_getmentionnews = 'https://api.weibo.com/2/statuses/mentions.json'
    __url_news_getnewdetail = 'https://api.weibo.com/2/statuses/show.json'
    __url_news_getcount = 'https://api.weibo.com/2/statuses/show.json'
    __url_news_getemotions = 'https://api.weibo.com/2/emotions.json'

    #api for write news
    __url_news_repost = 'https://api.weibo.com/2/statuses/repost.json'
    __url_news_destory = 'https://api.weibo.com/2/statuses/destroy.json'
    __url_news_update = 'https://api.weibo.com/2/statuses/update.json'
    __url_news_upload = 'https://upload.api.weibo.com/2/statuses/upload.json'

    user = ""
    __access_token = ""

    def __init__(self, user):
        self.user = user
        try:
            pass
        except ObjectDoesNotExist:
            pass
        finally:
            self.__access_token = '2.00Fd85eCDVUEAD1aa8ae3efb0_C2bf'

    def get_friends_statuses(self, **parms):            #获取好友动态列表
        if 'last_data' in parms:
            parms['max_id'] = parms['last_data'].mid
            print(parms['last_data'].created_at)
            del parms['last_data']
        parms['count'] = 20
        print(self.__access_token)
        j = self.get_json(self.__url_news_getfriendsnews, parms)
        statuses = []
        for status in j["statuses"]:
            statuses.append(self.toStatus(status))
        return DataResponse(data=statuses)

    def repost_status(self, statusid, **parms):        #转发
        parms['id'] = statusid
        parms['method'] = 'post'
        return self.get_json(self.__url_news_repost, parms)

    def destory_status(self, statusid, **parms):        #删除
        parms['id'] = statusid
        parms['method'] = 'post'
        return self.get_json(self.__url_news_destory, parms)

    def update_status(self, content, **parms):        #发一条说说
        parms['status'] = content
        parms['method'] = 'post'
        return self.get_json(self.__url_news_update, parms)

    def get_json(self, url, parms):            #获取json,私有方法，请忽视
        try:
            method = parms['method']
        except Exception:
            method = 'get'

        if method == 'get':
            querystring = '?access_token=' + self.__access_token
            for k in parms.keys():
                querystring += '&' + k + '=' + str(parms[k])
            try:
                print(url + querystring)
                html = urllib.request.urlopen(url + querystring).read().decode('utf8')
            except:
                print("error current")
                return {}
            return json.loads(html)
        elif method == 'post':
            parms['access_token'] = self.__access_token
            querystring = urllib.parse.urlencode(parms)
            html = urllib.request.urlopen(url, data = bytes(querystring.encode('utf8'))).read().decode('utf8')
            return json.loads(html)
        else:
            pass

    def toStatus(self, j):
        instance = Status()
        for key, value in j.items():
            setattr(instance, key, value)
        import datetime

        instance.created_at = datetime.datetime.strptime(instance.created_at, "%a %b %d %H:%M:%S +0800 %Y")
        return instance

    #序列化
    def object2dict(obj):
        d = {}
        d['__class__'] = obj.__class__.__name__
        d['__module__'] = obj.__module__
        d.update(obj.__dict__)
        return d

    #反序列化
    def dict2object(d, classname):
        module = __import__(Status.__module__, fromlist = (1))
        class_ = getattr(module, classname)
        instance = class_()
        for key, value in d.items():
            setattr(instance, key, value)
        return instance


class CommentsService(ICommentService):    #评论服务
    __url_comments_show = 'https://api.weibo.com/2/comments/show.json'
    __url_comments_by_me = 'https://api.weibo.com/2/comments/by_me.json'
    __url_comments_to_me = 'https://api.weibo.com/2/comments/to_me.json'
    __url_comments_timeline = 'https://api.weibo.com/2/comments/timeline.json'
    __url_comments_mentions = 'https://api.weibo.com/2/comments/mentions.json'
    __url_comments_show_batch = 'https://api.weibo.com/2/comments/show_batch.json'

    __url_comments_create = 'https://api.weibo.com/2/comments/create.json'
    __url_comments_destroy = 'https://api.weibo.com/2/comments/destroy.json'
    __url_comments_destroy_batch = 'https://api.weibo.com/2/comments/destroy_batch.json'
    __url_comments_reply = 'https://api.weibo.com/2/comments/reply.json'

    user = ""
    __access_token = ""

    def __init__(self, user):
        self.user = user
        try:
            pass
        except ObjectDoesNotExist:
            pass
        finally:
            self.__access_token = '2.00Fd85eCDVUEAD1aa8ae3efb0_C2bf'

    def get_comments(self, statusid, **parms):
        parms['id'] = statusid
        return self.get_json(self.__url_comments_show, parms)

    def create_comment(self, statusid, comment, **parms):
        parms['method'] = 'post'
        parms['id'] = statusid
        parms['comment'] = comment
        return self.get_json(self.__url_comments_create, parms)

    def destroy_comment(self, commentid, **parms):
        parms['cid'] = commentid
        parms['method'] = 'post'
        return self.get_json(self.__url_comments_destroy, parms)

    def reply_comment(self, statusid, commentid, comment, **parms):
        parms['method'] = 'post'
        parms['cid'] = commentid
        parms['id'] = statusid
        parms['comment'] = comment
        return self.get_json(self.__url_comments_reply, parms)

    def get_json(self, url, parms = {}):        #获取json,私有方法，请忽视
        try:
            method = parms['method']
        except Exception:
            method = 'get'

        if method == 'get':
            querystring = '?access_token=' + self.__access_token
            for k in parms.keys():
                querystring += '&' + k + '=' + str(parms[k])
            html = urllib.request.urlopen(url + querystring).read().decode('utf8')
            return json.loads(html)
        elif method == 'post':
            parms['access_token'] = self.__access_token
            querystring = urllib.parse.urlencode(parms)
            html = urllib.request.urlopen(url, data = bytes(querystring.encode('utf8'))).read().decode('utf8')
            return json.loads(html)
        else:
            pass


class FavouritesService(IFavoriteService): #收藏服务
    __url_favorites = 'https://api.weibo.com/2/favorites.json'
    __url_favorites_ids = 'https://api.weibo.com/2/favorites/ids.json'
    __url_favorites_show = 'https://api.weibo.com/2/favorites/show.json'
    __url_favorites_by_tags = 'https://api.weibo.com/2/favorites/by_tags.json'
    __url_favorites_tags = 'https://api.weibo.com/2/favorites/tags.json'
    __url_favorites_by_tags_ids = 'https://api.weibo.com/2/favorites/by_tags/ids.json'

    __url_favorites_create = 'https://api.weibo.com/2/favorites/create.json'
    __url_favorites_destroy = 'https://api.weibo.com/2/favorites/destroy.json'
    __url_favorites_destroy_batch = 'https://api.weibo.com/2/favorites/destroy_batch.json'
    __url_favorites_tags_update = 'https://api.weibo.com/2/favorites/tags/update.json'
    __url_favorites_tags_update_batch = 'https://api.weibo.com/2/favorites/tags/update_batch.json'
    __url_favorites_tags_destroy_batch = 'https://api.weibo.com/2/favorites/tags/destroy_batch.json'

    user = ""
    __access_token = ""

    def __init__(self, user):
        self.user = user
        try:
            pass
        except ObjectDoesNotExist:
            pass
        finally:
            self.__access_token = '2.00Fd85eCDVUEAD1aa8ae3efb0_C2bf'

    def get_favorites(self, **parms):        #获取用户的所有
        return self.get_json(self.__url_favorites, parms)

    def get_favorite(self, statusid, **parms):    #获取单条收藏
        parms['id'] = statusid
        return self.get_json(self.__url_favorites_show, parms)

    def create_favorite(self, statusid, **parms):    #添加收藏
        parms['method'] = 'post'
        parms['id'] = statusid
        return self.get_json(self.__url_favorites_create, parms)

    def destroy_favorite(self, statusid, **parms):    #取消收藏
        parms['method'] = 'post'
        parms['id'] = statusid
        return self.get_json(self.__url_favorites_destroy, parms)

    def get_json(self, url, **parms):        #获取json,私有方法，请忽视
        try:
            method = parms['method']
        except Exception:
            method = 'get'

        if method == 'get':
            querystring = '?access_token=' + self.__access_token
            for k in parms.keys():
                querystring += '&' + k + '=' + str(parms[k])
            html = urllib.request.urlopen(url + querystring).read().decode('utf8')
            return json.loads(html)
        elif method == 'post':
            parms['access_token'] = self.__access_token
            querystring = urllib.parse.urlencode(parms)
            html = urllib.request.urlopen(url, data = bytes(querystring.encode('utf8'))).read().decode('utf8')
            return json.loads(html)
        else:
            pass


class ShortUrlsService(IShortUrlService):
    __url_shorturl_shorten = ''        #长链转短链
    __url_shorturl_expand = ''            #短链转长链
    __url_shorturl_share_counts = ''    #获取短连接在微博上的微博分享数
    __url_shorturl_share_statuses = ''    #获取包含指定单个短链接的最新微博内容
    __url_shorturl_comment_counts = ''    #获取短链接在微博上的微博评论数
    __url_shorturl_comment_comments = ''#获取包含指定单个短链接的最新微博评论

    user = ""
    __access_token = ""

    def __init__(self, user):
        self.user = user
        try:
            pass
        except ObjectDoesNotExist:
            pass
        finally:
            self.__access_token = '2.00Fd85eCDVUEAD1aa8ae3efb0_C2bf'

    def Shorten(self, longurl, **parms):
        parms['url_long'] = longurl
        return self.get_json(self.__url_shorturl_shorten, parms)

    def Expand(self, shorturl, **parms):
        parms['url_short'] = shorturl
        return self.get_json(self.__url_shorturl_expand, parms)

    def get_json(self, url, parms = {}):        #获取json,私有方法，请忽视
        try:
            method = parms['method']
        except Exception:
            method = 'get'

        if method == 'get':
            querystring = '?access_token=' + self.__access_token
            for k in parms.keys():
                querystring += '&' + k + '=' + str(parms[k])
            html = urllib.request.urlopen(url + querystring).read().decode('utf8')
            return json.loads(html)
        elif method == 'post':
            parms['access_token'] = self.__access_token
            querystring = urllib.parse.urlencode(parms)
            html = urllib.request.urlopen(url, data = bytes(querystring.encode('utf8'))).read().decode('utf8')
            return json.loads(html)
        else:
            pass
