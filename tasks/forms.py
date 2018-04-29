from django.forms import *
from tasks.models import *


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['content']
        labels = {
            'content': ''
        }
        widgets = {
            'content': TextInput(attrs={'placeholder': 'insert new Task'}),
        }
