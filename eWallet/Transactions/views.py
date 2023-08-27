
from django.shortcuts import render, redirect
from django.views import View
from user.models import User
from Transactions.models import Transaction
from datetime import datetime
from django.db.models import Q
# Create your views here.
class fundsTransfer(View):
    def get(self,request):
        return render(request,'transferFunds.html',{'user':request.user,'Signed_in':True})

    def post(self,request):
        contact_recieved = request.POST.get('contact')
        transaction_sender=request.user
        sender_credit=float(transaction_sender.amount)
        amount=float(request.POST.get('amount'))
        purpose=request.POST.get('purpose')
        if  User.objects.filter(contact=contact_recieved).exists():
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
                transaction_reciever=User.objects.get(contact=contact_recieved)
                
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
                dis_type=True
                
            else:
                disclaimer='Your credit is insufficent to make the transfer.'
                dis_type=False
        else:
            disclaimer='The user with the mentioned contact number doesnot exist.'
            dis_type=False
        
        return render(request,'transferFunds.html',{'user':request.user,'Signed_in':True,'disclaimer':disclaimer ,'dis_type':dis_type })




class accountStatement(View):
    def get(self,request):
        transfers=Transaction.objects.filter(user=request.user)
        return render(request,'accountStatements.html',{'user':request.user,'Signed_in':True,'transfers':transfers})
    
    

