from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


from celery import shared_task

@shared_task(name="send_reset_email_task")
def send_reset_email_task(email, user_name, reset_url):
        ctx = {
            'name': user_name,
            'reset_url': reset_url,
        }
        send_mail(
            'Password Reset Email',
            render_to_string('reset_password_email.txt', ctx),
            settings.DDM_MANAGER,
            [email],
            fail_silently=True,
            html_message=render_to_string('reset_password_email.html', ctx),
        )