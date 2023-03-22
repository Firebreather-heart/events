from django import forms
from .models import Event,Attendee,Mailing, Speaker,Partner



class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['theme', 'date', 'start', 'end', 'img', 'desc', 'link', 'location']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start': forms.TimeInput(attrs={'type': 'time'}),
            'end': forms.TimeInput(attrs={'type': 'time'}),
        }
       
class AttendForm(forms.ModelForm):
    class Meta:
        model = Attendee
        fields = ['first_name', 'last_name', 'email']

class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = '__all__'
        
class SpeakerForm(forms.ModelForm):
    class Meta:
        model = Speaker
        fields = ['full_name', 'bio','img']
    
class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = ['name', 'img']
    