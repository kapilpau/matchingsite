from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.http import HttpResponse, QueryDict, HttpResponseBadRequest, JsonResponse, HttpResponseServerError
from .models import Member, Hobby, Profile
from django.core import serializers
from django.db.models.functions import Lower, datetime
import random, os
from datetime import date


# decorator that tests whether user is logged in
def loggedin(view):
    def mod_view(request):
        if 'username' in request.session:
            return view(request)
        else:
            return render(request, 'matchingapp/login.html', getContext())
    return mod_view


def index(request):
    context = getContext(request)
    return render(request, 'matchingapp/index.html', context)


def admin(request):
    context = getContext(request)
    return render(request, 'matchingapp/admin.html', context)


def login(request):
    if request.method == 'GET':
        context = getContext(request)
        return render(request, 'matchingapp/login.html', context)
    elif request.method == 'POST':
        if request.is_ajax():
            try:
                mem = Member.objects.get(username=request.POST['username'])
                if mem.password != request.POST['password']:
                    return HttpResponseBadRequest('Incorrect password')
                request.session['username'] = request.POST['username']
                request.session['isAdmin'] = mem.isAdmin
                try:
                    pfl = mem.profile
                    request.session['profile'] = {'id': pfl.pk, 'profile_image': pfl.profile_image.url, 'name': pfl.name, 'email': pfl.email, 'gender': pfl.gender, 'dob': str(pfl.dob), 'hobbies': serializers.serialize('json', pfl.hobbies.all())}
                except:
                    request.session['profile'] = {}
                return HttpResponse()
            except Member.DoesNotExist:
                return HttpResponseBadRequest('Member does not exist')
        else:
            return HttpResponseBadRequest('Request must ajax')


def signup(request):
    if request.method == 'POST':
        if request.is_ajax():
            try:
                mem = Member(username=request.POST['username'], password=request.POST['password'])
                mem.save()
                request.session['username'] = request.POST['username']
                request.session['isAdmin'] = mem.isAdmin
                request.session['profile'] = {}
                return HttpResponse()
            except IntegrityError:
                return HttpResponseBadRequest('Username already taken')


def profile(request, prof=None):
    print(prof)
    print(Profile.objects.get(member__username=request.session['username']))
    if prof == Profile.objects.get(member__username=request.session['username']).id:
        return redirect('/profile/')
    context = getContext(request)
    hobby_set = Hobby.objects.values_list('name', flat=True)
    context['hobby_list'] = list(hobby_set)
    pfl = Profile.objects.get(id=prof)
    context['profile'] = {'id': pfl.pk, 'profile_image': pfl.profile_image.url, 'name': pfl.name,
                                  'email': pfl.email, 'gender': pfl.gender, 'dob': str(pfl.dob),
                                  'hobbies': list(pfl.hobbies.values_list('name', flat=True))}
    print(context)
    return render(request, 'matchingapp/profile.html', context)


def userProfile(request):
    context = getContext(request)
    hobby_set = Hobby.objects.values_list('name', flat=True)
    context['hobby_list'] = list(hobby_set)
    return render(request, 'matchingapp/user_profile.html', context)


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


def getContext(request):
    try:
        user = request.session['username']
    except KeyError:
        user = ""
    try:
        isAdmin = request.session['isAdmin']
    except KeyError:
        isAdmin = ""
    try:
        profile = request.session['profile']
    except KeyError:
        profile = {}
    mem = Member.objects.get(username=request.session['username'])
    try:
        matches = []
        for match in mem.matches.all():
            matches.append({'id': match.profile.id, 'name': match.profile.name})
        request.session['matches'] = matches
    except:
        matches = []
        request.session['matches'] = []
    try:
        match_requests = []
        for match in mem.match_requests.all():
            match_requests.append({'id': match.profile.id, 'name': match.profile.name})
        request.session['match_requests'] = match_requests
    except:
        match_requests = []
        request.session['match_requests'] = []
    #     Graftr/Bindr
    context = {'siteName': 'Graftr', 'username': user, 'isAdmin': isAdmin, 'profile': profile, 'matches': matches, 'match_requests': match_requests}
    return context


