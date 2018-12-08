from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.http import HttpResponse, QueryDict, HttpResponseBadRequest, JsonResponse, HttpResponseServerError, FileResponse
from .models import Member, Hobby, Profile, Conversation, Message
from django.core import serializers
from django.db.models.functions import Lower, datetime
import random, os
from datetime import date
from bcrypt import hashpw
import json

# Fixed salt for hashing passwords to make sure that the hashing is constant
salt = b'$2b$12$Jx1Vfxjy0iuMxP0cBeDctu'

# Decorator to test if user is logged in, and if not to redirect to login
def loggedin(view):
    def mod_view(request):
        if 'username' in request.session:
            try:
                return view(request)
            except Member.DoesNotExist:
                request.session.flush()
                return render(request, 'matchingapp/login.html', getContext(request))
        else:
            return render(request, 'matchingapp/login.html', getContext(request))
    return mod_view

# Decorator to test if user is logged in and admin, if not then redirect to log in or index
def isadmin(view):
    def mod_view(request):
        if 'username' in request.session:
            if request.session['isAdmin'] is True:
                return view(request)
            else:
                return redirect('/')
        else:
            return  redirect('/login/')
    return mod_view


# View to display the index page to the users which displays the list of users which the user hasn't already matched
# with or requested
@loggedin
def index(request):
    context = getContext(request)
    return render(request, 'matchingapp/index.html', context)


# View to display the list of hobbies for the admins to edit
@isadmin
def admin(request):
    context = getContext(request)
    return render(request, 'matchingapp/admin.html', context)


# View split into get and post, if the method is get, then return the login page, otherwise test if the user exists
# and the password is correct. If they are then set up the user's session, otherwise return the appropriate error
def login(request):
    if request.method == 'GET':
        context = getContext(request)
        return render(request, 'matchingapp/login.html', context)
    elif request.method == 'POST':
        if request.is_ajax():
            try:
                mem = Member.objects.get(username=request.POST['username'])
                if mem.password != hashpw(request.POST['password'].encode('utf-8'), salt).decode("utf-8"):
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


# View split into get and post, if the method is get, then return the sign up page, otherwise attempt to create the user
# and their profile, if it can't then through an error
def signup(request):
    if request.method == 'POST':
        if request.is_ajax():
            try:
                req_dets = dict(request.POST.lists())
                mem = Member(username=req_dets['username'][0], password=hashpw(req_dets['password'][0].encode('utf-8'), salt).decode("utf-8"))
                try:
                    mem.save()
                except IntegrityError:
                    return HttpResponseBadRequest('Username already taken')
                hobbies = []
                checkedHobbies = req_dets['profile[checkedHobbies][]']
                for hobby in checkedHobbies:
                    hobbies.append(Hobby.objects.get(name=hobby))
                prof = Profile.objects.create(profile_image='profile_images/silhouette.png', name=req_dets['profile[name]'][0], email=req_dets['profile[email]'][0], dob=datetime.datetime.strptime(req_dets['profile[dob]'][0], "%Y-%m-%d").date(), gender=req_dets['profile[gender]'][0])
                # prof.save()
                prof.hobbies.set(hobbies)
                prof.save()
                mem.profile = prof
                mem.save()
                request.session['profile'] = {'id': prof.pk, 'profile_image': prof.profile_image.url, 'name': prof.name, 'email': prof.email, 'gender': prof.gender, 'dob': str(prof.dob), 'hobbies': serializers.serialize('json', prof.hobbies.all())}
                print(request.session['profile'])
                print(mem.profile.hobbies.all())
                for key, value in request.session.items():
                    print('{} => {}'.format(key, value))
                request.session['username'] = request.POST['username']
                request.session['isAdmin'] = mem.isAdmin
                return HttpResponse()
            except:
                return HttpResponseBadRequest('Something went wrong')

    else:
        if 'username' in request.session:
            return redirect('/')
        context = getContext(request)
        hobby_set = Hobby.objects.values_list('name', flat=True)
        context['hobby_list'] = list(hobby_set)
        return render(request, 'matchingapp/signup.html', context)


