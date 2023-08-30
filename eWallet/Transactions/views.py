
from django.shortcuts import render
from django.views import View
from user.models import User
from Transactions.models import Transaction
from datetime import datetime
from django.db.models import Q
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# Create your views here.
@method_decorator(login_required, name='dispatch')
class fundsTransfer(View):
    def get(self,request, **kwargs):
        contact =request.GET.get('contact')
        email = request.GET.get('email')
        if contact and email:
            return render(request,'transferFunds.html',{'received_contact':contact,'recieved_email':email})
        else:
            return render(request,'transferFunds.html')

    def post(self,request):
        contact_recieved = request.POST.get('contact')
        email_recieved = request.POST.get('email')
        transaction_sender=request.user
        sender_credit=float(transaction_sender.amount)
        amount=float(request.POST.get('amount'))
        purpose=request.POST.get('purpose')
        if  User.objects.filter(Q(contact=contact_recieved) |Q(email=email_recieved)).exists():
            today = datetime.now().date()
            user_transactions = Transaction.objects.filter(user=request.user, timestamp__date=today ,transaction_type='debit')
            amount_transferred_today = sum(transaction.amount for transaction in user_transactions)
            #updating the amount only if the transfaction limit for today has been achieved
            if (amount_transferred_today>=25000):
                senderBalance=sender_credit-amount-200
                checkamount=amount+200
            else:
                senderBalance=sender_credit-amount
                checkamount=amount

            
            if (sender_credit >= checkamount):
                transaction_reciever=User.objects.get(Q(contact=contact_recieved)|Q(email=email_recieved))
                
                #Sender being entered:
                Transaction.objects.create(user=transaction_sender,transaction_type='debit',otheruser=transaction_reciever.username,amount=float(amount),purpose=purpose)
                #updating the sender user object:
                transaction_sender.amount=str(senderBalance)
                transaction_sender.save()
                #Receiver bring entered:
                Transaction.objects.create(user=transaction_reciever,transaction_type='credit',otheruser=transaction_sender.username ,amount=float(amount),purpose=purpose)
                #updating the reciever user object:
                transaction_reciever.amount=str(float(transaction_reciever.amount)+amount)
                transaction_reciever.save()
                disclaimer='The amount has been transferred successfully!'
                messages.success(request,disclaimer)
                
            else:
                disclaimer='Your credit is insufficent to make the transfer.'
                messages.error(request,disclaimer)
        else:
            disclaimer='The user with the mentioned contact/email doesnot exist.'
            messages.error(request,disclaimer)
        
        return render(request,'transferFunds.html')



@method_decorator(login_required, name='dispatch')
class accountStatement(View):
    def get(self,request):
        transfers=Transaction.objects.filter(user=request.user)
        return render(request,'accountStatements.html',{'transfers':transfers})
    
    

