from django.shortcuts import render
from .models import Staff 
from .forms import StaffCreationForm
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy

def staff_list_and_create(request):
    form = StaffCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()

    # notice this comes after saving the form to pick up new objects
    objects = Staff.objects.all()
    return render(request, 'staff_list.html', {'objects': objects, 'form': form})


class StaffUpdateView(UpdateView):
    model = Staff
    template_name = 'staff_update.html'
    fields = ['first_name','last_name',
    'role','department','date_of_birth','staff_contact','place_of_residence','ssnit_number']


class StaffDeleteView(DeleteView):
    model = Staff
    template_name = 'staff_delete.html'
    success_url = reverse_lazy('staff')