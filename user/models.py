# will use django user model

from django.contrib.auth.models import User


# make email field unique
User._meta.get_field('email')._unique = True
