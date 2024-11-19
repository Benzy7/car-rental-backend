from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from .logger import exception_log

def send_email(recipient, subject, template, data):
    try:
        to = [f"{recipient}"]
        from_email = settings.EMAIL_HOST_USER
        
        html_content = render_to_string(template, data)

        msg = EmailMultiAlternatives(subject, html_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except Exception as e:
        print(e)
        exception_log(e, __file__)
