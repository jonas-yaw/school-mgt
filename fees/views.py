from django.shortcuts import render
from students.models import Student
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from .forms import ReceiptsForm,FeesCatalogueForm
from .models import Receipt,FeesCatalogue
from users.models import CustomUser
from django.http import HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from students.forms import SearchForm


#data pagination modules 
from django.core.paginator import Paginator 

def receipts_list_and_create(request):
    form = ReceiptsForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        instance = form.save(commit=False)

        querySet = Student.objects.filter(student_id__iexact=instance.student_id,
        first_name__iexact=instance.first_name,
        last_name__iexact=instance.last_name)
        
        #print(querySet)
        if querySet:  
            print('Student validated')      
            def get_balance():
                return Receipt.objects.filter(
                student_id__iexact=instance.student_id,
                student_class__iexact=instance.student_class ,
                academic_year__iexact=instance.academic_year,
                fee_type__iexact = instance.fee_type ,
                term__iexact =instance.term)[:1]
            
            def get_default_balance():
                return FeesCatalogue.objects.filter(
                student_class__iexact=instance.student_class ,
                academic_year__iexact=instance.academic_year,
                term__iexact =instance.term,
                fee_type__iexact = instance.fee_type
                )
    
            previous_balance = 0 
            
            balance_result_1 = get_balance()
            #print(balance_result_1)
            for x in balance_result_1:
                previous_balance = x.balance

            default_balance = 0

            balance_result_2 = get_default_balance()
            for y in balance_result_2:
                default_balance = y.total_fees

            if not balance_result_1 and default_balance > 0:
                instance.balance = default_balance - instance.amount_paid 
            else:
                instance.balance = previous_balance - instance.amount_paid 

            instance.receipient = request.user

            instance.save()


            message = 'Payment Successful'
            return render(request, 'receipt.html', {'objects': instance,'message':message})
        else:
            print('Not a Student')
            message = 'Not a Student'
            return render(request,'receipt.html', {'message':message})
        


    # notice this comes after saving the form to pick up new objects
    objects = Receipt.objects.all()

    p = Paginator(Receipt.objects.all(),10)
    page = request.GET.get('page')
    fees_list = p.get_page(page)

    nums = "a" * fees_list.paginator.num_pages

    search_form = SearchForm(request.GET or None)
    if request.method == 'GET' and search_form.is_valid():
        student_name = request.GET['student_name']
        #print(student_name)

        searched_students = Receipt.objects.filter(first_name__icontains=student_name) | Receipt.objects.filter(last_name__icontains=student_name) | Receipt.objects.filter(student_class__icontains=student_name)

        pagn = Paginator(searched_students.all(),10)
        page1 = request.GET.get('page')
        searched_receipts = pagn.get_page(page1)

        numbs = "a" * searched_receipts.paginator.num_pages
        return render(request, 'receipt_list_search.html', {
        'searched_receipts': searched_receipts,
        'numbs':numbs
        })


    return render(request, 'receipt_list.html', {'objects': objects,
    'fees_list':fees_list,
    'nums':nums, 
    'form': form,
    'search_form': search_form
    })


class ReceiptDeleteView(LoginRequiredMixin,DeleteView):
    model = Receipt
    template_name = 'receipt_delete.html'
    success_url = reverse_lazy('receipts')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user != CustomUser.objects.get(username="admin"):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)



def fees_catalogue_list_and_create(request):
    form = FeesCatalogueForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()

    # notice this comes after saving the form to pick up new objects
    p = Paginator(FeesCatalogue.objects.all(),10)
    page = request.GET.get('page')
    fees_catalogue_list = p.get_page(page)

    nums = "a" * fees_catalogue_list.paginator.num_pages

    return render(request, 'fees_catalogue_list.html', {
    'fees_catalogue_list':fees_catalogue_list,
    'nums':nums, 
    'form': form
    })


class FeesCatalogueUpdateView(LoginRequiredMixin,UpdateView):
    model = FeesCatalogue
    template_name = 'fees_catalogue_update.html'
    fields = ['student_class','term','academic_year','total_fees','fee_type']

    def dispatch(self, request, *args, **kwargs):
        if self.request.user != CustomUser.objects.get(username="admin"):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class FeesCatalogueDeleteView(LoginRequiredMixin,DeleteView):
    model = FeesCatalogue
    template_name = 'fees_catalogue_delete.html'
    success_url = reverse_lazy('fees_catalogue')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user != CustomUser.objects.get(username="admin"):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
