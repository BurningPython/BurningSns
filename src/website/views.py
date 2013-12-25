from django.shortcuts import render
from django.http import HttpResponseRedirect
from accounts.snsService.hotService import *


def content_view(request):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect("index")

    service = StatusService(user)
    ret = service.GetFriendsStatuses()
    if ret.code == 1:
        content = ret.data
        print(content)
    else:
        content = None
    return render(request, "website/content.html", {'user': user, 'timelinecontent': content})
