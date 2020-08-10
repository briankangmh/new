# django
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.db.models import F
from django.db.models import Q
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

# python
from decimal import Decimal
import time
import calendar
from datetime import datetime, timedelta

# models
from payment.models import WalletTransactions, TxCommission, PaymentTransactions
from users.models import UserProfileInfo
from tutee.models import ViewAnswer, Question
from tutor.models import Answer
from . import appenums

# Create your views here.


def credit(user, tx_reason, qid, aid, from_user_id, to_user_id, status, amount):
    now = timezone.now()
    tx_type = 'Credit'
    credit_user = User.objects.get(id=to_user_id)
    tx = WalletTransactions(
        user=credit_user, tx_reason=tx_reason, aid=aid, qid=qid, from_user_id=from_user_id, to_user_id=to_user_id,
        tx_type=tx_type, status=status, amount=Decimal(amount), date_updated=now)
    tx.save()
    update_wallet_balance(to_user_id, amount, tx_type)
    return True


def credit_admin(user, tx_reason, qid, aid, from_user_id, to_user_id, status, amount):
    now = timezone.now()
    tx_type = 'Credit'
    credit_user = User.objects.get(id=to_user_id)
    tx = WalletTransactions(
        user=credit_user, tx_reason=tx_reason, aid=aid, qid=qid, from_user_id=from_user_id, to_user_id=to_user_id,
        tx_type=tx_type, status=status, amount=Decimal(amount), date_updated=now)
    tx.save()
    return True


def debit(user, tx_reason, qid, aid, from_user_id, to_user_id, status, amount):
    now = timezone.now()
    tx_type = 'Debit'
    tx = WalletTransactions(
        user=user, tx_reason=tx_reason, aid=aid, qid=qid, from_user_id=from_user_id, to_user_id=to_user_id,
        tx_type=tx_type, status=status, amount=Decimal(amount), date_updated=now)
    tx.save()
    update_wallet_balance(from_user_id, amount, tx_type)
    return True


def update_wallet_balance(user_id, amount, tx_type):
    print(user_id)
    user_profile = UserProfileInfo.objects.get(user_id=user_id)
    if tx_type == 'Credit':
        UserProfileInfo.objects.filter(user_id=user_id).update(
            wallet_balance=Decimal(user_profile.wallet_balance) + Decimal(amount))
        return Decimal(user_profile.wallet_balance) + Decimal(amount)
    elif tx_type == 'Debit':
        UserProfileInfo.objects.filter(user_id=user_id).update(
            wallet_balance=Decimal(user_profile.wallet_balance) - Decimal(amount))
        return Decimal(user_profile.wallet_balance) - Decimal(amount)


def make_payment(request):
    print("-------------> make_payment")
    message = "Payment Failed"
    status = False
    now = timezone.now()
    if request.user.is_authenticated:
        if request.method == 'POST':
            amount = request.POST.get('amount')
            if float(amount) > float(request.user.userprofileinfo.wallet_balance):
                data = {
                    'status': status,
                    "msg": 'Insuffucient Wallet Balance'
                }
                return JsonResponse(data)
            tx_reason = request.POST.get('tx_reason')
            question_id = request.POST.get('question_id')
            answer_id = request.POST.get('answer_id')
            from_user_id = request.user.id
            to_user_id = request.POST.get('to_user_id')
            print(tx_reason, question_id, answer_id)
            status = '0'
            tx_comm = TxCommission.objects.get(txc_type="default")
            print(tx_comm.percent)
            credit_amount_after_txc = float(
                amount) - (float(amount) * float(tx_comm.percent) / 100)
            print(credit_amount_after_txc)
            txc_amount = float(amount) * float(tx_comm.percent) / 100
            print(txc_amount)
            if debit(request.user, tx_reason, question_id, answer_id, from_user_id, to_user_id, status, amount):
                credit_status = credit(request.user, tx_reason, question_id, answer_id,
                                       from_user_id, to_user_id, status, credit_amount_after_txc)
                print("credit_status", credit_status)
                txc_credit_status = credit_admin(
                    request.user, tx_reason, question_id, answer_id, to_user_id, 1, status, txc_amount)
                print("txc_credit_status", txc_credit_status)
                if(tx_reason == "Answer"):
                    question = Question.objects.get(id=question_id)
                    view_answer = ViewAnswer(user=request.user, qid=question_id,
                                             qtitle=question.title, view_status='1', view_mode='1')
                    view_answer.save()
            message = "Payment Success"
            status = True

    data = {
        'status': status,
        "msg": message
    }
    return JsonResponse(data)


def active_chat_session(request, qid):
    print("-------------> active_chat_session", qid)
    message = "Failed"
    status = False
    now = timezone.now()
    if request.user.is_authenticated:
        if request.method == 'GET':
            # time_threshold = datetime.now() - timedelta(hours=1)
            time_threshold = timezone.now() - timedelta(hours=1)

            print(time_threshold)
            active_sessions = WalletTransactions.objects.filter(
                qid=qid, user=request.user, date_created__gt=time_threshold)
            print("active_sessions", active_sessions.count())
            message = "Success"
            status = True
            data = {
                'status': status,
                "msg": message,
                "active_sessions": serializers.serialize('json', active_sessions),
            }

            return JsonResponse(data)

    data = {
        'status': status,
        "msg": message
    }
    return JsonResponse(data)


def ad_watched(request):
    print("-------------> ad_watched")
    message = "Failed"
    status = False
    now = timezone.now()
    if request.user.is_authenticated:
        if request.method == 'POST':
            tx_reason = request.POST.get('tx_reason')
            qid = request.POST.get('qid')
            question = Question.objects.get(id=qid)
            view_answer = ViewAnswer(user=request.user, qid=qid, qtitle=question.title,
                                     view_status='1', view_mode='0')
            view_answer.save()
            message = "Success"
            status = True

    data = {
        'status': status,
        "msg": message
    }
    return JsonResponse(data)


def transaction_history(request):
    print("-------------> transaction_history")
    if request.user.is_authenticated:
        transactions = WalletTransactions.objects.filter(
            user_id=request.user.id)
        pay_transactions = PaymentTransactions.objects.filter(
            user_id=request.user.id)
        context = {
            'data': {
                'transactions': transactions,
                'pay_transactions': pay_transactions,
            }
        }
        return render(request, "payment/transaction_history.html", context)
    else:
        return redirect('index')


def add_money_to_wallet(request):
    print("-------------> add_money_to_wallet")
    resp_message = "Failed"
    resp_status = False
    if request.user.is_authenticated:
        pay_mode = request.POST.get('pay_mode')
        amount = request.POST.get('amount')
        currency_code = request.POST.get('currency_code')
        payer_email = request.POST.get('payer_email')
        payer_id = request.POST.get('payer_id')
        payer_name = request.POST.get('payer_name')
        status = request.POST.get('status')
        txid = request.POST.get('txid')
        create_time = request.POST.get('create_time')
        update_time = request.POST.get('update_time')
        pay_tx = PaymentTransactions(
            user=request.user, pay_mode=pay_mode, amount=amount, currency_code=currency_code, payer_email=payer_email,
            payer_id=payer_id, payer_name=payer_name, status=status, txid=txid, create_time=create_time,
            update_time=update_time)
        pay_tx.save()
        wallet_balance = update_wallet_balance(
            request.user.id, amount, 'Credit')
        resp_message = "Success"
        resp_status = True

    data = {
        'status': resp_status,
        'msg': resp_message,
        'wallet_balance': wallet_balance
    }
    return JsonResponse(data)
