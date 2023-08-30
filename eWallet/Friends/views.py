from django.shortcuts import render
from user.models import User
from django.views import View
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from Friends.models import Friend
from django.contrib import messages
# Create your views here.
@method_decorator(login_required, name='dispatch')
class Pals(View):
    def get(self,request):
        friends=Friend.objects.filter(user=request.user)
        #user objects of friends
        user_query= Q()
        users = []
        if Friend.objects.filter(user=request.user).exists():
            for friend in friends:
                user_query = Q(email=friend.email) | Q(contact=friend.contact)
                current_user=User.objects.get(user_query)
                users.append(current_user)
            
        else:
            users=[]
        combined_data = zip(friends, users)
        
       
        return render(request,'seePals.html',{'combined_data':combined_data})
    
@method_decorator(login_required, name='dispatch')
class AddPals(View):
    def get(self,request):
        return render(request,'palsPage.html')
    
    def post(self,request):
        nickname=request.POST.get('nickname') 
        email=request.POST.get('email')
        contact=request.POST.get('contact')
        if (User.objects.filter(Q(email=email) | Q(contact=contact)).exists()):
            if  (email and contact):
                Friend.objects.create(user=request.user,email=email,contact=contact,nickname=nickname)
            elif contact:
                Friend.objects.create(user=request.user,contact=contact,nickname=nickname)
            elif email:
                Friend.objects.create(user=request.user,email=email,nickname=nickname)

            msg='The pal with the specified credentials have been added as a payee.'
            messages.success(request,msg)
        else:
            msg='Please provide the correct and complete detail.'
            messages.error(request,msg)

        return render(request,'palsPage.html')
        

