import os
import pandas as pd

from django.core.management.color import no_style
from django.core.management.base import BaseCommand
from django.db import connection

from group.models import Group
from customer.models import (
    Customer, 
    GroupCustomer, 
)


filenames = ['Customer', 'GroupCustomer']
filenames = dict(zip(
    filenames,
    list(map(
        lambda filename: os.path.dirname(os.path.abspath(__file__)) + f"/data/{filename}.csv",
        filenames
    ))
))


class Command(BaseCommand):
    
    def init_customer_data(self):
        filename = filenames['Customer']
        df = pd.read_csv(filename).fillna('')
        df = df[['id', 'name', 'id_number', 'address', 'gender', 'phone_number']]

        data_list = df.to_dict(orient='records')

        inserted = []

        for idx, row in enumerate(data_list):
            print(row)
            obj, created = Customer.objects.get_or_create(
                id              = row['id'],
                name            = row['name'],
                id_number       = row['id_number'],
                address         = row['address'],
                gender          = row['gender'],
                phone_number    = row['phone_number']
            )
            inserted.append(obj)

        print("---- INIT CUSTOMER SUCCESSFULLY ----\n")
        print(inserted)
        
    def init_group_customer_data(self):
        filename = filenames['GroupCustomer']
        df = pd.read_csv(filename).fillna('')
        df = df[['id', 'group', 'customer']]

        data_list = df.to_dict(orient='records')

        inserted = []

        for idx, row in enumerate(data_list):
            print(row)
            obj, created = GroupCustomer.objects.get_or_create(
                id              = row['id'],
                group           = Group.objects.get(pk=row['group']),
                customer        = Customer.objects.get(pk=row['customer'])
            )
            inserted.append(obj)

        print("---- INIT GROUP CUSTOMER SUCCESSFULLY ----\n")
        print(inserted)
        
    def reset_primary_key(self):
        sequence_sql = connection.ops.sequence_reset_sql(no_style(), [
            Customer, 
            GroupCustomer, 
        ])
        with connection.cursor() as cursor:
            for sql in sequence_sql:
                cursor.execute(sql)
                        
        print("---- RESET PRIMARY KEY SUCCESSFULLY ----\n")
     
    def handle(self, **options):
        self.init_customer_data()
        self.init_group_customer_data()
        self.reset_primary_key()

        print("---- INIT CUSTOMER DATA SUCCESSFULLY ----\n")