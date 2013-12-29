#encoding="utf8"
from urllib.request import urlopen

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, logout
from accounts.shortcutes import login,logined_redirect,unlogined_redirect
from BurningSns.config import domain
from accounts.platform.tokenService import TokenService
from accounts.platform.oauthService import OpenAuthService
from accounts.models import User
from accounts.forms import RegisterForm, LoginForm
from accounts.utils import unparse_params, get_client_ip




def register_view(request):
    logined_redirect(request)

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]
            user = User.objects.create(username = username, email = email)
            user.set_password(password)
            user.save()

            user = authenticate(username = username, password = password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("/")

    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {
        "form":form
    })


def login_view(request):
    logined_redirect(request)

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username = username, password = password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("home:content")
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {
        "form":form,
    })


def logout_view(request):
    user = request.user
    if user.is_authenticated():
        logout(request)
    return redirect("index")


def tw_oauth_confirm(request):
    """
    处理请求完code后的回调,同时申请腾讯微博accessToken
    """

    if 'state' in request.GET:
        state = request.GET['state']
        #防止跨站伪造请求攻击
        # if state == request.session["oauthstate"]:
        if True:
            code = request.GET['code']
            # openid = request.GET['openid']
            # openkey = request.GET['openkey']

            from accounts.platform.handlers.tencentWeiboHandler import client_id, client_secret

            access_token_url = "https://open.t.qq.com/cgi-bin/oauth2/access_token?"\
                               + "client_id=%s&client_secret=%s&redirect_uri=%s&gra"\
                               + "nt_type=authorization_code&code=%s&state=%s"
            redirect_uri = domain + reverse("account:tw_oauth_confirm")
            targetUrl = access_token_url % (client_id, client_secret, redirect_uri, code, state)

            response = str(urlopen(targetUrl).read(), encoding = "utf-8")
            params = unparse_params(response)
            if "access_token" in params:
                user = request.user
                if user.is_authenticated():
                    #如果是已登录的用户,则绑定一个openauth
                    tokenService = TokenService(user)
                    tokenService.addToken(site = 'tw', **params)
                #如果是通过第三方认证登录的用户,检查该token是否已经绑定到某个账号,如果是的话,返回该用户
                #否则系统自动创建一个账户,并绑定这个token
                else:
                    oauthService = OpenAuthService(site = 'tw', **params)
                    ret = oauthService.get_or_create_user()
                    user = ret["user"]
                    if user.is_active:
                        login(request, user)
                    else:
                        return redirect("index")

                return redirect("home:content")
            else:
                pass
    else:
        pass

    return redirect("index")


def tw_oauth_request(request):
    """
    请求腾讯微博的code
    """
    import random

    state = random.randint(100000, 999999)
    request.session["oauthstate"] = str(state)

    request_code = "https://open.t.qq.com/cgi-bin/oauth2/authorize?"\
                   + "client_id=%s&response_type=code&redirect_uri=%s&state=%s"

    redirect_uri = domain + reverse("account:tw_oauth_confirm")

    from accounts.platform.handlers.tencentWeiboHandler import client_id

    url = request_code % (client_id, redirect_uri, state)

    return redirect(url)


def sw_oauth_confirm(request):
    """
    处理请求完code后的回调,同时申请腾讯微博accessToken
    """
    #if request.GET["state"] != request.session['sw_oauth_state']:
    #    print(request.GET["state"])
    a = {}
    a['client_id'] = '2749469053'
    a['client_secret'] = '22a991ef6b614ebc2bcb75555b5a1aec'
    a['grant_type'] = 'authorization_code'
    a['redirect_uri'] = domain + reverse("account:sw_oauth_confirm")
    a['code'] = request.GET["code"]
    import urllib.request
    import urllib.parse
    import json

    querystring = urllib.parse.urlencode(a)
    by = urllib.request.urlopen('https://api.weibo.com/oauth2/access_token',
                                data=bytes(querystring.encode('utf8'))).read()
    j = json.loads(str(by, encoding='utf8'))
    for item in j:
        print("item:" + item)

    if "access_token" in j:
        user = request.user
        if user.is_authenticated():
            tokenService = TokenService(user)
            tokenService.addToken(site=u"sina", access_token=j["access_token"], refresh_token="",
                                  expires_in=j['expires_in'], remind_in=j['remind_in'], openid=j['uid'])
        else:
            oauthService = OpenAuthService(site=u"sina", access_token=j["access_token"], refresh_token="",
                                           expires_in=j['expires_in'], remind_in=j['remind_in'], openid=j['uid'])
            ret = oauthService.get_or_create_user()
            user = ret["user"]
            if user.is_active:
                login(request, user)
            else:
                return redirect("index")
        return redirect("home:statuses")
    else:
        pass
    return redirect("index")


def sw_oauth_request(request):
    """
    请求腾讯微博的code
    """
    import random

    state = random.randint(100000, 999999)
    request.session['sw_oauth_state'] = str(state)
    request_code = r'https://api.weibo.com/oauth2/authorize?client_id='\
                   + '2749469053'\
                   + '&response_type=code&redirect_uri='\
                   + domain + reverse("account:sw_oauth_confirm")\
                   + '&state='\
                   + str(state)
    return redirect(request_code)


def oauth_manage_view(request):
    """
    用户的第三方平台账号管理页面
    """

    unlogined_redirect(request)

    from accounts.platform.config import site_config
    import copy

    sitelist = copy.deepcopy(site_config)

    ts = TokenService(request.user)
    for site in sitelist:
        for token in ts.getTokens():
            if token.site == site['site']:
                site['token'] = token

    return render(request,'accounts/oauth_manage.html',{'sitelist':sitelist})

def destroy_oauth(request,site):
    """
    删除一个绑定
    """
    unlogined_redirect(request)

    ts=TokenService(request.user)
    ts.deleteToken(site)
    return redirect("account:oauth_manage")
