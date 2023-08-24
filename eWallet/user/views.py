from django.shortcuts import render, redirect
from user.models import User
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth import  login,logout
from django.views import View
from django.urls import reverse
from django.core.cache import cache
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
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
            user=User.objects.create(username=username, email=email, password=password,cnic=cnic,contact=contact,profileImage=profileImg, address=address,is_active=False)
            # messages.success(request, 'Registration successful! Please confirm your email.')
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            activation_link = reverse('confirm_email', kwargs={'uid': uid, 'token': token})
            activation_url = f'http://{current_site.domain}{activation_link}'
            message = render_to_string('activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': uid,
            'token': token,
            'activation_url': activation_url,
        })
            
            send_mail(mail_subject, message, 'noreply@example.com', [email])
            return redirect('login') 
   
        else:
            return render(request, self.template_name, {'error_message': 'Username already exists'})


class Login(LoginView):

    def get(self,request):
        return render(request, 'login.html')
       
   

    def post(self, request):
        # Get the username and password from the request
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user =User.objects.filter(username=username).first()
        
        if user is not None  :
            attempts= int(user.attempts)
            if user.is_active:
                locked_out = cache.get(f'lockout_{user.username}')
                if locked_out:
                    context = {'info': 'Account locked. Please try again later.'}
                    return render(request, 'login.html', context)

                if user.check_password(password):
                    attempts=0
                    cache.delete(f'lockout_{user.username}')
                    user.attempts=str(attempts)
                    user.save()
                    login(request, user)
                    return render(request, 'homepage.html')
                else:
                    attempts=attempts+1
                    if attempts > 5:
                        cache.set(f'lockout_{user.username}', True, 300)  # Lock user out for 5 minutes
                        context = {'info': 'Account locked. Please try again later after 5 minutes.'}
                       
                    else:
                        context={'info':'Wrong Password','attempts':attempts}
                    user.attempts= str(attempts)
                    user.save()
                    return render(request, 'login.html',context)

            else:
                context={'info':'Activate your account first'}
                return render(request, 'login.html',context)
        
        else:
            
            context={'info':'Invalid User'}
            return render(request, 'login.html',context)
           

  
class Logout(View):
    
    def get(self, request):
        logout(request)
        return  redirect('login')
    
class ConfirmEmailView(View):
    def get(self, request, token, **kwargs):
        uid = force_text(urlsafe_base64_decode(kwargs['uid']))
        user = User.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
        return redirect('login')