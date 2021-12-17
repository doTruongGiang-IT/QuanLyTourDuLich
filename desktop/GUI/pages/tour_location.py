import re
import dearpygui.dearpygui as dpg

from ..base_table import init_table
from BUS.tour import LocationBUS
from DTO.tour import Location


class TourLocationGUI:
    group_content_window = None
    table = None

    @classmethod
    def content_render(cls, data):
        dpg.delete_item(cls.group_content_window, children_only=True)
        dpg.add_text(default_value=data, parent=cls.group_content_window)
        cls.table = None

        top_group = dpg.add_group(horizontal=True, parent=cls.group_content_window)
        dpg.add_button(label="Add new location", callback=cls.create_window, parent=top_group)
        search_text = dpg.add_input_text(label="Search", parent=top_group, on_enter=True)
        column_search = dpg.add_combo(label="Columns", items=['all', 'name', 'type', 'level'], parent=top_group, default_value='all')
        dpg.set_item_user_data(search_text, column_search)
        dpg.set_item_callback(search_text, cls.search_callback)
        
        header = ['id', 'name', 'type', 'level']
        type_columns = [int, str, str, str]
        data = []
        location_bus = LocationBUS()
        location_data = location_bus.objects

        if cls.table is not None:
            dpg.delete_item(cls.table)
            cls.table = None
        
        for d in location_data:
            data.append([
                d.id,
                d.name,
                d.type,
                d.level
            ])
        
        cls.table = init_table(
            header=header,
            data=data,
            parent=cls.group_content_window,
            type_columns=type_columns,
            is_action=True,
            modified_callback=cls.modified_window,
            delete_callback=cls.delete_window,
            view_callback=cls.view_window
        )
        
    @classmethod
    def create_window(cls):
        window = dpg.add_window(label="Add new characterisitc", width=400, autosize=True, pos=[500, 200])
        location_types = ['Hotel', 'Tourist Area', 'Unknown']
        location_levels = ['District', 'City', 'Province', 'Country', 'Unknown']
        
        location_name = dpg.add_input_text(label="Name ", parent=window)
        location_type = dpg.add_combo(label="Type", items=location_types, parent=window)
        location_level = dpg.add_combo(label="Level", items=location_levels, parent=window)
        
        group = dpg.add_group(horizontal=True, parent=window)
        button = dpg.add_button(label="Add new location", callback=cls.create_window_callback, parent=group)
        status = dpg.add_text(default_value="Status", parent=group)
        dpg.set_item_user_data(
            button, 
            {
                'window': window,
                'status': status, 
                'items': [
                    {
                        'field': 'name',
                        'name': 'Location name',
                        'item': location_name,
                    },
                    {
                        'field': 'type',
                        'name': 'Location type',
                        'item': location_type,
                    },  
                    {
                        'field': 'level',
                        'name': 'Location level',
                        'item': location_level,
                    }
                ]
            }
        )
        
    @classmethod
    def create_window_callback(cls, sender, app_data, user_data):
        is_valid = True
        request_data = {}
        
        for item in user_data['items']:
            data = dpg.get_value(item['item'])
            if data != "": 
                print(data)
                request_data[item['field']] = data
            else:
                is_valid = False
                dpg.configure_item(user_data['status'], default_value=f'Status: {item["name"]} is invalid', color=[255, 92, 88])               
                break
            
        if is_valid:
            dpg.configure_item(user_data['status'], default_value=f'Status: OK', color=[128, 237, 153])
            
            tour_obj = Location(
                id=0,
                name=request_data['name'],
                type=request_data['type'],
                level=request_data['level']
            ) 
            location_bus = LocationBUS()
            error = location_bus.create(tour_obj)
            
            if error.status is True:
                dpg.configure_item(user_data['status'], default_value=f'Status: {error.message}', color=[255, 92, 88])
            else:
                dpg.delete_item(user_data['window'])
                cls.content_render("location")
                
    @classmethod
    def modified_window(cls, sender, app_data, user_data):
        locations = LocationBUS().objects
        
        location = [t for t in locations if t.id == user_data][0]
        
        window = dpg.add_window(label="Modified the location", width=400, autosize=True, pos=[500, 200])
        dpg.add_text(default_value=f"id: {location.id}", parent=window)
        location_types = ['Hotel', 'Tourist Area', 'Unknown']
        location_levels = ['District', 'City', 'Province', 'Country', 'Unknown']
        
        tour_name = dpg.add_input_text(label="Name ", parent=window, default_value=location.name)
        location_type = dpg.add_combo(label="Type", items=location_types, parent=window, default_value=location.type)
        location_level = dpg.add_combo(label="Level", items=location_levels, parent=window, default_value=location.level)
        
        group = dpg.add_group(horizontal=True, parent=window)
        button = dpg.add_button(label="Save the location", callback=cls.modified_window_callback, parent=group)
        status = dpg.add_text(default_value="Status", parent=group)
        dpg.set_item_user_data(
            button, 
            {
                'window': window,
                'status': status, 
                'id': location.id,
                'items': [
                    {
                        'field': 'name',
                        'name': 'Location name',
                        'item': tour_name,
                    },
                    {
                        'field': 'type',
                        'name': 'Location type',
                        'item': location_type,
                    },
                    {
                        'field': 'level',
                        'name': 'Location level',
                        'item': location_level,
                    }
                ]
            }
        )
        
    @classmethod
    def modified_window_callback(cls, sender, app_data, user_data):
        is_valid = True
        request_data = {}
        
        for item in user_data['items']:
            data = dpg.get_value(item['item'])
            if data != "": 
                print(data)
                request_data[item['field']] = data
            else:
                is_valid = False
                dpg.configure_item(user_data['status'], default_value=f'Status: {item["name"]} is invalid', color=[255, 92, 88])               
                break
            
        if is_valid:
            dpg.configure_item(user_data['status'], default_value=f'Status: OK', color=[128, 237, 153])
            
            location_obj = Location(
                id=user_data['id'],
                name=request_data['name'],
                type=request_data['type'],
                level=request_data['level'],
            ) 
            location_bus = LocationBUS()
            error = location_bus.update(location_obj)
            
            if error.status is True:
                dpg.configure_item(user_data['status'], default_value=f'Status: {error.message}', color=[255, 92, 88])
            else:
                dpg.delete_item(user_data['window'])
                cls.content_render('location')
        
    @classmethod
    def delete_window(cls, sender, app_data, user_data):
        location_id = user_data
        window = dpg.add_window(label="Delete the location", width=400, autosize=True, pos=[500, 200])

        question = dpg.add_text(default_value=f"Do you want to delete the location (id: {location_id})?", parent=window)
        status = dpg.add_text(default_value="Status", parent=window)
        
        group = dpg.add_group(horizontal=True, parent=window)
        
        user_data = {
            'location_id': location_id,
            'status': status,
            'window': window
        }
        button_yes = dpg.add_button(label="Yes", callback=cls.delete_window_callback, user_data=user_data, parent=group)
        button_no = dpg.add_button(label="Cancel", callback=lambda :dpg.delete_item(window), parent=group)
        
    @classmethod
    def delete_window_callback(cls, sender, app_data, user_data):
        error = LocationBUS().delete(user_data['location_id'])
        if error.status is True:
            dpg.configure_item(user_data['status'], default_value=f'Status: {error.message}', color=[255, 92, 88])
        else:
            dpg.configure_item(user_data['status'], default_value=f'Status: OK', color=[128, 237, 153])
            dpg.delete_item(user_data['window'])
            cls.content_render('location')
            
    @classmethod
    def view_window(cls, sender, app_data, user_data):
        locations = LocationBUS().objects
        location = [t for t in locations if t.id == user_data][0]
        
        window = dpg.add_window(label="View the Characteristic", width=400, autosize=True, pos=[500, 200])
        dpg.add_text(default_value=f"id: {location.id}", parent=window)
        dpg.add_text(default_value=f"Name: {location.name}", parent=window)
        dpg.add_text(default_value=f"Type: {location.type}", parent=window)
        dpg.add_text(default_value=f"Level: {location.level}", parent=window)
        dpg.add_button(label="Close", callback=lambda :dpg.delete_item(window), parent=window)
    
    @classmethod
    def search_callback(cls,sender, app_data, user_data):
        location_bus = LocationBUS()
        location = location_bus.objects
        header = ['id', 'name', 'type', 'level']
        type_columns = [int, str, str, str]
        data = []
        column_search = dpg.get_value(user_data)
        if (column_search == 'all'):
            for l in location:
                multi_strings = f"{l.id} | {l.name} | {l.type} | {l.level}"
                search = re.search(app_data, multi_strings)
                if (search):
                    data.append([
                        l.id,
                        l.name,
                        l.type,
                        l.level
                    ])
        if (column_search == 'name'):
            for l in location:
                search = re.search(app_data, l.name)
                if (search):
                    data.append([
                        l.id,
                        l.name,
                        l.type,
                        l.level
                    ])
        if (column_search == 'type'):
            for l in location:
                search = re.search(app_data, l.type)
                if (search):
                    data.append([
                        l.id,
                        l.name,
                        l.type,
                        l.level
                    ])
        if (column_search == 'level'):
            for l in location:
                search = re.search(app_data, l.level)
                if (search):
                    data.append([
                        l.id,
                        l.name,
                        l.type,
                        l.level
                    ])
        
        dpg.delete_item(cls.table)
        cls.table= init_table(
                header=header,
                data=data,
                parent=cls.group_content_window,
                type_columns=type_columns,
                is_action=True,
                modified_callback=cls.modified_window,
                delete_callback=cls.delete_window,
                view_callback=cls.view_window
            )   