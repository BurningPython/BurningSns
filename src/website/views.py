from django.shortcuts import render
from django.http import HttpResponseRedirect
from accounts.snsService.hotService import *


def content_view(request):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect("index")

    service = StatusService(user)
    if service:
        content = service.GetFriendsStatuses()
    else:
        content = None
    return render(request, "website/content.html", {'user': user, 'timelinecontent': content})
