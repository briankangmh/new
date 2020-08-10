# django
import calendar
import time
# python
from decimal import Decimal

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, auth
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone

# models
from users.models import Subject, Ticket, UserProfileInfo
from ticket_comments.models import Comment

from . import appenums


def home(request):
    if(request.method == "GET"):
        return render(request, "user/home.html")


def privacy_policy(request):
    if(request.method == "GET"):
        return render(request, "user/privacy.html")


def login(request):
    if(request.method == "POST"):
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('login')

        else:
            context = {
                'data': {
                    'error': 'Invaild Credential',
                }
            }
            return render(request, "user/signin.html", context)
    else:
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return redirect('/admin')
            if not request.user.userprofileinfo.ugroup:
                subject = Subject.objects.all()
                context = {
                    'data': {
                        'subject': subject,
                    }
                }
                return render(request, "user/social_signup.html", context)
            if request.user.userprofileinfo.ugroup == '1':
                return redirect('tutor')
            else:
                return redirect('tutee')
        else:
            subject = Subject.objects.all()
            context = {
                'data': {
                    'subject': subject,
                }
            }
            return render(request, "user/signin.html", context)


def logout(request):
    auth.logout(request)
    return redirect('login')


def signup(request):
    if(request.method == "POST"):
        name = request.POST['name']
        password = request.POST['password']
        subject = request.POST['expertise']
        country = request.POST['country']
        classg = request.POST['class']
        ugroup = request.POST['ugroup']
        if(request.POST['ssign'] == '1'):
            request.user.password = make_password(password)
            request.user.first_name = name
            request.user.save()
            user = auth.authenticate(
                username=request.user.username, password=password)
            UserProfileInfo.objects.filter(user_id=request.user.id).update(
                subject=subject, country=country, classg=classg, ugroup=ugroup)
            auth.login(request, user)
            return redirect('profile')

        email = request.POST['email']
        if User.objects.filter(username=email).exists():
            context = {
                'data': {
                    'request': request.POST.copy(),
                    'error': 'User Already Exists',
                }
            }
            return render(request, "user/signin.html", context)
        user = User.objects.create_user(
            username=email, password=password, first_name=name, email=email)
        user.save()
        up = UserProfileInfo(user=user, subject=subject,
                             country=country, classg=classg, ugroup=ugroup)
        up.save()
        # 'error': 'Username already exists',
        context = {
            'data': {
                'success': 'Signup Successfully Completed'
            }
        }
        return render(request, "user/signin.html", context)

    else:
        return redirect('login')


def profile(request):
    if request.user.is_authenticated:
        if request.user.userprofileinfo.ugroup == '1':
            return redirect('tutor')  # tutor
        else:
            return redirect('tutee')  # tutee
    else:
        return redirect('login')


def switch_user_type(request, ugroup):
    print("-------------> switch_user_type")
    if request.user.is_authenticated:
        UserProfileInfo.objects.filter(
            user_id=request.user.id).update(ugroup=ugroup)
        return redirect('login')
    else:
        return redirect('login')


def ticket_list(request):
    print("-------------> ticket_list")
    if request.user.is_authenticated:
        tickets = Ticket.objects.filter(user_id=request.user.id)
        context = {
            'data': {
                'tickets': tickets,
            }
        }
        return render(request, "user/ticket_list.html", context)
    else:
        return redirect('login')


def ticket(request):
    print("-------------> ticket")
    if request.user.is_authenticated:
        if(request.method == "POST"):
            ref_id = request.POST['ref_id']
            title = request.POST['title']
            desc = request.POST['desc']
            ts = calendar.timegm(time.gmtime())
            now = timezone.now()
            ticket = Ticket(user=request.user, title=title, desc=desc,
                            ref_id=ref_id, date_updated=now)
            ticket.save()

            return redirect("/viewticket/" + str(ticket.id))
        elif(request.method == "GET"):
            return render(request, "user/ticket.html")
    else:
        return redirect('login')


def viewticket(request, id):
    print("----------> viewticket", id)
    if request.user.is_authenticated:
        status = False
        ticket = Ticket.objects.get(id=id)
        ticket_comments = Comment.objects.filter(object_id=id)
        context = {
            'data': {
                'ticket': ticket,
                'ticket_comments': ticket_comments
            }
        }
        return render(request, "user/viewticket.html", context)
    else:
        return redirect('login')


def new_comment(request, id):
    print("----------> new_comment", id)
    message = "Error"
    status = False
    if request.user.is_authenticated:
        if request.method == 'POST':
            cmnt = request.POST.get('comment')
            content_type_id = 14
            now = timezone.now()
            comment = Comment(comment=cmnt, content_type_id=14,
                              user=request.user, object_id=id, time=now)
            comment.save()
            message = "Ticket Added"
        status = True

        data = {
            'status': status,
            "msg": message,
            "comment": cmnt,
            "time": str(now),
            "first_name": comment.user.first_name
        }
    return JsonResponse(data)
