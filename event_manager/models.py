from django.db import models

# Create your models here.

class Event(models.Model):
    theme = models.CharField(max_length = 250)
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField(null =True, blank = True)
    img = models.ImageField(upload_to='media', blank= False)
    desc = models.TextField(max_length= 5000)
    link = models.CharField(max_length=12)
    
class Attendee(models.Model):
    f_name = models.CharField(max_length=50,)
    l_name = models.CharField(max_length= 50)
    email = models.EmailField(max_length = 100)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="event")

class Mailing(models.Model):
    mail = models.EmailField(max_length= 50)
 

    
    
class Speaker(models.Model):
    fn = models.CharField(max_length = 100)
    img = models.ImageField(upload_to='media/speakers', blank = True, null = True)
    bio = models.TextField(max_length = 1000)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name = "speakers")

class Partner(models.Model):
    name = models.CharField(max_length= 100)
    img = models.ImageField(upload_to = "media/partners", )
    event = models.ForeignKey(Event, on_delete = models.CASCADE, related_name='partner')