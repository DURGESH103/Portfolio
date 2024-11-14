from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .models import Signup


# Home view
def home(request):
    context = {}
    if request.session.get('user_id'):
        user = Signup.objects.get(id=request.session['user_id'])
        context['username'] = user.username  # Pass username to context
    return render(request, 'home.html', context)

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        subject = f"New Contact Message from {name}"
        full_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        try:
            send_mail(
                subject,
                full_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            return JsonResponse({'success': True, 'message': 'Message sent successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'Failed to send message. Please try again.'})
    return JsonResponse({'success': False, 'message': 'Invalid request.'})

def send_contact_message(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if name and email and message:
            subject = f"New Message from {name}"
            message_body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
            recipient_email = 'dkumar11dec2003@gmail.com'  # Your email

            try:
                send_mail(subject, message_body, settings.DEFAULT_FROM_EMAIL, [recipient_email])
                return JsonResponse({'message': 'Message sent successfully!'})
            except Exception as e:
                return JsonResponse({'error': str(e)})

        return JsonResponse({'error': 'Please fill all fields'})
    return JsonResponse({'error': 'Invalid request'})


def about_view(request):
    return render(request, 'about.html')



