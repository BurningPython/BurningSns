from django.shortcuts import render


def index_view(request):
    me = None
    user = request.user
    if user.is_authenticated():
        if user.is_active:
            me = user

    return render(request, "index.html", {'user':me})