from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth import get_user_model

from .forms import NewUserForm
from .models import Message, Profile
# Create your views here.
def home(request):
    current_user = request.user
    users = User.objects.order_by('?').exclude(id=current_user.id)[:10]
    context = {
        'users': users,
    }
    return render(request, 'home.html', context)

def user_login(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.warning(request, "error while login in.")

    return render(request, 'autho/user_login.html')

def email_login(request):
    if request.method == 'POST':
        email = request.POST["email"]
        password = request.POST["password"]
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user is not None:
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
        messages.warning(request, "error while login in.")

    return render(request, 'autho/email_login.html')

def user_logout(request):
    logout(request)
    return redirect('/')

def user_register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                messages.error(request, 'This email is already registered.')
                return redirect('register')
            else:
                form.save()
                messages.success(request, 'Registration successful. You can now log in.')
                return redirect('/')
    else:
        form = NewUserForm()
    
    context = {
        'form': form,
    }
    return render(request, 'autho/user_register.html', context)

def dashboard(request):
    return render(request, 'users/dashboard.html')

def profile(request, username):
    user = get_object_or_404(User, username=username)
    context = {
        'user': user,
    }
    return render(request, 'users/profile.html', context)

@login_required
def inbox(request):
    user = request.user
    messages = Message.get_message(user=user)
    active_direct = None
    directs = None

    if messages:
        message = messages[0]
        active_direct = message['user'].username
        directs = Message.objects.filter(user=user, reciepient=message['user'])
        directs.update(is_read=True)

        for message in messages:
            if message['user'].username == active_direct:
                message['unread'] = 0

    last_login = user.last_login
    current_time = timezone.now()
    if current_time - last_login < timezone.timedelta(minutes=5):
        is_active = True
    else:
        is_active = False

    context = {
        'directs': directs,
        'active_direct': active_direct,
        'messages': messages,
        'is_active': is_active,
    }
    return render(request, 'users/inbox.html', context)

@login_required
def directs(request, username):
    sending_message_to = get_object_or_404(User, username=username)
    user = request.user
    messages = Message.get_message(user=user)
    active_direct = username
    directs = Message.objects.filter(user=user, reciepient__username=username)
    directs.update(is_read=True)

    last_login = user.last_login
    current_time = timezone.now()
    if current_time - last_login < timezone.timedelta(minutes=5):
        is_active = True
    else:
        is_active = False

    for message in messages:
        if message['user'].username == username:
            message['unread'] = 0

    if request.user.username == username:
        return redirect('/')

    context = {
        'sending_message_to': sending_message_to,
        'directs': directs,
        'active_direct': active_direct,
        'messages': messages,
        'is_active': is_active,
    }
    return render(request, 'users/directs.html', context)

def send_message_ajax(request):
    if request.method == 'POST':
        from_user = request.user
        to_user_username = request.POST.get('to_user')
        body = request.POST.get('body')
        file = request.FILES.get('file')

        to_user = User.objects.get(username=to_user_username)
        Message.send_message(from_user, to_user, body, file)

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'failed'})

def get_messages_ajax(request, username):
    user = request.user
    sending_message_to = get_object_or_404(User, username=username)
    directs = Message.objects.filter(user=user, reciepient__username=username)
    directs.update(is_read=True)

    messages = []
    for direct in directs:
        message_data = {
            'sender': direct.sender.username,
            'body': direct.body,
            'date': direct.date.strftime('%Y-%m-%d %H:%M:%S'),
        }
        if direct.file:
            message_data['file_url'] = direct.file.url
        messages.append(message_data)

    # print(messages)  # Add this line to print messages data
    return JsonResponse({'messages': messages})


