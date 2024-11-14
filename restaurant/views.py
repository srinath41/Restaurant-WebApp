from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import render
from .forms import BookingForm
from .models import Menu
from django.core.mail import send_mail
from django.conf import settings

def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()

            # Send email notification with the user's email as the sender
            subject = "New Reservation Received"
            message = f"New reservation from {form.cleaned_data['first_name']} {form.cleaned_data['last_name']}.\n\nDetails:\n\nGuest Number: {form.cleaned_data['guest_number']}\nComment: {form.cleaned_data['comment']}"
            from_email = settings.EMAIL_HOST_USER  # Your Gmail address
            recipient_list = ["devarapallisrinath8@gmail.com"]  # Your email address for receiving notification
            reply_to_email = form.cleaned_data['email']  # User's email address

            # Create an email message
            email = EmailMessage(
                subject,
                message,
                from_email,
                recipient_list
            )
            email.reply_to = [reply_to_email]  # Add the Reply-To header

            # Send the email
            email.send(fail_silently=False)

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': 'Your reservation has been successfully submitted!'})
            else:
                return render(request, 'book.html', {'form': form, 'success': True})

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': 'There was an error with your reservation. Please check the form and try again.'})

    context = {'form': form}
    return render(request, 'book.html', context)

# Create your views here.
def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def menu(request):
    menu_data = Menu.objects.all()
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', main_data)


def display_menu_item(request, pk=None):
    if pk:
        menu_item = Menu.objects.get(pk=pk)
    else:
        menu_item = ''

    return render(request, 'menu_item.html', {"menu_item": menu_item})
