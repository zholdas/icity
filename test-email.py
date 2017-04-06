from django.core.mail import send_mail
from django.core.management import setup_environ
import settings
setup_environ(settings)

send_mail(
          "email",
          "message",
          "from@example.com",
          ['tzhe@yandex.ru'],
          )