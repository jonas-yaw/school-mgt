from django.shortcuts import render
from students.models import Student
from .forms import ReceiptsForm
from .models import Receipt,FeesCatalogue
from django.http import HttpResponseRedirect
from django.urls import reverse

def receipts_list_and_create(request):
    form = ReceiptsForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        instance = form.save(commit=False)

        querySet = Student.objects.filter(student_id=instance.student_id,first_name=instance.first_name,last_name=instance.last_name)
        
        if querySet is not None:  
            print('Student validated')      
            def get_balance():
                return Receipt.objects.filter(student_id=instance.student_id,
                student_class=instance.student_class ,
                academic_year=instance.academic_year,
                fee_type = instance.fee_type ,
                term =instance.term)[:1]
            
            def get_default_balance():
                return FeesCatalogue.objects.filter(student_class=instance.student_class ,
                academic_year=instance.academic_year,
                term =instance.term,
                fee_type = instance.fee_type
                )
    
            balance_result_1 = get_balance()
            for x in balance_result_1:
                previous_balance = x.balance


            balance_result_2 = get_default_balance()
            for y in balance_result_2:
                default_balance = y.total_fees

            if not balance_result_1:
                instance.balance = default_balance - instance.amount_paid 
            else:
                instance.balance = previous_balance - instance.amount_paid 

            instance.receipient = request.user

            instance.save()


            url = reverse('dashboard')
            return render(request, 'receipt.html', {'objects': instance})
        


    # notice this comes after saving the form to pick up new objects
    objects = Receipt.objects.all()
    return render(request, 'receipt_list.html', {'objects': objects, 'form': form})

