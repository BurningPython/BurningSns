__author__ = 'july'

from django.shortcuts import redirect

def login(request, user):
    """
    登录,在原功能上加入了记录ip地址的功能
    """
    from accounts.utils import get_client_ip
    user.ip_address = get_client_ip(request)
    user.save()

    from django.contrib.auth import login as _login
    _login(request, user)

def logined_redirect(request, redirect_view="home:content"):
    """
    已登录后跳转
    """
    user = request.user
    if user.is_authenticated():
        if user.is_active:
            return redirect(redirect_view)

def unlogined_redirect(request,redirect_view="account:login"):
    """
    未登录跳转
    """
    user = request.user
    if user.is_authenticated():
        if not user.is_active:
            return redirect(redirect_view)

