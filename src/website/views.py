from django.shortcuts import render
from django.http import HttpResponseRedirect
from accounts.OpenAuth.hotService import *


def content_view(request):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect("index")

    service = StatuseService()
    twh = None
    if twh:
        content = twh.home_timeline()
    else:
        content = None
    return render(request, "website/content.html", {'user': user, 'timelinecontent': content})
