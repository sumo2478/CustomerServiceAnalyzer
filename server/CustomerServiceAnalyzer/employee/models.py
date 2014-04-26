from django.db import models
import datetime

from main.models import BasePerson
from chat.models import Chat

# Create your models here.

class Employee(BasePerson):
    """
    Employee Class

    user  - User, related field to Django user model
    score - int, quality assessment score for the employee
    """
    score = models.IntegerField(default = 0)

    # Retrieve the employees most recent chat sessions
    def retrieve_recent_sessions(self):
        sorted_messages = EmployeeChatList.objects.filter(employee=self).order_by('-timestamp')

        # Sort messages by time

        if len(sorted_messages) > 10:
            return sorted_messages[0:10]
        else:
            return sorted_messages

    # Updates the employee score based on the score of a chat session
    def update_score(self, score):
        if score > 0:
            self.score += 1
        elif score < 0:
            self.score -= 1

    # Retrieve the number of customers helped today
    def num_recent_customers(self):
        messages = EmployeeChatList.objects.filter(employee=self)
        date = datetime.datetime.now()
        today_min = datetime.datetime.combine(date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(date.today(), datetime.time.max)

        return EmployeeChatList.objects.filter(employee=self, timestamp__range=(today_min, today_max)).count()


class EmployeeChatList(models.Model):
    employee      = models.ForeignKey(Employee)
    chat_id       = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=20)
    score         = models.IntegerField(default=0)
    timestamp     = models.DateTimeField(auto_now_add=True)

    def sentiment(self):
        if self.score >= 0:
            return "Acceptable"
        else:
            return "Unacceptable"

    class Meta:
        ordering = ['timestamp']