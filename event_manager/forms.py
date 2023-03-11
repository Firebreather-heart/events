from django.forms import ModelForm as Mf
from django import forms
from .models import Event,Attendee,Mailing, Speaker,Partner

class EventForm(Mf):
    class Meta:
        model = Event
        fields = '__all__'
       
class AttendForm(Mf):
    event = forms.ModelChoiceField(queryset = Event.objects.order_by('date'))
    class Meta:
        model = Attendee
        fields = '__all__'

class MailingForm(Mf):
    class Meta:
        model = Mailing
        fields = '__all__'
        
class SpeakerForm:
    event = forms.ModelChoiceField(queryset = Event.objects.order_by('date'))
    class Meta:
        model = Speaker
        fields = '__all__'

class PartnerForm:
    event = forms.ModelChoiceField(queryset = Event.objects.order_by('date'))
    class Meta:
        model = Partner
        fields = '__all__'