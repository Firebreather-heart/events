from django.shortcuts import render,redirect
from requests import delete
from .models import Attendee,Event,Mailing,Partner,Speaker
from .forms import AttendForm,EventForm,MailingForm,PartnerForm,SpeakerForm
from django.contrib import messages
from .custom import require_key

# Create your views here.

KEYS = ['evm_rmp102', 'evm_lfb345', 'evm_ayd666']

import smtplib
import ssl,threading
from .main import sendmail
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

# Define the transport variables
password = "jkadifnyyrpdryeb"    # Your app password goes here
sender = "lordfirebcorps@gmail.com"    # Your e-mail address

def register(request, link):
    event = Event.objects.get(link=link)
    if request.method == 'POST':
        form =  AttendForm(request.POST)
        if form.is_valid():
            cd  = form.cleaned_data
            fn = cd['f_name']
            ln = cd['l_name']
            mail = cd['email']
            event = cd['event']
            try: 
                form.save()
                messages.add_message(request, messages.SUCCESS, message = 'Registration Successfull')
            except:
                return messages.error(request, 'you have registered already')
            else:
                payload = f'''
                    Congrats, you have successfully registered for the event:
                    {str(event.theme).capitalize()}
                    You will recieve an email with information as regards the 
                    date, time and location.
                    Have a nice day!
                '''
                try:
                    sendmail(payload=payload, recipient=mail, subject='Event Registration', sender=sender, password=password,)
                except:
                    pass 
    else:
        form = AttendForm()
    return render(request, 'event_page.html', {'form': form, 'event':event})


def admin_key(request):
    key =  request.POST.get('key')
    if key in KEYS:
        request.session['key']=key 
        messages.success(request, 'Validation Successfull')
        return redirect(request.session.get('return_url'))
    else:
        messages.error(request, 'enter a valid key')
    return render(request, 'super.html')

@require_key
def create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print('saved')
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'create.html', {'form': form})

@require_key
def remove_event(request,link):
    to_del = Event.objects.get(link=link)
    to_del.delete()
    ev = Event.objects.order_by('date')
    return render(request, 'event.html', {'event':ev})
 

@require_key
def new_partner(request, link):
    if request.method == "POST":
        form = PartnerForm(request.POST, request.FILES)   
        if form.is_valid():
            form.save()     
        return redirect('event_detail', link=link)
    else:
        form = PartnerForm()
    ctx = {
        'form': form,
        'event': Event.objects.get(link=link)
    }
    return render(request, 'partner.html', ctx)

@require_key
def remove_partner(request,link,id):
    p = Partner.objects.get(id=id)
    p.delete()
    ev = Event.objects.get(link=link)
    partners = Partner.objects.filter(event = ev)
    speakers = Speaker.objects.filter(event=ev)
    ctx = {
        'event':ev,
        'partners':partners,
        'speakers':speakers,
    }
    return render(request, 'detail.html', ctx)
 
@require_key
def remove_speaker(request, link,id):
    p = Speaker.objects.get(id=id)
    p.delete()
    ev = Event.objects.get(link=link)
    partners = Partner.objects.filter(event = ev)
    speakers = Speaker.objects.filter(event=ev)
    ctx = {
        'event':ev,
        'partners':partners,
        'speakers':speakers,
    }
    return render(request, 'detail.html', ctx) 

@require_key
def new_speaker(request, link):
    if request.method == "POST":
        form = SpeakerForm(request.POST, request.FILES)   
        if form.is_valid():
            form.save()     
        return redirect('event_detail', link=link)
    else:
        form = SpeakerForm()
    ctx = {
        'form': form,
        'event': Event.objects.get(link=link)
    }
    return render(request, 'speaker.html', ctx)

@require_key
def events(request):
        ev = Event.objects.order_by('date')   
        return render(request, 'event.html', {'events':ev})    

@require_key
def event_detail(request, link):
    ev = Event.objects.get(link=link)
    partners = Partner.objects.filter(event = ev)
    speakers = Speaker.objects.filter(event=ev)
    ctx = {
        'event':ev,
        'partners':partners,
        'speakers':speakers,
    }
    return render(request, 'detail.html', ctx) 

@require_key
def edit_event(request, link):
    event = Event.objects.get(link=link)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_detail', link = link)
    else:
        form = EventForm(instance=event)
    return render(request, 'edit_event.html', {'form': form, 'event': event})

@require_key
def sendIv(request, link):
    event = Event.objects.get(link = link)
    attendee = event.attendee.all()
    print(attendee)
    return HttpResponse('working')