# Attempts to display the profile of the user specified in the url
# Intermittent error meaning that the whole view is surrounded in a try catch which redirects to the index
# Cause unknown, occurs seemingly randomly and unable to replicate
def profile(request, prof=None):
    try:
        pfl = Profile.objects.get(id=prof)
        print(pfl)
        mem = Member.objects.get(profile=pfl)
        user = Member.objects.get(username=request.session['username'])
        if prof == user.profile.id:
            return redirect('/profile/')
        context = getContext(request)
        hobby_set = Hobby.objects.values_list('name', flat=True)
        context['hobby_list'] = list(hobby_set)
        pfl = Profile.objects.get(id=prof)
        context['profile'] = {'id': pfl.pk, 'profile_image': pfl.profile_image.url, 'name': pfl.name,
                                      'email': pfl.email, 'gender': pfl.gender, 'dob': str(pfl.dob),
                                      'hobbies': list(pfl.hobbies.values_list('name', flat=True))}
        print(context)
        match_status = 0
        if mem in user.match_requests.all():
            match_status = 1
        elif mem in user.matches.all():
            match_status = 2
        elif user in mem.match_requests.all():
            match_status = 3
        context['match_status'] = match_status
        return render(request, 'matchingapp/profile.html', context)
    except KeyError:
        return redirect('/')


# Displays the user's own profile, through this page, they can update their profile
@loggedin
def userProfile(request):
    context = getContext(request)
    hobby_set = Hobby.objects.values_list('name', flat=True)
    context['hobby_list'] = list(hobby_set)
    print(context)
    return render(request, 'matchingapp/user_profile.html', context)


# API endpoint to return the list of possible hobbies
def getHobbies(request):
    if request.is_ajax():
        if request.method == 'GET':
            hobby_list = Hobby.objects.all().order_by(Lower('name'))
            return JsonResponse(serializers.serialize('json', hobby_list), safe=False)
    else:
        return HttpResponseBadRequest("Request must be ajax")


# API endpoint to add a new hobby, can only best called if the user is an admin
@isadmin
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


# API endpoint to delete a hobby, can only best called if the user is an admin
@isadmin
def deleteHobby(request):
    if request.is_ajax():
        if request.method == 'DELETE':
            Hobby.objects.filter(id=request.body.decode('utf-8').split('=')[1]).delete()
            return HttpResponse("OK")
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest("Request must be ajax")


# Function to return the context which should be pages to the templates when they are rendered
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
    try:
        mem = Member.objects.get(username=request.session['username'])
        matches = []
        for match in mem.matches.all():
            matches.append({'id': match.profile.id, 'name': match.profile.name})
        request.session['matches'] = matches
    except:
        matches = []
        request.session['matches'] = []
    try:
        mem = Member.objects.get(username=request.session['username'])
        match_requests = []
        for match in mem.match_requests.all():
            match_requests.append({'id': match.profile.id, 'name': match.profile.name})
        request.session['match_requests'] = match_requests
    except:
        match_requests = []
        request.session['match_requests'] = []
    #     Graftr/Bindr
    context = {'siteName': 'LinkUp', 'username': user, 'isAdmin': isAdmin, 'profile': profile, 'matches': matches, 'match_requests': match_requests}
    return context


# API endpoint for a user to update their profile
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
    pfl.save()
    request.session['profile'] = {'id': pfl.pk, 'profile_image': pfl.profile_image.url, 'name': pfl.name,
                                  'email': pfl.email, 'gender': pfl.gender, 'dob': str(pfl.dob),
                                  'hobbies': serializers.serialize('json', pfl.hobbies.all())}
    return HttpResponse()


