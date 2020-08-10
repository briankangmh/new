Workspace Setup

Install Anaconda
https://docs.anaconda.com/anaconda/install/windows/

```console
conda create --name officehours python=3.6

conda activate officehours

cd git/officehours

pip install -r requirements.txt

```

Start Server commands

```console
python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver
```

login to admin
add tx_comissions -> 10%
add question_prics -> 2
add subjects -> Maths, Physics, English
to set email domain
https://stackoverflow.com/questions/5812985/django-password-reset-email-subject-line-contains-example-com

    ugroup
        1-tutor
        2-tutee

    question 
        status
        0-posted
        1-accepted
        2-answered

        view_Status
        0-view diaabled
        1-view enabled

        question_type
        0-paid
        1-free

    answer 
        status
        0-accepted
        1-answered

    ViewAnswer
        view_status
        1-enabled

        view_mode
        0-ad
        1-payment

Wallet Transactions

    tx_reason
        ANSW = "Answer"
        CHAT = "Chat"
        ACHAT = "Achat"
        VCHAT = "Vchat"

    tx_type
        CR = "Credit"
        DB = "Debit"

    profile info status
        0-offline
        1-online
        2-away

    user status
        ws_status = django channels connection flag
        status = Manual (on or off)

    ticket
        status
        0 - created
        1 - accepted
        2 - resolving
        3 - closed


# prod

    debug
    allowed_host
    database
    channel_layers

# settings

    timezone
    price all
    comission all
    create root user
    remove comment comission
