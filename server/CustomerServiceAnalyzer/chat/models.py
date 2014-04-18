from django.db import models

# Create your models here.
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