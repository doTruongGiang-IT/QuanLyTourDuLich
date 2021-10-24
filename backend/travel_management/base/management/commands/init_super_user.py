import os

from django.core.management.color import no_style
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import connection


SU_USERNAME = os.environ.get('SU_USERNAME', '')
SU_PASSWORD = os.environ.get('SU_PASSWORD', '')


class Command(BaseCommand):
    def reset_primary_key(self):
        sequence_sql = connection.ops.sequence_reset_sql(no_style(), [
            User
        ])
        with connection.cursor() as cursor:
            for sql in sequence_sql:
                cursor.execute(sql)
                        
        print("---- RESET PRIMARY KEY SUCCESSFULLY ----\n")
    
    def handle(self, **options):
        print("[Super Account Creation] Setting up for DEV environment.")
    
        su_user, created = User.objects.get_or_create(username=SU_USERNAME)
        if created:
            su_user.set_password(SU_PASSWORD)
            su_user.is_superuser = True
            su_user.is_staff = True
            su_user.save()
            self.reset_primary_key()
            print(su_user)
        else:
            print("super user has already existed or cannot be create")
            
        print("\n---- INIT USER SUCCESSFULLY ----\n")