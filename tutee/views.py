# python core
import calendar
import json
import time
from decimal import Decimal

# websocket
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# django
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.db.models import Avg, Max, Min, Sum
from django.forms.models import modelformset_factory
from django.http import HttpResponse, JsonResponse, QueryDict
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

# twilio
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant
from twilio.rest import Client


# models
from tutor.models import Answer, TutorFeedback
from users.models import Subject, UserProfileInfo
from payment.models import QuestionPrice
from tutee.models import Question, ViewAnswer
from .forms import QuestionForm, QuestionFullForm, UserProfileInfoForm


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        questions = Question.objects.filter(
            user_id=request.user.id).order_by('date_created')[:6]
        tutors = UserProfileInfo.objects.filter(
            ugroup=1, status=1, ws_status=1).order_by('-rating')[:5]
        subjects = Subject.objects.all()

        context = {
            'data': {
                'tutors': tutors,
                'questions': questions,
                'subjects': subjects,
            }
        }
        return render(request, "tutee/index.html", context)
    else:
        return redirect('index')


def profile(request):
    data = ''
    if request.user.is_authenticated:
        if request.method == 'POST':
            gender = request.POST['gender']
            classg = request.POST['classg']
            if request.FILES:
                myfile = request.FILES['photo']
                fs = FileSystemStorage()
                upfilename = 'profile' + str(request.user.id)
                filename = fs.save(upfilename, myfile)
                uploaded_file_url = fs.url(filename)
                UserProfileInfo.objects.filter(user_id=request.user.id).update(
                    gender=gender, photo=filename, classg=classg)
            else:
                UserProfileInfo.objects.filter(user_id=request.user.id).update(
                    gender=gender, classg=classg)
            data = 'success'
        if 'http' in str(request.user.userprofileinfo.photo.url):
            profile_pic = request.user.userprofileinfo.photo
        else:
            profile_pic = request.user.userprofileinfo.photo.url
            context = {'profile_pic': profile_pic, 'success': data}
        return render(request, "tutee/profile.html", context)
    else:
        return redirect('index')