# API endpoint to allow the user to upload a new profile picture. The view stores the file with a random name and then
# stores the file name in their profile record in the database
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
                random.randint(10000, 100000000000)) + '_' + str(
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


# API end point for the index page. It returns the list of users which the user hasn't already requested or matched with
@loggedin
def getUsers(request):
    if request.method == 'GET' and request.is_ajax():
        pfls = Profile.objects.exclude(member__username=request.session['username'])
        print(pfls)
        resp = []
        for pfl in pfls:
            if (Member.objects.get(username=request.session['username']) not in Member.objects.get(profile=pfl).matches.all()) and (Member.objects.get(username=request.session['username']) not in Member.objects.get(profile=pfl).match_requests.all()):
                hobbies = []
                for hobby in pfl.hobbies.all():
                    hobbies.append(hobby.name)
                today = date.today()
                born = pfl.dob
                resp.append({'id': pfl.id, 'name': pfl.name, 'hobbies': hobbies, 'gender': pfl.gender, 'age': today.year - born.year - ((today.month, today.day) < (born.month, born.day))})
        return JsonResponse(resp, safe=False)


# Signs the user out by flushing the session and redirects them to the login page
def signout(request):
    request.session.flush()
    return redirect('/login/')


# API to request to match with the user specified in the request
@loggedin
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


# View which displays the user's match requests and matches
@loggedin
def matches(request):
    context = getContext(request)
    print(context)
    return render(request, 'matchingapp/matches.html', context)


# API endpoint to allow the user to accept or reject a match request
@loggedin
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


# API endpoint to allow the user to delete a match
@loggedin
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


# View which displays the user's conversations
@loggedin
def messages(request):
    convos = Conversation.objects.all()
    user = Member.objects.get(username=request.session['username'])
    contextConvos = []
    for convo in convos:
        if user in convo.participants.all():
            readStatus = False
            print(Message.objects.order_by('sent_at').filter(conversation=convo))
            try:
                if user in Message.objects.order_by('sent_at').filter(conversation=convo).last().read_by.all():
                    readStatus = True
            except AttributeError:
                readStatus = True
            contextConvos.append({'id': convo.id, 'name': convo.name, 'read': readStatus})
    context = getContext(request)
    context['conversations'] = contextConvos
    return render(request, 'matchingapp/messages.html', context)


# A redirecting view to allow the user to go to their conversation with another user from the matches page or the user's profile
def convoRedirect(request, id):
    prof = Member.objects.get(profile=Profile.objects.get(id=id))
    user = Member.objects.get(username=request.session['username'])
    convos = Conversation.objects.all()
    for convo in convos:
        if (convo.participants.count() == 2) and (prof in convo.participants.all()) and (user in convo.participants.all()):
            return redirect('/messages/' + str(convo.id))
    if prof.profile.name > user.profile.name:
        name = user.profile.name + ", " + prof.profile.name
    else:
        name = prof.profile.name + ", " + user.profile.name
    convo = Conversation.objects.create(name=name)
    convo.participants.add(prof)
    convo.participants.add(user)
    convo.save()
    return redirect('/messages/' + str(convo.id))


# A view to which contains the user's conversation
def conversation(request, id):
    context = getContext(request)
    try:
        msgs = Message.objects.order_by('sent_at').filter(conversation=Conversation.objects.get(id=id))
        user = Member.objects.get(username=request.session['username'])
        print(Conversation.objects.get(id=id).participants.all())
        if user not in Conversation.objects.get(id=id).participants.all():
            return redirect('/')
        contextMsgs = []
        for msg in msgs:
            contextMsgs.append({'sender': msg.sender.profile.name, 'sent_at': msg.sent_at.strftime("%Y-%m-%d %H:%M:%S"), 'contents': msg.contents})
            context['msgs'] = contextMsgs
            msg.read_by.add(user)
            msg.save()
    except Message.DoesNotExist:
        context['msgs'] = {}
    return render(request, 'matchingapp/conversation.html', context)


# API endpoint to allow the user to cancel a match request with a user
@loggedin
def cancelRequest(request):
    if request.method == 'POST':
        prof = Profile.objects.get(id=request.POST['id'])
        mem = Member.objects.get(profile=prof)
        user = Member.objects.get(username=request.session['username'])
        if user in mem.match_requests.all():
            mem.match_requests.remove(user)
            mem.save()
            return HttpResponse()
        else:
            return HttpResponseBadRequest(user.profile.name + " hasn't requested to match with " + prof.name)
    else:
        return HttpResponseBadRequest('Request must be post')


def static(request, appname, foldername, filename):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_name = os.path.join(BASE_DIR, "matchingapp/static") + "/" + appname + "/" + foldername + "/" + filename
    if os.path.exists(file_name):
        try:
            file = open(file_name, 'rb')
        except:
            print("Foo")
    else:
        print("Doesn't exist bro")
    return FileResponse(file)


def media(request, foldername, filename):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_name = os.path.join(BASE_DIR, "media") + "/" + foldername + "/" + filename
    if os.path.exists(file_name):
        try:
            file = open(file_name, 'rb')
        except:
            print("Foo")
    else:
        print("Doesn't exist bro")
    return FileResponse(file)


def favicon(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_name = os.path.join(BASE_DIR, "media/favicon.ico")
    if os.path.exists(file_name):
        try:
            file = open(file_name, 'rb')
        except:
            print("Foo")
    else:
        print("Doesn't exist bro")
    return FileResponse(file)
