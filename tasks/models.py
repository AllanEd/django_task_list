from django.db import models

# Create your models here.

class Task(models.Model):
    content = models.CharField(max_length=500)
    done = models.BooleanField(default=False)

    def __str__(self):
        return "Content: {}, Done: {}".format(self.content, self.done)