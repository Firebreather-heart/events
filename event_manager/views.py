from django.shortcuts import render,redirect
from .models import Attendee,Event,Mailing,Partner,Speaker
from .forms import AttendForm,EventForm,MailingForm,PartnerForm,SpeakerForm
# Create your views here.

def create(request):
    if request.method == "POST":
        form = EventForm(data = request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'create.html',{'form':form})

def new_partner(request):
    if request.method == "POST":
        form = PartnerForm(data = request.POST)   
        if form.is_valid():
            form.save()     


def events(request):
        ev = Event.objects.all()    
        return render(request, 'event.html', {'events':ev})     