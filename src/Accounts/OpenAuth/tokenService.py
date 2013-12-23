'''
用来处理用户关联的Token信息,比如添加第三方绑定/刷新某平台token信息,
初始化时传入特定用户的实例,所有操作只针对该用户

Created on 2013年12月22日

@author: july
'''

from Accounts.models import OpenAuth,MyUser

class TokenService(object):
    
    def __init__(self,user):
        """
        根据用户实例对象来初始化
        """
        pass

    def addToken(self,site,**args):
        """
        添加Token,即绑定一个AccessToken,如果该site已经被绑定,
        则更新accesstoken信息
        """
        pass
    
    def setTokenEnable(self,site,enable = True):
        """
        设置对应site的accessToken是否有效,
        传入enable默认为True,即为有效
        """
        pass
    
    def deleteToken(self,site):
        """
        删除一个accessToken,直接从数据库中删除
        """
        pass

    def deleteTokens(self,*site):
        """
        批量删除accessToken
        """
        pass

    def refreshToken(self,site):
        """
        通过refreshToken,刷新一个accessToken,因为accessToken是会过期的.
        refreshToken在OpenAuthModel里面有
        """
        pass
   
    def refreshTokens(self,*site):
        """
        批量刷新refreshToken
        """
        pass

    def getTokens(self):
        """
        获取该用户的所有token信息的列表
        """
        pass
    
if __name__ == '__main__':
    pass
