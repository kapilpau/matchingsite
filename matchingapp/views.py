from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from .models import Member


def index(request):
    try:
        user = request.session['username']
    except KeyError:
        user = ""
    context = {'siteName': 'Bindr', 'username': user}
    return render(request, 'matchingapp/index.html', context)


def admin(request):
    try:
        user = request.session['username']
    except KeyError:
        user = ""
    context = {'siteName': 'Bindr', 'username': user}
    return render(request, 'matchingapp/index.html', context)


def login(request):
    if request.method == 'GET':
        try:
            user = request.session['username']
        except KeyError:
            user = ""
        context = {'siteName': 'Bindr', 'username': user}
        return render(request, 'matchingapp/login.html', context)
    elif request.method == 'POST':
        if request.is_ajax():
            try:
                Member.objects.get(username=request.POST['username'], password=request.POST['password'])
                request.session['username'] = request.POST['username']
                return HttpResponse()
            except Member.DoesNotExist:
                return HttpResponseBadRequest('Member does not exist')


def profile(request):
    try:
        user = request.session['username']
    except KeyError:
        user = ""
    context = {'siteName': 'Bindr', 'username': user}
    return render(request, 'matchingapp/profile.html', context)
