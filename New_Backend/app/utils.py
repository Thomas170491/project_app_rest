import random
from io import BytesIO

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.files import File
from django.core.mail import EmailMessage
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from PIL import Image

from .token import generate_token

User = get_user_model()


def send_email_verification(request, email):
    from_email = settings.EMAIL_HOST_USER
    to_list = [email]
    current_site = get_current_site(request)
    print(
        {
            "domain": current_site.domain,
            "email": urlsafe_base64_encode(force_bytes(email)),
            "token": generate_token.make_token(email),
        },
    )
    subject = "Activate Your Account"
    message = render_to_string(
        "invite.html",
        {
            "domain": current_site.domain,
            "email": urlsafe_base64_encode(force_bytes(email)),
            "token": generate_token.make_token(email),
        },
    )
    mail = EmailMessage(subject, message, from_email, to=to_list)
    mail.fail_silently = True
    mail.content_subtype = "html"
    mail.send()
