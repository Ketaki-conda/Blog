from django.shortcuts import render
from blog.settings import EMAIL_HOST_USER
from . import forms
from .models import SubscribeModel
from django.core.mail import send_mail
import datetime

# Create your views here.
#DataFlair #Send Email
def subscribe(request):
    sub = forms.Subscribe()
    if request.method == 'POST':
        sub = forms.Subscribe(request.POST)
        if(sub.is_valid()):
            a = SubscribeModel(email = str(sub['Email'].value()),created_date = datetime.datetime.now())
            a.save()
        subject = 'Welcome to OurBlog'
        message = 'We are blessed to serve you!'
        recepient = str(sub['Email'].value())
        send_mail(subject,
            message, EMAIL_HOST_USER, [recepient], fail_silently = False)
        return render(request, 'subscribe/success.html', {'recepient': recepient})
    return render(request, 'subscribe/index.html', {'form':sub})

