from django.shortcuts import render, redirect
from user.models import User
from django.contrib import messages
from django.views import View
from django.urls import reverse
# Create your views here.
class RegistrationView(View):
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        firstname = request.POST.get('firstName')
        lastname = request.POST.get('lastName')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cnic = str(request.POST.get('cnic'))
        contact = str(request.POST.get('contact'))
        profileImg = request.POST.get('profile')
        address = str(request.POST.get('address'))
        username =str(firstname)+' '+str(lastname)

        if not User.objects.filter(username=username).exists():
            User.objects.create_user(username=username, email=email, password=password,cnic=cnic,contact=contact,profileImage=profileImg, address=address)
            # messages.success(request, 'Registration successful! Please confirm your email.')
            return redirect(reverse('register'))
        else:
            return render(request, self.template_name, {'error_message': 'Username already exists'})
