'''
Created on 2013年12月18日

@author: july
'''
from Accounts.OpenAuth import utils
from Accounts.OpenAuth import config

class ActionHandler(object):
    '''
    用来调用API的类
    '''
    
    def __init__(self, access_token, openid, request):
        '''
        初始化
        '''
        ip = utils.getClientIp(request)
        self.client_id = config.tw_client_id
        self.oauth_version = config.tw_oauth_version
        
        self.api_url = config.tw_api_url
        self.common_parm = config.tw_api_common_parm % (
            self.client_id,
            access_token,
            openid,
            ip,
            self.oauth_version,
            "all",
        )
    
    def make_api_url(self,api_name,api_param):
        target_url = (self.api_url % api_name) +self.common_parm + api_param
        return target_url
    
    def home_timeline(self,pageflag = 0,pagetime = 0,reqnum = 25,type = 0,contenttype = 0):
        """
        主页时间线
        """
        #api的名称
        api_name = "statuses/home_timeline"
        #参数列表
        api_param_list = "format=%s&pageflag=%s&pagetime=%s&reqnum=%s&type=%s&contenttype=%s"
        #拼接参数列表字符串
        api_param_str = api_param_list % (
            "json",
            pageflag,
            pagetime,
            reqnum,
            type,
            contenttype,
        )
        #完整url
        target_url = self.make_api_url(api_name,api_param_str)
        #读取接口数据
        ret = utils.urlRead(target_url)
        #将数据转换成字典返回
        return utils.jsonToParamDic(ret) 
    
     
class TokenManager(object):
    """
    用来获取和管理 access token
    """
    def __init__(self,code,openid,openkey):
        """
        初始化
        """
        self.client_id = config.tw_client_id
        self.app_secret = config.tw_client_secret
        self.redirect_uri = config.tw_redirect_uri
        self.code = code 
        self.openid = openid
        self.openkey = openkey
        
    def getAccessToken(self):
        """
        如果获取成功,返回一个字典,包含accesstoken等信息
        如果获取失败,返回一个字典,包含errorCode和errorMsg
        """
        targetUrl = config.tw_access_token_url % (self.client_id,self.app_secret,self.redirect_uri,self.code)
        result = utils.urlRead(targetUrl)
        return utils.urlParamToDicParam(result)
    
    def refreshAccessToken(self,refresh_token):
        """
        用来刷新accessToken,需要refresh_token参数
        """
        targetUrl = config.tw_refresh_token_url % (self.client_id,refresh_token)
        result = utils.urlRead(targetUrl)
        return utils.urlParamToDicParam(result)
    
    @staticmethod
    def getRequestCodeUrl(request):
        client_id = config.tw_client_id
        redirect_uri = config.tw_redirect_uri
        import random
        state = random.randint(100000,999999)
        request.session["oauthState"] = str(state)
        url = config.tw_request_code % (client_id,redirect_uri,state)
        return url
    
if __name__ == '__main__':
    pass