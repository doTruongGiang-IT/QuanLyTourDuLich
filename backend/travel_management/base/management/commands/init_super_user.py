import os
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

SU_USERNAME = os.environ.get('SU_USERNAME', '')
SU_PASSWORD = os.environ.get('SU_PASSWORD', '')


class Command(BaseCommand):
    def handle(self, **options):
        print("[Super Account Creation] Setting up for DEV environment.")
    
        su_user, created = User.objects.get_or_create(username=SU_USERNAME)
        if created:
            su_user.set_password(SU_PASSWORD)
            su_user.is_superuser = True
            su_user.is_staff = True
            su_user.save()
            print(su_user)
        else:
            print("super user has already existed or cannot be create")
            
        print("\n---- INIT USER SUCCESSFULLY ----\n")