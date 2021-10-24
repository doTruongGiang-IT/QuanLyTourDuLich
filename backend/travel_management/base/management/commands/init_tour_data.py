import os
import pandas as pd

from django.core.management.color import no_style
from django.core.management.base import BaseCommand
from django.db import connection

from tour.models import (
    Tour, 
    TourCharacteristic, 
    TourType, 
    TourPrice,
    Location,
)


filenames = ['Tour', 'TourCharacteristic', 'TourType', 'TourPrice', 'Location']
filenames = dict(zip(
    filenames,
    list(map(
        lambda filename: os.path.dirname(os.path.abspath(__file__)) + f"/data/{filename}.csv",
        filenames
    ))
))


class Command(BaseCommand):
    
    def init_tour_data(self):
        filename = filenames['Tour']
        df = pd.read_csv(filename).fillna('')
        df = df[['id', 'name', 'characteristic', 'type', 'price', 'location']]

        data_list = df.to_dict(orient='records')

        inserted = []

        for idx, row in enumerate(data_list):
            print(row)
            obj, created = Tour.objects.get_or_create(
                id              = row['id'],
                name            = row['name'],
                characteristic  = TourCharacteristic.objects.get(pk=row['characteristic']),
                type            = TourType.objects.get(pk=row['type']),
                price           = TourPrice.objects.get(pk=row['price']),
                location        = Location.objects.get(pk=row['location'])
            )
            inserted.append(obj)

        print("---- INIT TOUR SUCCESSFULLY ----\n")
        print(inserted)
        
    def init_tour_characteristic_data(self):
        filename = filenames['TourCharacteristic']
        df = pd.read_csv(filename).fillna('')
        df = df[['id', 'name']]

        data_list = df.to_dict(orient='records')

        inserted = []

        for idx, row in enumerate(data_list):
            print(row)
            obj, created = TourCharacteristic.objects.get_or_create(
                id              = row['id'],
                name            = row['name']
            )
            inserted.append(obj)

        print("---- INIT TOUR CHARACTERISTIC SUCCESSFULLY ----\n")
        print(inserted)
        
    def init_tour_type_data(self):
        filename = filenames['TourType']
        df = pd.read_csv(filename).fillna('')
        df = df[['id', 'name']]

        data_list = df.to_dict(orient='records')

        inserted = []

        for idx, row in enumerate(data_list):
            print(row)
            obj, created = TourType.objects.get_or_create(
                id              = row['id'],
                name            = row['name']
            )
            inserted.append(obj)

        print("---- INIT TOUR TYPE SUCCESSFULLY ----\n")
        print(inserted)
        
    def init_tour_price_data(self):
        filename = filenames['TourPrice']
        df = pd.read_csv(filename).fillna('')
        df = df[['id', 'name', 'price', 'start_date', 'end_date']]

        data_list = df.to_dict(orient='records')

        inserted = []

        for idx, row in enumerate(data_list):
            print(row)
            obj, created = TourPrice.objects.get_or_create(
                id              = row['id'],
                name            = row['name'],
                price           = row['price'],
                start_date      = row['start_date'],
                end_date        = row['end_date']
            )
            inserted.append(obj)

        print("---- INIT TOUR PRICE SUCCESSFULLY ----\n")
        print(inserted)
        
    def init_location_data(self):
        filename = filenames['Location']
        df = pd.read_csv(filename).fillna('')
        df = df[['id', 'name', 'type', 'level']]

        data_list = df.to_dict(orient='records')

        inserted = []

        for idx, row in enumerate(data_list):
            print(row)
            obj, created = Location.objects.get_or_create(
                id              = row['id'],
                name            = row['name'],
                type            = row['type'],
                level           = row['level'],
            )
            inserted.append(obj)

        print("---- INIT LOCATION SUCCESSFULLY ----\n")
        print(inserted)
        
    def reset_primary_key(self):
        sequence_sql = connection.ops.sequence_reset_sql(no_style(), [
            Tour, 
            TourCharacteristic, 
            TourType, 
            TourPrice,
            Location,
        ])
        with connection.cursor() as cursor:
            for sql in sequence_sql:
                cursor.execute(sql)
                        
        print("---- RESET PRIMARY KEY SUCCESSFULLY ----\n")
     
    def handle(self, **options):
        self.init_tour_characteristic_data()
        self.init_tour_type_data()
        self.init_tour_price_data()
        self.init_location_data()
        self.init_tour_data()
        self.reset_primary_key()

        print("---- INIT TOUR DATA SUCCESSFULLY ----\n")