from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BasePerson(models.Model):
    user = models.OneToOneField(User)

    def name(self):
        return self.user.first_name + ' ' + self.user.last_name

    def id(self):
        return self.user.id
    
    def __unicode__(self):
        return self.name()

    # Abstract base class
    class Meta:
        abstract = True

class Employee(BasePerson):
    """
    Employee Class

    user  - User, related field to Django user model
    score - int, quality assessment score for the employee
    """
    score = models.IntegerField(default = 0)
    

class Manager(BasePerson):
    """
    Manager Class
    """

class EmployeeChatList(models.Model):
    employee      = models.ForeignKey(Employee)
    chat_id       = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=20)
    score         = models.IntegerField(default=0)

    def sentiment(self):
        if self.score >= 0:
            return "Acceptable"
        else:
            return "Unacceptable"

    def timestamp(self):
        message = Chat.objects.filter(chat_id=self.chat_id)
        return message[0].timestamp

class Chat(models.Model):
    chat_id     = models.IntegerField(default=0)
    timestamp   = models.DateTimeField(auto_now_add=True)
    message     = models.TextField(default="")
    is_employee = models.BooleanField(default=False)
    score       = models.IntegerField(default=0)

    def sentiment(self):
        if self.score == 1:
            return "Positive"
        elif self.score == -1:
            return "Negative"
        else:
            return "Neutral"
    class Meta:
        ordering = ['timestamp']