def manage_file_upload(f):
    with open('media/questions/' + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def question_file(request):
    print("----------------------->", "question_file")

    if request.method == 'POST':
        form = QuestionFullForm(request.POST, request.FILES)
        attachments = request.FILES.getlist('attachments')
        print(form)

        if form.is_valid():
            print("---------------> valid")
            title = request.POST['title']
            subject = "Maths"
            desc = request.POST['desc']
            remarks = request.POST['remarks']
            difficulty = request.POST['difficulty']
            ts = calendar.timegm(time.gmtime())
            qid = str(request.user.id) + str(ts)
            status = "0"
            now = timezone.now()
            question = Question(user=request.user, title=title, subject=subject, desc=desc, remarks=remarks,
                                difficulty=difficulty, qid=qid, status=status, date_updated=now)
            question.save()
            for f in attachments:
                print(f)

            return redirect('index')
    if request.method == "GET":
        subject = Subject.objects.all()
        context = {
            'data': {
                'subject': subject,
            }
        }
        return render(request, "tutee/question.html", context)
    return redirect('index')


def publish_question(question):
    channel_layer = get_channel_layer()
    top_records = (UserProfileInfo.objects
                   .order_by('-rating')
                   .filter(ugroup="1", status="1", ws_status="1", subject__icontains=question.subject))

    # active_tutors = UserProfileInfo.objects.filter(
    #     ugroup="1", status="1", ws_status="1", subject__icontains=question.subject)

    top_tutors = UserProfileInfo.objects.filter(
        ugroup="1", status="1", ws_status="1", subject__icontains=question.subject).order_by('-rating')[:5]

    for tutor in top_tutors:
        async_to_sync(channel_layer.send)(tutor.channel_name, {
            "type": "new_question",
            "event": "New Question",
            "qid": question.id,
            "title": question.title,
            "subject": question.subject,
            "desc": question.desc,
            "channel_name": tutor.channel_name})
    # async_to_sync(channel_layer.group_send)(
    #     "active", {"type": "user_active",
    #             "event": "New Question",
    #             "qid": qid,
    #             "title": title,
    #             "subject": subject,
    #             "desc": desc})


def question(request):
    print("----------------------->", "question")

    if request.user.is_authenticated:
        # add new question service
        if(request.method == "POST"):
            title = request.POST['title']
            subject = request.POST['subject']
            desc = request.POST['desc']
            remarks = request.POST['remarks']
            difficulty = request.POST['difficulty']
            price = QuestionPrice.objects.get(subject='default').price
            status = "0"
            now = timezone.now()
            if request.FILES:
                attachments = request.FILES.getlist('attachments')
                attachment_names = []
                for i, f in enumerate(attachments):
                    # manage_file_upload(f)
                    fs = FileSystemStorage()
                    upfilename = 'q' + '_' + str(f.name)
                    filename = fs.save(upfilename, f)
                    attachment_names.append(filename)
                    uploaded_file_url = fs.url(filename)
                    print(uploaded_file_url)

                question = Question(user=request.user, title=title, subject=subject, desc=desc, remarks=remarks, difficulty=difficulty,
                                    price=price, attachment=",".join(attachment_names), status=status, date_updated=now)
            else:
                question = Question(user=request.user, title=title, subject=subject, desc=desc, remarks=remarks,
                                    difficulty=difficulty, price=price, status=status, date_updated=now)
            question.save()
            publish_question(question)
            context = {
                'data': {
                    'data': question,
                    'success': ' Added'
                }
            }
            return redirect("question/" + str(question.id), context)
        if request.method == "GET":
            # new question form page
            subject = Subject.objects.all()
            context = {
                'data': {
                    'subject': subject,
                }
            }
            return render(request, "tutee/question.html", context)
        else:
            return redirect('index')
    else:
        return redirect('index')


def view_question(request, qid):
    print("----------------------->", "view_question", qid)
    req_status = ''
    if request.user.is_authenticated:
        if request.method == 'GET':
            data = Question.objects.get(id=qid)
            if(data.status == '2'):
                answer = Answer.objects.get(qid=qid)
                data.answer_id = answer.id
            req_status = 'success'
            context = {'data': data, 'success': req_status}
            return render(request, "tutee/answer.html", context)
    else:
        return redirect('index')


def tutor_feedback(request, aid):
    print("----------------------->", "tutor_feedback", aid)
    now = timezone.now()
    message = "Error"
    status = False
    data = {}
    if request.user.is_authenticated:
        if request.method == 'POST':
            question_id = request.POST.get('question_id')
            remarks = request.POST.get('remarks')
            rating = request.POST.get('rating')
            tutor_id = request.POST.get('tutor_id')

            existing_tf = TutorFeedback.objects.filter(
                aid=aid, user_id=request.user.id)
            if(existing_tf.count() == 0):
                feedback = TutorFeedback(user=request.user, tutor_id=tutor_id, aid=aid, qid=question_id,
                                         remarks=remarks, rating=Decimal(rating), date_updated=now)
                feedback.save()
                message = "Feedback Added"
            else:
                existing_tf.update(
                    remarks=remarks, rating=Decimal(rating), date_updated=now)
                message = "Feedback Updated"

            feedbacks = TutorFeedback.objects.filter(tutor_id=tutor_id)
            if feedbacks.count() > 0:
                avg_rating = Decimal(feedbacks.aggregate(
                    Avg('rating'))['rating__avg'])
                UserProfileInfo.objects.filter(
                    user_id=tutor_id).update(rating=avg_rating)

            status = True

            data = {
                'status': status,
                "msg": message
            }
    return JsonResponse(data)


def view_answer(request, qid):
    print("----------------------->", "view_answer", qid)

    message = ""
    status = False
    answered = False
    question = Question.objects.get(id=qid)
    view_answer = ViewAnswer.objects.filter(qid=qid, user_id=request.user.id)
    if view_answer.count() == 0:
        message = "Pay or Watch ad to view answer"
        status = False
        data = {
            'status': status,
            "msg": message,
        }
        return JsonResponse(data)
    else:
        status = True
        if question.status == '2':
            message = "Question Answered"
            answered = True
            answer = Answer.objects.get(qid=qid)
            feedback = TutorFeedback.objects.filter(aid=answer.id)
            data = {
                'status': status,
                "msg": message,
                "answer": serializers.serialize('json', [answer, ]),
                "feedback": serializers.serialize('json', feedback),
                "answered": answered
            }
            return JsonResponse(data)
        else:
            message = "Question Not Answered Yet"
            answered = False
            data = {
                'status': status,
                "msg": message,
                "answered": answered
            }
            return JsonResponse(data)


def delete_question(request, qid):
    print("----------------------->", "delete_question", qid)
    message = "Error"
    status = False

    if request.user.is_authenticated:
        query = Question.objects.filter(
            user_id=request.user.id, id=qid).delete()
        message = "Question Deleted Successfully"
        status = True

    data = {
        'status': status,
        "msg": message,
    }
    return JsonResponse(data)


def tutee_question_history(request):
    if request.user.is_authenticated:
        questions = Question.objects.filter(user_id=request.user.id)
        answers = ViewAnswer.objects.filter(user_id=request.user.id)
        context = {
            'data': {
                'questions': questions,
                'answers': answers,
            }
        }
        return render(request, "tutee/history.html", context)
    else:
        return redirect('index')


def search_question(request):
    print("----------------------->", "search_question")

    if request.user.is_authenticated:
        if request.method == 'POST':
            search_query = request.POST['search_query']
            subject = request.POST['subject']
            questions = Question.objects.filter(
                title__icontains=search_query, subject=subject)
            tutors = UserProfileInfo.objects.filter(ugroup=1, status=1)
            subjects = Subject.objects.all()
            context = {
                'data': {
                    'tutors': tutors,
                    'questions': questions,
                    'subjects': subjects
                }
            }
            return render(request, "tutee/index.html", context)
        else:
            return redirect('index')
    else:
        return redirect('index')


def view_tutor(request, id):
    print("----------------------->", "view_tutor", id)

    if request.user.is_authenticated:
        tutor = UserProfileInfo.objects.get(
            user_id=id)  # group 1 is tutor, 2 is tutee
        context = {
            'data': {
                'tutor': tutor
            }
        }

    return render(request, "tutee/tutor-view.html", context)


def find_tutor(request):
    print("---------------------->", "find_tutor")
    if request.user.is_authenticated:
        if request.method == 'POST':
            subject = request.POST['subject']
            # active = request.POST['active']
            subjects = Subject.objects.all()
            if subject == 'All':
                subjects = Subject.objects.all()
            else:
                tutors = UserProfileInfo.objects.filter(
                    ugroup="1", status="1", subject__icontains=subject)
                context = {
                    'data': {
                        'tutors': tutors,
                        'subjects': subjects,
                    }
                }
            return render(request, "tutee/findtutor.html", context)
        else:
            subjects = Subject.objects.all()
            context = {
                'data': {
                    'subjects': subjects,
                }
            }
            return render(request, "tutee/findtutor.html", context)
    else:
        return redirect('index')
