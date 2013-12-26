from django.shortcuts import render,redirect
from accounts.snsService.hotService import *


def content_view(request):
    user = request.user
    if not user.is_authenticated():
        return redirect("index")

    service = StatusService(user)
    ret = service.GetFriendsStatuses()
    return render(
        request,
        "website/content.html",
        {'user': user, 'timelinecontent': ret.data,'errors':ret.errors}
    )
