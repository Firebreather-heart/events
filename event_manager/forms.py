from django.forms import ModelForm as Mf
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
        fields = '__all__'

    def add_link(self, link):
        self.link = link
        return self 
    
    def save(self, commit: bool = ...):
        attendee = super().save(commit=False)
        event = Event.objects.get(link=self.link)
        attendee.event = event
        return super().save(commit=True)

class MailingForm(Mf):
    class Meta:
        model = Mailing
        fields = '__all__'
        
class SpeakerForm(Mf):
    #event = forms.ModelChoiceField(queryset = Event.objects.order_by('date'))
    class Meta:
        model = Speaker
        fields = ['fn', 'bio','img']
    
    def add_link(self, link):
        self.link = link
        return self 
    
    def save(self, commit: bool = ...):
        speaker = super().save(commit=False)
        event = Event.objects.get(link=self.link)
        speaker.event = event
        return super().save(commit=True)
        

class PartnerForm(Mf):
    #event = forms.ModelChoiceField(queryset = Event.objects.order_by('date'))
    class Meta:
        model = Partner
        fields = ['name', 'img']
    
    def add_link(self, link):
        self.link = link
        return self 
    
    def save(self, commit: bool = ...):
        speaker = super().save(commit=False)
        event = Event.objects.get(link=self.link)
        speaker.event = event
        return super().save(commit=True)