# django
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.core import serializers
from django.utils import timezone
from django.db.models import Avg, Max, Min, Sum

# models
from users.models import UserProfileInfo, Subject, TimeOnline
from tutee.models import Question
from tutor.models import Answer, TutorFeedback
from .forms import UserProfileInfoForm

# python core
import time
import calendar
from datetime import date
import datetime

# Create your views here.


def index(request):
    if request.user.is_authenticated:
        questions = Question.objects.filter(accepted_by=request.user.id)
        total_time_online = TimeOnline.objects.filter(user_id=request.user.id)
        today = date.today()
        today_time_online = TimeOnline.objects.filter(
            user_id=request.user.id, date=today)
        total_mins = 0
        today_mins = 0
        if total_time_online.count() > 0:
            total_mins = total_time_online.aggregate(Sum('time_mins'))[
                'time_mins__sum']
            print(total_mins)
        if today_time_online.count() > 0:
            today_mins = today_time_online.aggregate(Sum('time_mins'))[
                'time_mins__sum']
            print(today_mins)
        context = {
            'data': {
                'questions': questions,
                'total_mins': str(datetime.timedelta(seconds=total_mins)),
                'today_mins': str(datetime.timedelta(seconds=today_mins)),
                'today_secs': today_mins
            }
        }
        return render(request, "tutor/index.html", context)
    else:
        return redirect('index')


def profile(request):
    data = ''
    if request.user.is_authenticated:
        if request.method == 'POST':
            gender = request.POST['gender']
            subject = request.POST['expertise']
            if request.FILES:
                myfile = request.FILES['photo']
                fs = FileSystemStorage()
                upfilename = 'profile' + str(request.user.id)
                filename = fs.save(upfilename, myfile)
                uploaded_file_url = fs.url(filename)
                UserProfileInfo.objects.filter(user_id=request.user.id).update(
                    gender=gender, photo=filename, subject=subject)
            else:
                UserProfileInfo.objects.filter(
                    user_id=request.user.id).update(gender=gender, subject=subject)
            data = 'success'
        if 'http' in str(request.user.userprofileinfo.photo.url):
            profile_pic = request.user.userprofileinfo.photo
        else:
            profile_pic = request.user.userprofileinfo.photo.url

        subject_list = Subject.objects.all()
        context = {'profile_pic': profile_pic,
                   'success': data, 'subject': subject_list}
        return render(request, "tutor/profile.html", context)
    else:
        return redirect('index')


def view_question(request, qid):
    print("----------------------->", "view_question", qid)
    req_status = ''
    if request.user.is_authenticated:
        if request.method == 'GET':
            data = Question.objects.get(id=qid)
            req_status = 'success'
            context = {'data': data, 'success': req_status}
            return render(request, "tutor/answer.html", context)
    else:
        return redirect('index')


def add_answer(request, qid):
    print("---------------------->", "add_answer", qid)
    req_status = ''
    if request.user.is_authenticated:
        if request.method == 'POST':
            print("post")
            answer = request.POST['answer']
            remarks = request.POST['remarks']
            now = timezone.now()
            print('tutor---->', "attachments")
            if request.FILES:
                print('tutor---->', "attachments")
                attachments = request.FILES.getlist('attachments')
                attachment_names = []
                for i, f in enumerate(attachments):
                    print('tutor file name--->', f.name)
                    # myfile = request.FILES['photo']
                    fs = FileSystemStorage()
                    upfilename = 'a' + '_' + str(qid) + '_' + str(f.name)
                    filename = fs.save(upfilename, f)
                    attachment_names.append(filename)
                    uploaded_file_url = fs.url(filename)
                    print('tutor---->', uploaded_file_url)
                answer = Answer(user=request.user, answer=answer, remarks=remarks, attachment=",".join(
                    attachment_names), qid=qid, date_updated=now, status='1')
            else:
                answer = Answer(user=request.user, answer=answer, remarks=remarks,
                                qid=qid, date_updated=now, status='1')
            answer.save()
            Question.objects.filter(id=qid).update(status=2)
            question = Question.objects.get(id=qid)
            context = {
                'data': {
                    'question': question,
                    'answer': answer,
                    'success': ' Added'
                }
            }
            return redirect("/tutor/answer/" + str(qid), context)
    else:
        return redirect('index')


def accept_question(request, qid):
    print("---------------------->", "accept_question", qid)
    message = ""
    status = False
    question = Question.objects.get(id=qid)
    if question.status == "0":
        message = "Question Accepted Successfully"
        status = True
        Question.objects.filter(id=qid).update(
            status=1, accepted_by=request.user.id)
    elif question.status == "1":
        message = "Question Already Accepted"
        status = False
    questions = Question.objects.filter(accepted_by=request.user.id)
    questions_json = serializers.serialize('json', questions)

    data = {
        'status': status,
        'qid': qid,
        "msg": message,
        "accepted_questions": questions_json
    }
    return JsonResponse(data)


def view_answer(request, qid):
    print("---------------------->", "view_answer", qid)
    if request.user.is_authenticated:
        answer = Answer.objects.get(qid=qid)
        question = Question.objects.get(id=qid)

        context = {
            'data': {
                'question': question,
                'answer': answer,
            }
        }
        return render(request, "tutor/view_answer.html", context)
    else:
        return redirect('index')


def tutor_history(request):
    if request.user.is_authenticated:
        answers = Answer.objects.filter(user_id=request.user.id)
        context = {
            'data': {
                'answers': answers,
            }
        }
        return render(request, "tutor/history.html", context)
    else:
        return redirect('index')


def status(request, val):
    if request.user.is_authenticated:
        message = "Signed In Successfully"
        status = True
        UserProfileInfo.objects.filter(user_id=request.user).update(status=val)

    data = {
        'status': status,
        "msg": message,
    }
    return JsonResponse(data)


def update_answer(request, aid):
    print("---------------------->", "update_answer", aid)
    message = "Error"
    status = False
    if request.user.is_authenticated:
        if request.method == 'POST':
            answer = request.POST.get('answer')
            remarks = request.POST.get('remarks')
            tutoranswer = Answer.objects.filter(
                id=aid).update(remarks=remarks, answer=answer)
            message = "Answer Updated Successfully"
            status = True
    data = {
        'status': status,
        "msg": message,
    }
    return JsonResponse(data)


def delete_answer(request, aid):
    print("----------------------->", "delete_answer", aid)
    message = "Error"
    status = False

    if request.user.is_authenticated:
        query = Answer.objects.filter(user_id=request.user.id, id=aid).delete()
        message = "Answer Deleted Successfully"
        status = True

    data = {
        'status': status,
        "msg": message,
    }
    return JsonResponse(data)
