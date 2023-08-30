from django.shortcuts import render, redirect
from user.models import User
from .decorators import group_required
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from django.contrib.auth import login, logout
from django.views import View
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.cache import cache
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.db.models import Q
from Transactions.models import Transaction


# Create your views here.
class RegistrationView(View):
    template_name = 'register.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        firstname = request.POST.get('firstName')
        lastname = request.POST.get('lastName')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cnic = request.POST.get('cnic')
        contact = request.POST.get('contact')
        profileImg = request.FILES.get('profile')
        address = request.POST.get('address')
        username = str(firstname)+' '+str(lastname)

        if not User.objects.filter(Q(username=username) | Q(contact=contact) | Q(email=email)).exists():
            user = User.objects.create(username=username, email=email, password=password, cnic=cnic,
                                       contact=contact, profileImage=profileImg, address=address, is_active=False)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            activation_link = reverse('confirm_email', kwargs={
                                      'uid': uid, 'token': token})
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
            messages.error(
                request, 'Username , Contact or email is already registered')
            return render(request, self.template_name)


class Login(LoginView):

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        # Get the username and password from the request
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username).first()

        if user is not None:
            attempts = int(user.attempts)
            if user.is_active:
                locked_out = cache.get(f'lockout_{user.username}')
                if locked_out:

                    messages.error(
                        request, 'Account locked. Please try again later.')
                    return render(request, 'login.html')

                if user.check_password(password):
                    attempts = 0
                    cache.delete(f'lockout_{user.username}')
                    user.attempts = str(attempts)
                    user.save()

                    login(request, user)
                    return redirect('homepage')
                else:
                    attempts = attempts+1
                    if attempts > 5:
                        # Lock user out for 5 minutes
                        cache.set(f'lockout_{user.username}', True, 300)
                        messages.error(
                            request, 'Account locked. Please try again later after 5 minutes.')

                    else:
                        message = 'Wrong Password '+str(attempts)
                        messages.error(request, message)
                    user.attempts = str(attempts)
                    user.save()
                    return render(request, 'login.html')

            else:
                messages.error(request, 'Activate your account first')
                return render(request, 'login.html')

        else:
            messages.error(request, 'Invalid User')
            return render(request, 'login.html',)


@method_decorator(login_required, name='dispatch')
class homepage(View):
    def get(self, request):
        return render(request, 'homepage.html')


class ConfirmEmailView(View):
    def get(self, request, token, **kwargs):
        uid = force_text(urlsafe_base64_decode(kwargs['uid']))
        user = User.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
        return redirect('login')


@method_decorator(group_required('AppAdmin'), name='dispatch')
@method_decorator(login_required, name='dispatch')
class StatementHistory(View):
    def get(self, request):
        return render(request, 'StatementHistory.html')

    def post(self, request):
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        if User.objects.filter(Q(contact=contact) | Q(email=email)).exists():
            user = User.objects.get(Q(contact=contact) | Q(email=email))
            transfers = Transaction.objects.filter(user=user)
            heading = 'Transaction History of '+transfers.first().user.username
            return render(request, 'accountStatements.html', {'transfers': transfers, 'heading': heading})
        else:

            error = 'User with mentioned information doesnot exist.'
            messages.error(request, error)
            return render(request, 'StatementHistory.html')


@method_decorator(group_required('AppAdmin'), name='dispatch')
@method_decorator(login_required, name='dispatch')
class loadBalance(View):
    def get(self, request):
        return render(request, 'loadBalance.html')

    def post(self, request):
        username = request.POST.get('username')
        amount = request.POST.get('amount')
        userEdited = User.objects.filter(username=username).first()
        if userEdited is not None:
            userEdited.amount = str(float(amount)+float(userEdited.amount))
            userEdited.save()
            information = 'The amount of the mentioned user is updated successfully'
            messages.success(request, information)
        else:
            information = 'Please enter a valid user.'
            messages.error(request, information)
        return render(request, 'loadBalance.html')


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('login')


@method_decorator(login_required, name='dispatch')
class profile(View):
    def get(self, request):
        user = request.user
        print(request.user.is_authenticated)
        return render(request, 'profilePage.html')

    def post(self, request):

        user = User.objects.get(id=request.user.id)
        new_email = request.POST.get('email')
        user.username = request.POST.get('username', user.username)
        user.cnic = request.POST.get('cnic', user.cnic)
        user.contact = request.POST.get('contact', user.contact)
        profileImg = request.FILES.get('profile', user.profileImage)
        user.profileImage = profileImg
        user.address = request.POST.get('address', user.address)

        if (new_email != user.email):
            user.email = request.POST.get('email', user.email)
            user.is_active = False
            user.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            mail_subject = 'Email Updation Confirmation'
            activation_link = reverse('confirm_email', kwargs={
                                      'uid': uid, 'token': token})
            activation_url = f'http://{current_site.domain}{activation_link}'
            message = render_to_string('activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
                'activation_url': activation_url,
            })

            logout(request)
            send_mail(mail_subject, message,
                      'noreply@example.com', [new_email])
            return redirect('login')

        else:
            user.save()
            return redirect('profile')


class ForgotPassword(View):
    def get(self, request):
        return render(request, 'forgotPassword.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmpassword')

        if User.objects.filter(email=email).exists():
            if (password == confirmPassword):
                user = User.objects.get(email=email)
                user.set_password(password)
                user.is_active = False
                user.save()
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                current_site = get_current_site(request)
                mail_subject = 'Password change Confirmation'
                activation_link = reverse('confirm_email', kwargs={
                                          'uid': uid, 'token': token})
                activation_url = f'http://{current_site.domain}{activation_link}'
                message = render_to_string('activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': uid,
                    'token': token,
                    'activation_url': activation_url,
                })
                send_mail(mail_subject, message,
                          'noreply@example.com', [email])
                return redirect('login')
            else:
                messages.error(
                    request, 'Please make sure that password and confirm password are same.')
                return render(request, 'forgotPassword.html')
        else:
            messages.error(request, 'Mentioned user does not exists.')
            return render(request, 'forgotPassword.html')


def handler404(request, exception):
    return render(request, 'error404.html', status=404)
