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
    event = forms.ModelChoiceField(queryset = Event.objects.order_by('date'))
    class Meta:
        model = Attendee
        fields = '__all__'
    
    def save(self, commit: bool = ...):
        speaker = super().save(commit=False)
        ev = self.cleaned_data['event']
        speaker.event = ev
        return super().save(commit=True)

class MailingForm(Mf):
    class Meta:
        model = Mailing
        fields = '__all__'
        
class SpeakerForm(Mf):
    event = forms.ModelChoiceField(queryset = Event.objects.order_by('date'))
    class Meta:
        model = Speaker
        fields = ['fn', 'bio','img']
    
    def save(self, commit: bool = ...):
        speaker = super().save(commit=False)
        ev = self.cleaned_data['event']
        speaker.event = ev
        return super().save(commit=True)
        

class PartnerForm(Mf):
    event = forms.ModelChoiceField(queryset = Event.objects.order_by('date'))
    class Meta:
        model = Partner
        fields = ['name', 'img']
    
    def save(self, commit: bool = ...):
        speaker = super().save(commit=False)
        ev = self.cleaned_data['event']
        speaker.event = ev
        return super().save(commit=True)