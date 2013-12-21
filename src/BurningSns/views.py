from django.shortcuts import render
from django.http import HttpResponseRedirect

def index_view(request):
    return render(request,"BurningSns/index.html")

def content_view(request):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect("index")
    
    #tencent_weibo_handler
    twh = user.get_open_auth_handler("腾讯微博",request)
    if twh:
        content = twh.home_timeline()
    else:
        content = None
    return render(request,"BurningSns/content.html",{'user':user,'timelinecontent':content})