from datetime import timedelta
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from BeautyParlour import settings
from .models import Appointment, Category, Service, Gallery
from .forms import AppointmentForm
from django.urls import reverse
from ParlourApp.forms import UserRegistrationForm


# Create your views here.
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username Already Taken")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email Already Taken")
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                email=email,
                                                password=password)
                user.is_active = False  # set user account as inactive
                user.save()
                # Send an email confirmation message to the user
                token_generator = PasswordResetTokenGenerator()
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = token_generator.make_token(user)

                # Build activation link
                domain = get_current_site(request).domain
                activate_url = request.build_absolute_uri(reverse('activate', kwargs={'uidb64': uidb64, 'token': token}))
                activation_link = activate_url
                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                message = render_to_string('acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'activation_link': activation_link,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),

                })
                to_email = email
                email = EmailMessage(
                            mail_subject, message, to=[to_email]
                )
                email.send()
                messages.success(request, "An email has been sent to your email address. Please verify your email to activate your account.")
                return redirect('login')
        else:
            print("password not match")
            messages.error(request, "Password incorrect")
            return redirect('register')
    return render(request, "register.html")

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated. Please log in.')
        return redirect(reverse('https://beautyparlour-and-shopping-production.up.railway.app/login'))
    else:
        return HttpResponse('Activation link is invalid.')

def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request,"Welcome")
            if user.is_admin:
                return redirect('/admin')
            return redirect("https://beautyparlour-and-shopping-production.up.railway.app/user")
        else:
            messages.error(request, "Invalid credentials!!!")
            return redirect('https://beautyparlour-and-shopping-production.up.railway.app/login')
    return render(request, "login.html")


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('/')


def user(request):
    if request.user.is_authenticated:
        apptmnt_info = Appointment.objects.filter(user=request.user)
        return render(request, "user.html",{
            'info': apptmnt_info,
        })
    return redirect('https://beautyparlour-and-shopping-production.up.railway.app/login')

from django.contrib.auth.views import PasswordResetView

class MyPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html'

########Sevices##########

def demo(request):
    obj = Category.objects.all()
    return render(request, "index.html", {'category': obj})


def bridal(request):
    bridal = Service.objects.filter(category_id=1)
    return render(request, "services/bridal.html", {'list': bridal})


def hair(request):
    hair = Service.objects.filter(category_id=2)
    return render(request, "services/hair.html", {'list2': hair})


def makeover(request):
    mkup = Service.objects.filter(category_id=6)
    return render(request, "services/makeover.html", {'list5': mkup})


def wax(request):
    wax = Service.objects.filter(category_id=5)
    return render(request, "services/wax.html", {'list6': wax})


def skin(request):
    skin = Service.objects.filter(category_id=3)
    return render(request, "services/skin.html", {'list3': skin})


def nails(request):
    nails = Service.objects.filter(category_id=4)
    return render(request, "services/nails.html", {'list4': nails})

def gallery(request):
    gallery = Gallery.objects.all
    return render(request, "gallery.html", {'photos': gallery})

def contact(request):
    return render(request, "contact.html")


########Appointment##########

def appointment(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AppointmentForm(request.POST)
            if form.is_valid():
                service = form.cleaned_data['service']
                date = form.cleaned_data['date']
                time = form.cleaned_data['time']
                if date < timezone.now().date():
                    messages.info(request, "Date cannot be in the past")
                    return redirect('appointment')
                startdate = date
                enddate = startdate + timedelta(days=0)
                todays_service = Appointment.objects.filter(date__range=[startdate, enddate]).values_list('service').filter(service=service).count()
                todays_slot = Appointment.objects.filter(date__range=[startdate, enddate]).values_list('time').filter(service=service).filter(time=time).count()
                count_per_day = Appointment.objects.filter(date__range=[startdate, enddate]).count()
                if count_per_day > 5:
                    messages.info(request, "Appointment is full for this date!! Try another date!")
                    return redirect('appointment')
                elif todays_service > 2:
                    messages.info(request, "Appointment is full for this service!! Try another day!")
                    return redirect('appointment')
                elif todays_slot > 1:
                    messages.info(request, "Appointment is full for this time slot!! Try another time slot!")
                    return redirect('appointment')
                    # print(result)
                    print(count_per_day)
                    print(todays_aptmnt)
                    print(todays_slot)
                apptmnt = Appointment(user=request.user, service=service, date=date, time=time)
                apptmnt.save()
                send_confirmation_email(apptmnt)
                messages.info(request, "New Appointment Added Successfully!!!")
                apptmnt_info = Appointment.objects.filter(user=request.user)
                return render(request, "appointment_info.html", {
                    'info': apptmnt_info,
                    'service': service,
                    'date': date,
                    'time': time,
                })

        else:
            form = AppointmentForm
        return render(request, 'appointment.html', {'form': form})
    return redirect('login')





def send_confirmation_email(appointment):
    # Render the email template with appointment details
    email_html = render_to_string('appointment_confirmation_email.html', {'appointment': appointment})

    # Create the email message
    email = EmailMessage(
        subject='Appointment Confirmation',
        body=email_html,
        from_email=settings.EMAIL_HOST_USER,
        to=[appointment.user.email]
    )

    # Send the email
    email.content_subtype = 'html'
    email.send()

def appointment_info(request):
    if request.user.is_authenticated:
        apptmnt_info = Appointment.objects.filter(user=request.user)
        return render(request, "appointment_info.html", {
            'info': apptmnt_info,
        })
    return redirect('appointment')


# CRUD OPERATIONS
def Delete(request, id):
    apptmnt_info = Appointment.objects.filter(id=id)
    apptmnt_info.delete()
    messages.info(request, "Appointment Deleted!!!")
    return redirect("appointment_info")


def Update(request, id):
    if request.method == 'POST':
        result = Appointment.objects.get(id=id)
        form = AppointmentForm(request.POST, instance=result)
        if form.is_valid():
            form.save()
            return redirect("appointment_info")
    else:
        result = Appointment.objects.get(id=id)
        form = AppointmentForm(instance=result)
        messages.info(request, "Updated!!!")
    return render(request, 'update_appointment.html', {'form': form})

def new(request):
    return render(request, "new.html")
