'''

用来处理用户关联的Token信息,比如添加第三方绑定/刷新某平台token信息,
初始化时传入特定用户的实例,所有操作只针对该用户

Created on 2013年12月22日

@author: july

'''

from django.core.exceptions import ObjectDoesNotExist

from accounts.models import OpenAuth, User


class TokenService(object):
    def __init__(self, user):
        """
        根据用户实例对象来初始化
        """

        self.user = user

        pass

    def addToken(self, site, **args):
        """
        添加Token,即绑定一个AccessToken,如果该site已经被绑定,
        则更新accesstoken信息
        """

        #这2个参数必须有
        if ('access_token' in args) and ('expires_in' in args):
            access_token = args['access_token']
            expires_in = args['expires_in']
        else:
            raise Exception("没有给定access_token和expires_in参数")
        #以下参数可能不一定有
        if 'refresh_token' in args:
            refresh_token = args['refresh_token']
        else:
            refresh_token = ""
        if 'openid' in args:
            openid = args['openid']
        else:
            openid = ""

        oauth = self.isUserBindedSite(site=site)
        #如果已经存在该openAuth,则更新
        if oauth:
            oauth.site = site
            oauth.access_token = access_token
            oauth.refresh_token = refresh_token
            oauth.expires_in = expires_in
            oauth.openid = openid
            oauth.save()
        #如果不存在这个openAuth,则继续
        else:
            user = self.user
            user.openauth_set.create(
                site=site,
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=expires_in,
                openid=openid,
            )
            user.save()

    def setTokenEnable(self, site, enable=True):
        """
        设置对应site的accessToken是否有效,
        传入enable默认为True,即为有效
        """

        #TODO

        pass

    def deleteToken(self, site):
        """
        删除一个accessToken,直接从数据库中删除
        """

        #TODO

        pass

    def deleteTokens(self, *site):
        """
        批量删除accessToken
        """

        #TODO

        pass

    def refreshToken(self, site):
        """
        通过refreshToken,刷新一个accessToken,因为accessToken是会过期的.
        refreshToken在OpenAuthModel里面有
        """

        #TODO

        pass

    def refreshTokens(self, *site):
        """
        批量刷新refreshToken
        """

        #TODO

        pass

    def getTokens(self):
        """
        获取该用户的所有token信息的列表
        """

        #TODO

        pass

    def isUserBindedSite(self, site, username=None):
        """
        检查用户是否已经绑定到指的社交平台
        如果是,返回openauth对象,否则返回None
        """

        if username:
            try:
                user = User.objects.get(username)
            except ObjectDoesNotExist:
                raise Exception("用户名为%s的账户不存在" % username)
        else:
            user = self.user
        try:
            oauth = OpenAuth.objects.get(user=user, site=site)
        except ObjectDoesNotExist:
            return None
        else:
            return oauth


if __name__ == '__main__':
    pass