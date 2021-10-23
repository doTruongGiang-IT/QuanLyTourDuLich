import os
import pandas as pd
from django.core.management.base import BaseCommand
from group.models import (
    Group, 
    GroupJourney, 
)
from tour.models import (
    Tour,
    Location
)

filenames = ['Group', 'GroupJourney']
filenames = dict(zip(
    filenames,
    list(map(
        lambda filename: os.path.dirname(os.path.abspath(__file__)) + f"/data/{filename}.csv",
        filenames
    ))
))


class Command(BaseCommand):
    
    def init_group_data(self):
        filename = filenames['Group']
        df = pd.read_csv(filename).fillna('')
        df = df[['id', 'name', 'tour', 'start_date', 'end_date', 'revenue']]

        data_list = df.to_dict(orient='records')

        inserted = []

        for idx, row in enumerate(data_list):
            print(row)
            obj, created = Group.objects.get_or_create(
                id              = row['id'],
                name            = row['name'],
                tour            = Tour.objects.get(pk=row['tour']),
                start_date      = row['start_date'],
                end_date        = row['end_date']
            )
            inserted.append(obj)

        print("---- INIT GROUP SUCCESSFULLY ----\n")
        print(inserted)
        
    def init_group_journey_data(self):
        filename = filenames['GroupJourney']
        df = pd.read_csv(filename).fillna('')
        df = df[['id', 'group', 'content', 'start_date', 'end_date', 'location']]

        data_list = df.to_dict(orient='records')

        inserted = []

        for idx, row in enumerate(data_list):
            print(row)
            obj, created = GroupJourney.objects.get_or_create(
                id              = row['id'],
                group           = Group.objects.get(pk=row['group']),
                content         = row['content'],
                start_date      = row['start_date'],
                end_date        = row['end_date'],
                location        = Location.objects.get(pk=row['location']),
            )
            inserted.append(obj)

        print("---- INIT TOUR CHARACTERISTIC SUCCESSFULLY ----\n")
        print(inserted)
     
    def handle(self, **options):
        self.init_group_data()
        self.init_group_journey_data()

        print("---- INIT GROUP DATA SUCCESSFULLY ----\n")