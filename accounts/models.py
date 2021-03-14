# Django
from django.contrib.auth.models import User as BaseUser
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template import Context, Template
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class User(BaseUser):
    class Meta:
        proxy = True

    def send_auth_email(self, url_template):
        uid = urlsafe_base64_encode(force_bytes(self.pk))
        token = default_token_generator.make_token(self)

        template = Template(url_template)
        context = Context({"uid": uid, "token": token})
        url = template.render(context)

        message = render_to_string("accounts/email_activate.html", {"user": self, "url": url})
        email = EmailMessage("Please confirm your email address", message, to=[self.email])

        return email.send(fail_silently=False)

    def activate(self, token):
        if default_token_generator.check_token(self, token):
            self.is_active = True
            self.save()
            return True

        return False
