from django.shortcuts import render
from user.models import User
from django.views import View
from django.db.models import Q
from Friends.models import Friend
# Create your views here.
class Pals(View):
    def get(self,request):
        friends=Friend.objects.filter(user=request.user)
        #user objects of friends
        user_query= Q()
        if Friend.objects.filter(user=request.user).exists():
            for friend in friends:
                user_query |= Q(email=friend.email) | Q(contact=friend.contact)

            userObjects = User.objects.filter(user_query)
            userObjects=userObjects[::-1]
        else:
            userObjects={}
        combined_data = zip(friends, userObjects)
        print(friends)
        print(userObjects)
        print(combined_data)
        return render(request,'seePals.html',{'combined_data':combined_data,'Signed_in':True})
    
class AddPals(View):
    def get(self,request):
        return render(request,'palsPage.html',{'Signed_in':True})
    
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
            success=True
        else:
            msg='Please provide the correct and complete detail.'
            success=False

        return render(request,'palsPage.html',{'Signed_in':True,'msg':msg,'success':success})
        

