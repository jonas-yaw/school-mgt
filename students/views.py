from email import message
from operator import index
from urllib.request import Request
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView

from django.shortcuts import render
from .forms import StudentCreationForm,CsvImportForm
from .models import Student
from django.urls import reverse_lazy

import pandas as pd 
from .resources import StudentResource
from django.contrib import messages
from django.http import HttpResponse
from tablib import Dataset

from django.db.models import Count
from django.http import JsonResponse


class DashboardView(TemplateView):
    template_name = 'dashboard.html'

""" class StudentListView(ListView):
    model = Student
    template_name = 'student_list.html'


class StudentCreateView(CreateView):
    model = Student
    template_name = 'student_list.html'
    fields = '__all__' """


def list_and_create(request):
    form = StudentCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()

    # notice this comes after saving the form to pick up new objects
    objects = Student.objects.all()
    return render(request, 'student_list.html', {'objects': objects, 'form': form})


class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'student_update.html'
    fields = ['first_name','last_name',
    'student_class','date_of_birth','mother_name',
    'mother_contact','father_name','father_contact','place_of_residence']


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'student_delete.html'
    success_url = reverse_lazy('students')


def simple_upload(request):
    form = CsvImportForm(request.POST or None)

    if request.method == 'POST':
        new_student = request.FILES['excel_file']


        if not new_student.name.endswith('xlsx'):
            messages.info(request,'wrong format')
            return render(request,'import_data.html')

        imported_data = pd.read_excel(new_student)

        count = len(imported_data)-1

        for data in imported_data.index:
           new_record = imported_data.iloc[count].tolist()
           Student.objects.update_or_create(
           first_name = new_record[0],
           last_name = new_record[1],
           year = new_record[2],
           course = new_record[3]
           )
           count = count - 1
           


    return render(request,'import_data.html',{'form': form})



def Student_population(request):
    labels = []
    data = []

    querySet = Student.objects.values('student_class').annotate(class_population=Count('student_class')).order_by('-class_population')
    for x in querySet:
        labels.append(x['student_class'])
        data.append(x['class_population'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })