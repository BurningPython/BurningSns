from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from Accounts.OpenAuth.oauthManager import OpenAuthManager
from Accounts.OpenAuth.sns.tencentWeibo import TokenManager as twm
from Accounts.models import MyUser
from Accounts.forms import RegisterForm,LoginForm
# Create your views here.

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]
            user = MyUser.objects.create(username = username,email = email)
            user.set_password(password)
            user.save()
            
            user = authenticate(username = username,password = password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect("/")
                
    else:
        form = RegisterForm()
    return render(request,"Accounts/register.html",{
        "form":form
    })

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username = username,password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect("/content")
    else:
        form = LoginForm()
    return render(request,"Accounts/login.html",{
        "form":form,
    })

def logout_view(request):
    user = request.user
    if user.is_authenticated():
        logout(request)
    return HttpResponseRedirect("/")

def tw_oauthProcess(request):
    """
    处理请求完code后的回调,同时申请腾讯微博accessToken
    """
    
    code = request.GET['code']
    openid = request.GET['openid']
    openkey = request.GET['openkey']
    state = request.GET['state']
    
    #防止跨站伪造请求攻击
    if(state == request.session['oauthState']):
        retdic = twm(code,openid,openkey).getAccessToken()
        if "access_token" in retdic:
            oauthManager = OpenAuthManager(**retdic)
            user = request.user
            #如果是已注册并登陆的用户,则绑定一个openauth
            if user.is_authenticated():
                oauthManager.createOrUpdateOpenAuth(user.username, u"腾讯微博")
            #否则,系统自动创建一个账户,并绑定openauth
            else:
                ret = oauthManager.getUser(u"腾讯微博")
                user = ret["user"]
                if user.is_active:
                    login(request,user)
                
            return HttpResponseRedirect("/content")
        else:
            pass
        
    return HttpResponseRedirect("/")

def tw_oauthBegin(request):
    """
    请求腾讯微博的code
    """
    url = twm.getRequestCodeUrl(request)
    
    return HttpResponseRedirect(url)