@loggedin
def updateProfile(request):
    request_dets = QueryDict(request.body)
    mem = Member.objects.get(username=request.session['username'])
    pfl = mem.profile
    hobbies = []
    checkedHobbies = request_dets.getlist('checkedHobbies[]')
    for hobby in checkedHobbies:
        hobbies.append(Hobby.objects.get(name=hobby))
    if pfl is None:
        pfl = Profile.objects.create(profile_image='profile_images/silhouette.png', name=request_dets['name'], email=request_dets['email'], dob=datetime.datetime.strptime(request_dets['dob'], "%Y-%m-%d").date(), gender=request_dets['gender'])
        mem.profile = pfl
        mem.save()
    else:
        pfl.name = request_dets['name']
        pfl.email = request_dets['email']
        pfl.dob = datetime.datetime.strptime(request_dets['dob'], "%Y-%m-%d").date()
        pfl.gender = request_dets['gender']
    pfl.hobbies.set(hobbies)
    pfl.hobbies.set(hobbies)
    pfl.save()
    request.session['profile'] = {'id': pfl.pk, 'profile_image': pfl.profile_image.url, 'name': pfl.name,
                                  'email': pfl.email, 'gender': pfl.gender, 'dob': str(pfl.dob),
                                  'hobbies': serializers.serialize('json', pfl.hobbies.all())}
    return HttpResponse()


@loggedin
def uploadNewProfileImage(request):
    if 'new_img' in request.FILES:
        if request.session['profile'] == {}:
            return HttpResponseBadRequest('Please create your profile before adding a profile picture')
        new_img = request.FILES['new_img']
        filename = str(random.randint(10000, 100000000000)) + '_' + str(random.randint(10000, 100000000000)) + '_' + str(
            random.randint(10000, 100000000000)) + '.png'
        while filename in os.listdir(os.getcwd() + '/media/profile_images'):
            filename = str(random.randint(10000, 100000000000)) + '_' + str(
                random.randint(10000, 100000000000)) + _ + str(
                random.randint(10000, 100000000000)) + '.png'
        print(filename)
        new_img.name = filename
        try:
            pfl = Member.objects.get(username=request.session['username']).profile
            pfl.profile_image = new_img
            pfl.save()
            request.session['profile'] = {'id': pfl.pk, 'profile_image': pfl.profile_image.url, 'name': pfl.name,
                                          'email': pfl.email, 'gender': pfl.gender, 'dob': str(pfl.dob),
                                          'hobbies': serializers.serialize('json', pfl.hobbies.all())}
            return JsonResponse({'url': '/media/profile_images/' + filename})
        except:
            return HttpResponseServerError()
    else:
        print(request.FILES)
        return HttpResponseBadRequest('Image file required')


@loggedin
def getUsers(request):
    if request.method == 'GET' and request.is_ajax():
        pfls = Profile.objects.exclude(member__username=request.session['username'])
        print(pfls)
        resp = []
        for pfl in pfls:
            print(pfl.hobbies.all())
            hobbies = []
            for hobby in pfl.hobbies.all():
                hobbies.append(hobby.name)
            today = date.today()
            born = pfl.dob
            resp.append({'id': pfl.id, 'name': pfl.name, 'hobbies': hobbies, 'gender': pfl.gender, 'age': today.year - born.year - ((today.month, today.day) < (born.month, born.day))})
        return JsonResponse(resp, safe=False)


def signout(request):
    request.session.flush()
    return redirect('/login/')


def requestMatch(request):
    prof = Profile.objects.get(id=request.POST['id'])
    mem = Member.objects.get(profile=prof)
    user = Member.objects.get(username=request.session['username'])
    if mem in user.match_requests.all():
        try:
            user.matches.add(mem)
            user.save()
            user.match_requests.remove(mem)
            user.save()
        except:
            return HttpResponseServerError("Something went wrong")

    else:
        mem.match_requests.add(user)
        mem.save()
    return HttpResponse()


def matches(request):
    context = getContext(request)
    print(context)
    return render(request, 'matchingapp/matches.html', context)


def manageRequest(request):
    if request.method == 'POST':
        prof = Profile.objects.get(id=request.POST['id'])
        mem = Member.objects.get(profile=prof)
        user = Member.objects.get(username=request.session['username'])
        if request.POST['action'] == 'accept':
            if mem in user.match_requests.all():
                try:
                    user.matches.add(mem)
                    user.save()
                    user.match_requests.remove(mem)
                    user.save()
                    return JsonResponse({'id': prof.id, 'name': prof.name}, safe=False)
                except:
                    return HttpResponseServerError()
            else:
                return HttpResponseBadRequest(mem.profile.name + " hasn't requested to match")
        else:
            user.match_requests.remove(mem)
            return HttpResponse()
    else:
        return HttpResponseBadRequest()


def deleteMatch(request):
    if request.method == 'POST':
        prof = Profile.objects.get(id=request.POST['id'])
        mem = Member.objects.get(profile=prof)
        user = Member.objects.get(username=request.session['username'])
        if mem in user.matches.all():
            try:
                user.matches.remove(mem)
                user.save()
                return HttpResponse()
            except:
                return HttpResponseServerError()
        else:
            return HttpResponseBadRequest(mem.profile.name + " isn't matched")

    else:
        return HttpResponseBadRequest()


def messages(request):
    return HttpResponse()


def conversation(request):
    return HttpResponse()

