from datetime import datetime
from django.shortcuts import render,redirect
from requests import delete
from .models import Attendee,Event,Mailing,Partner,Speaker
from .forms import AttendForm,EventForm,MailingForm,PartnerForm,SpeakerForm
from django.contrib import messages
from .custom import require_key
from .tasks import send_mail_task
import time

# Create your views here.

KEYS = ['evm_rmp102', 'evm_lfb345', 'evm_ayd666']



def register(request, link):
    event = Event.objects.get(link=link)
    speakers = Speaker.objects.filter(event=event)
    partners = Partner.objects.filter(event=event)
    if request.method == 'POST':
        form =  AttendForm(request.POST)
        if form.is_valid():
            cd  = form.cleaned_data
            fn = cd['first_name']
            ln = cd['last_name']
            mail = cd['email']
            try: 
                Attendee.objects.create(first_name = fn, last_name= ln, email = mail, event = event)
                messages.add_message(request, messages.SUCCESS, message = 'Registration Successfull')
            except Exception as e:
                messages.add_message(request,messages.ERROR, message = 'you have registered already')
                print(e)
            else:
                payload = f'''
                    Congrats, you have successfully registered for the event:
                    {str(event.theme).capitalize()}
                    You will recieve an email with information as regards the 
                    date, time and location.
                    Have a nice day!
                '''
                task_result = send_mail_task.delay(payload=payload, recipient=mail, subject='Event Registration',filepath=None )
                if task_result.successful():
                    print(f'Reg successful')
                else:
                    print(f'Error sending reg msg: {task_result.result}')
                return render(request, 'success.html', {'event':event})

    else:
        form = AttendForm()
    return render(request, 'event_page.html', {'form': form, 'event':event, 'partners':partners, 'speakers':speakers})


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
    event = Event.objects.get(link=link)
    if request.method == "POST":
        form = PartnerForm(request.POST, request.FILES)   
        if form.is_valid():
            cd = form.cleaned_data
            name = cd['name']
            img = cd['img']
            event  = event
            try: 
                Partner.objects.create(name = name, img = img,  event = event)
                messages.add_message(request, messages.SUCCESS, message = 'Partner Added Successfully')
            except Exception as e:
                messages.add_message(request,messages.ERROR, message = 'An error occured, retry')
                print(e)
        return redirect('event_detail', link=link)
    else:
        form = PartnerForm()
    ctx = {
        'form': form,
        'event': event
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
    event = Event.objects.get(link=link)
    if request.method == "POST":
        form = SpeakerForm(request.POST, request.FILES)   
        if form.is_valid():
            cd = form.cleaned_data
            name = cd['full_name']
            img = cd['img']
            bio = cd['bio']
            event  = event
            try: 
                Speaker.objects.create(full_name = name, img= img,  event = event, bio=bio)
                messages.add_message(request, messages.SUCCESS, message = 'Partner Added Successfully')
            except Exception as e:
                messages.add_message(request,messages.ERROR, message = 'An error occured, retry')
                print(e) 
        return redirect('event_detail', link=link)
    else:
        form = SpeakerForm()
      #  form = form.add_link(link)
    ctx = {
        'form': form,
        'event': event
    }
    return render(request, 'speaker.html', ctx)

@require_key
def events(request):
        ev = Event.objects.filter(date__gte = datetime.today()).order_by('date')   
        return render(request, 'event.html', {'events':ev})    

@require_key
def event_detail(request, link):
    ev = Event.objects.get(link=link)
    partners = Partner.objects.filter(event = ev)
    speakers = Speaker.objects.filter(event= ev)
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
    if request.method == 'POST':
        event = Event.objects.get(link = link)
        attendee = event.attendee.all()
        subject = request.POST.get('sub')
        content = request.POST.get('cont')
        for person in attendee:
            recipient = str(person.email)
            task_result = send_mail_task.delay(
                payload = content, 
                recipient = recipient,
                subject = subject,
                filepath = None,
            )
            if task_result.successful():
                print(f'Invitation sent to {person.f_name} ({recipient})')
            else:
                print(f'Error sending invitation to {person.f_name} ({recipient}): {task_result.result}')
            return(redirect('event_detail', link=link))

    return render(request, 'email.html')