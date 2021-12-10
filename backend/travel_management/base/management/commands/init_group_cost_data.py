import os
import pandas as pd

from django.core.management.color import no_style
from django.core.management.base import BaseCommand
from django.db import connection

from group.models import (
    Group,
    GroupJourneyCost,
    GroupJourneyCostType, 
)


filenames = ['GroupCost', 'GroupCostType']
filenames = dict(zip(
    filenames,
    list(map(
        lambda filename: os.path.dirname(os.path.abspath(__file__)) + f"/data/{filename}.csv",
        filenames
    ))
))


class Command(BaseCommand):
    
    def init_group_cost_type_data(self):
        filename = filenames['GroupCostType']
        df = pd.read_csv(filename).fillna('')
        df = df[['id', 'name']]

        data_list = df.to_dict(orient='records')

        inserted = []

        for idx, row in enumerate(data_list):
            print(row)
            obj, created = GroupJourneyCostType.objects.get_or_create(
                id              = row['id'],
                name            = row['name'],
            )
            inserted.append(obj)

        print("---- INIT GROUP COST TYPE SUCCESSFULLY ----\n")
        print(inserted)
        
    def init_group_cost_data(self):
        filename = filenames['GroupCost']
        df = pd.read_csv(filename).fillna('')
        df = df[['id', 'name', 'group', 'type', 'price']]

        data_list = df.to_dict(orient='records')

        inserted = []

        for idx, row in enumerate(data_list):
            print(row)
            obj, created = GroupJourneyCost.objects.get_or_create(
                id              = row['id'],
                name            = row['name'],
                group           = Group.objects.get(pk=row['group']),
                type            = GroupJourneyCostType.objects.get(pk=row['type']),
                price           = row['price'],
            )
            inserted.append(obj)

        print("---- INIT GROUP COST SUCCESSFULLY ----\n")
        print(inserted)
        
    def reset_primary_key(self):
        sequence_sql = connection.ops.sequence_reset_sql(no_style(), [
            GroupJourneyCost, 
            GroupJourneyCostType, 
        ])
        with connection.cursor() as cursor:
            for sql in sequence_sql:
                cursor.execute(sql)
                        
        print("---- RESET PRIMARY KEY SUCCESSFULLY ----\n")
     
    def handle(self, **options):
        self.init_group_cost_type_data()
        self.init_group_cost_data()
        self.reset_primary_key()

        print("---- INIT GROUP COST SUCCESSFULLY ----\n")