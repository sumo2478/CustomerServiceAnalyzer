from django.db import models
from django.contrib.auth.models import User

from chat.models import Chat

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
    

class Manager(BasePerson):
    """
    Manager Class
    """