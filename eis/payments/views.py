from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import DeleteView
from payments.models import *
from payments.forms import PaymentForm
# Create your views here.
class IndexView(View):
    template_name = 'payments/index.html'
    def get(self, request):
        payments = Payment.objects.all()
        accruals = Accrual.objects.all()
        payment_form = PaymentForm()
        return render(request, self.template_name, 
                      context={"payments": payments, 
                               "accruals": accruals,    
                               "payment_form": payment_form
                               })
    def post(self, request):
        payments = Payment.objects.all()
        accruals = Accrual.objects.all()
        payment_form = PaymentForm(request.POST)
        if not payment_form.is_valid():
            return render(request, self.template_name, 
                          context={"payments": payments, 
                                   "accruals": accruals,    
                                   "payment_form": payment_form})
        date = request.POST['date']
        payment = Payment(date=date)
        payment.save()
        return redirect('index')
    
class DeletePaymentView(DeleteView):
    model = Payment
    fields = '__all__'
    success_url = reverse_lazy('index')