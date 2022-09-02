from email.policy import default
from random import choices
from .models import Receipt
from django import forms

fee_type_choices = [
    ('BUS','BUS'),
    ('School fees','School fees')
]

class ReceiptsForm(forms.Form):
    student_id = forms.CharField(max_length=255)
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    student_class = forms.CharField(max_length=50)
    fee_type = forms.CharField(max_length=50)
    term = forms.CharField(max_length=5)

    class Meta:
        model = Receipt
        fields = ('student_id','first_name','last_name','student_class','fee_type','term')
