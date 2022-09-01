from django.shortcuts import render
from .models import Staff 
from .forms import StaffCreationForm

def staff_list_and_create(request):
    form = StaffCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()

    # notice this comes after saving the form to pick up new objects
    objects = Staff.objects.all()
    return render(request, 'staff_list.html', {'objects': objects, 'form': form})