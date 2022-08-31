from .models import Receipt
from django import forms

class ReceiptsForm(forms.ModelForm):
    student_id = forms.CharField(max_length=255, blank=True)
    first_name = forms.CharField(max_length=255, blank=True)
    last_name = forms.CharField(max_length=255, blank=True)
    student_class = forms.CharField(max_length=20, blank=True)
    fee_type = forms.CharField(max_length=255, blank=True)
    term = forms.CharField(max_length=5)

    class Meta:
        model = Receipt
        fields = ('student_id','first_name','last_name','student_class','fee_type','term')