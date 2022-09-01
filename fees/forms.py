from email.policy import default
from random import choices
from .models import Receipt
from django import forms



class ReceiptsForm(forms.ModelForm):
    student_id = forms.CharField(max_length=255)
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    student_class = forms.CharField(max_length=20)
    fee_type = forms.CharField(max_length=255)
    term = forms.CharField(max_length=5)

    class Meta:
        model = Receipt
        fields = ('student_id','first_name','last_name','student_class','fee_type','term')
