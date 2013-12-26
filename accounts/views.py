from urllib.request import urlopen

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login as _login, logout
from BurningSns.config import domain
from accounts.snsService.tokenService import TokenService
from accounts.snsService.oauthService import OpenAuthService
from accounts.models import User
from accounts.forms import RegisterForm, LoginForm
from accounts.utils import unparse_params, get_client_ip


def login(request, user):
    user.ip_address = get_client_ip(request)
    user.save()

    _login(request, user)


def register_view(request):
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


def tw_oauth_confirm(request, action):
    """
    处理请求完code后的回调,同时申请腾讯微博accessToken
    """

    if 'state' in request.GET:
        state = request.GET['state']
        #防止跨站伪造请求攻击
        #if state == request.session['_oauth_state']:
        if True:
            code = request.GET['code']
            openid = request.GET['openid']
            openkey = request.GET['openkey']

            from accounts.snsService.handlers.tencentWeiboHandler import client_id, client_secret

            access_token_url = "https://open.t.qq.com/cgi-bin/oauth2/access_token?"\
                               + "client_id=%s&client_secret=%s&redirect_uri=%s&gra"\
                               + "nt_type=authorization_code&code=%s&state=%s"
            redirect_uri = domain + reverse("account:tw_oauth_confirm", kwargs = {"action":action})
            targetUrl = access_token_url % (client_id, client_secret, redirect_uri, code, state)

            response = str(urlopen(targetUrl).read(), encoding = "utf-8")
            params = unparse_params(response)
            if "access_token" in params:
                user = request.user
                if action == "bind":
                    #如果是已登录的用户,则绑定一个openauth
                    if user.is_authenticated():
                        tokenService = TokenService(user)
                        tokenService.addToken(site = u"腾讯微博", **params)
                    else:
                        return redirect("account:login")
                #如果是通过第三方认证登录的用户,检查该token是否已经绑定到某个账号,如果是的话,返回该用户
                #否则系统自动创建一个账户,并绑定这个token
                elif action == "login":
                    oauthService = OpenAuthService(site = u"腾讯微博", **params)
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


def tw_oauth_request(request, action):
    """
    请求腾讯微博的code
    """
    import random

    state = random.randint(100000, 999999)
    request.session['_oauth_state'] = str(state)

    request_code = "https://open.t.qq.com/cgi-bin/oauth2/authorize?"\
                   + "client_id=%s&response_type=code&redirect_uri=%s&state=%s"

    redirect_uri = domain + reverse("account:tw_oauth_confirm", kwargs = {"action":action})

    from .snsService.handlers.tencentWeiboHandler import client_id

    url = request_code % (client_id, redirect_uri, state)

    return redirect(url)

