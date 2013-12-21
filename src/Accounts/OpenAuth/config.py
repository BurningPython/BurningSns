'''
Created on 2013年12月11日

@author: july
'''
#腾讯微博相关
tw_client_id = "801453781"
tw_client_secret = "c2ee75038d707a610c7a4a10c0377c2e"
tw_redirect_uri = "http://127.0.0.1:8000/account/tw_oauthProcess"
tw_request_code = "https://open.t.qq.com/cgi-bin/oauth2/authorize?client_id=%s&response_type=code&redirect_uri=%s&state=%s"
tw_access_token_url = "https://open.t.qq.com/cgi-bin/oauth2/access_token?client_id=%s&client_secret=%s&redirect_uri=%s&grant_type=authorization_code&code=%s"
tw_refresh_token_url = "https://open.t.qq.com/cgi-bin/oauth2/access_token?client_id=%s&grant_type=refresh_token&refresh_token=%s"
tw_api_url = "https://open.t.qq.com/api/%s?"
tw_api_common_parm = "oauth_consumer_key=%s&access_token=%s&openid=%s&clientip=%s&oauth_version=%s&scope=%s&"
tw_oauth_version = "2.a"
#搜狐微博相关
sw_client_id = "QzijcaDQtONTNKv4MNE5"
sw_redirect_uri = "http://127.0.0.1:8000/account/sw_oauthProcess"
sw_consumer_key = "QzijcaDQtONTNKv4MNE5"
sw_consumer_secret ="-tPcwNR(X!B4^88MkBfD=ugQS1etGJMV-^VgGiU9"
sw_request_token_url = "https://api.t.sohu.com/oauth2/request_token"
sw_access_token_url = "https://api.t.sohu.com/oauth2/access_token?client_id=%s&client_secret=%s&grant_type=authorization_code&code=%s&redirect_uri=%s&state=%s"
sw_authorize_url = "https://api.t.sohu.com/oauth2/authorize?client_id=%s&scope=basic&response_type=code&redirect_uri=%s&state=%s"
#点点网相关
diandian_client_id = ""     #点点网是老子的,别跟我抢.----by Eleven 2013-12-18 15:15
diandian_client_secret = ""
