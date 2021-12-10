import os
import pandas as pd

from django.core.management.color import no_style
from django.core.management.base import BaseCommand
from django.db import connection

from group.models import Group
from staff.models import (
    Staff,
    StaffType, 
    GroupStaff, 
)


filenames = ['Staff', 'StaffType', 'GroupStaff']
filenames = dict(zip(
    filenames,
    list(map(
        lambda filename: os.path.dirname(os.path.abspath(__file__)) + f"/data/{filename}.csv",
        filenames
    ))
))


class Command(BaseCommand):
    
    def init_staff_data(self):
        filename = filenames['Staff']
        df = pd.read_csv(filename).fillna('')
        df = df[['id', 'name']]

        data_list = df.to_dict(orient='records')

        inserted = []

        for idx, row in enumerate(data_list):
            print(row)
            obj, created = Staff.objects.get_or_create(
                id              = row['id'],
                name            = row['name']
            )
            inserted.append(obj)

        print("---- INIT STAFF SUCCESSFULLY ----\n")
        print(inserted)
        
    def init_staff_type_data(self):
        filename = filenames['StaffType']
        df = pd.read_csv(filename).fillna('')
        df = df[['id', 'name']]

        data_list = df.to_dict(orient='records')

        inserted = []

        for idx, row in enumerate(data_list):
            print(row)
            obj, created = StaffType.objects.get_or_create(
                id              = row['id'],
                name            = row['name'],
            )
            inserted.append(obj)

        print("---- INIT STAFF TYPE SUCCESSFULLY ----\n")
        print(inserted)
        
    def init_group_staff_data(self):
        filename = filenames['GroupStaff']
        df = pd.read_csv(filename).fillna('')
        df = df[['id', 'group', 'staff', 'staff_type']]

        data_list = df.to_dict(orient='records')

        inserted = []

        for idx, row in enumerate(data_list):
            print(row)
            obj, created = GroupStaff.objects.get_or_create(
                id              = row['id'],
                group           = Group.objects.get(pk=row['group']),
                staff           = Staff.objects.get(pk=row['staff']),
                staff_type      = StaffType.objects.get(pk=row['staff_type'])
            )
            inserted.append(obj)

        print("---- INIT GROUP STAFF SUCCESSFULLY ----\n")
        print(inserted)
        
    def reset_primary_key(self):
        sequence_sql = connection.ops.sequence_reset_sql(no_style(), [
            Staff, 
            StaffType, 
            GroupStaff, 
        ])
        with connection.cursor() as cursor:
            for sql in sequence_sql:
                cursor.execute(sql)
                        
        print("---- RESET PRIMARY KEY SUCCESSFULLY ----\n")
     
    def handle(self, **options):
        self.init_staff_data()
        self.init_staff_type_data()
        self.init_group_staff_data()
        self.reset_primary_key()

        print("---- INIT STAFF DATA SUCCESSFULLY ----\n")