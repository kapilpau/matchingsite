from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseBadRequest, JsonResponse
from .models import Member, Hobby
from django.core import serializers
from django.db.models.functions import Lower


def index(request):
    try:
        user = request.session['username']
        isAdmin = request.session['isAdmin']
    except KeyError:
        user = ""
        isAdmin = ""
    context = {'siteName': 'Bindr', 'username': user, 'isAdmin': isAdmin}
    return render(request, 'matchingapp/index.html', context)


def admin(request):
    try:
        user = request.session['username']
        isAdmin = request.session['isAdmin']
    except KeyError:
        user = ""
        isAdmin = ""
    context = {'siteName': 'Bindr', 'username': user, 'isAdmin': isAdmin}
    return render(request, 'matchingapp/admin.html', context)


def login(request):
    if request.method == 'GET':
        try:
            user = request.session['username']
            isAdmin = request.session['isAdmin']
        except KeyError:
            user = ""
            isAdmin = ""
        context = {'siteName': 'Bindr', 'username': user, 'isAdmin': isAdmin}
        return render(request, 'matchingapp/login.html', context)
    elif request.method == 'POST':
        if request.is_ajax():
            try:
                mem = Member.objects.get(username=request.POST['username'], password=request.POST['password'])
                request.session['username'] = request.POST['username']
                request.session['isAdmin'] = mem.isAdmin
                return HttpResponse()
            except Member.DoesNotExist:
                return HttpResponseBadRequest('Member does not exist')


def signup(request):
    if request.method == 'POST':
        if request.is_ajax():
            try:
                mem = Member(username=request.POST['username'], password=request.POST['password'])
                mem.save()
                request.session['username'] = request.POST['username']
                request.session['isAdmin'] = mem.isAdmin
                return HttpResponse()
            except IntegrityError:
                return HttpResponseBadRequest('Username already taken')


def profile(request):
    try:
        user = request.session['username']
        isAdmin = request.session['isAdmin']
    except KeyError:
        user = ""
        isAdmin = ""
    context = {'siteName': 'Bindr', 'username': user, 'isAdmin': isAdmin}
    return render(request, 'matchingapp/profile.html', context)


def getHobbies(request):
    if request.is_ajax():
        if request.method == 'GET':
            hobby_list = Hobby.objects.all().order_by(Lower('name'))
            return JsonResponse(serializers.serialize('json', hobby_list), safe=False)
    else:
        return HttpResponseBadRequest("Request must be ajax")


def addHobby(request):
    if request.is_ajax():
        if request.method == 'POST':
            try:
                Hobby.objects.create(name=request.POST['name'])
                return HttpResponse()
            except IntegrityError:
                return HttpResponseBadRequest('Hobby already exists')

    else:
        return HttpResponseBadRequest("Request must be ajax")


def deleteHobby(request):
    if request.is_ajax():
        if request.method == 'DELETE':
            Hobby.objects.filter(id=request.body.decode('utf-8').split('=')[1]).delete()
            return HttpResponse("OK")
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest("Request must be ajax")