import re
import dearpygui.dearpygui as dpg

from ..base_table import init_table
from BUS.tour import TourTypeBUS
from DTO.tour import TourType


class TourTypeGUI:
    group_content_window = None
    table = None

    @classmethod
    def content_render(cls, data):
        dpg.delete_item(cls.group_content_window, children_only=True)
        dpg.add_text(default_value=data, parent=cls.group_content_window)
        cls.table = None
        
        top_group = dpg.add_group(horizontal=True, parent=cls.group_content_window)
        dpg.add_button(label="Add new type", callback=cls.create_window, parent=top_group)
        dpg.add_input_text(label="Search", parent=top_group, on_enter=True, callback=cls.search_callback)
        # dpg.add_combo(label="Columns", items=['column1', 'column2', 'column3'], parent=top_group)
        
        header = ['id', 'name']
        type_columns = [int, str]
        data = []
        tour_type_bus = TourTypeBUS()
        tour_type_data = tour_type_bus.objects
        
        if cls.table is not None:
            dpg.delete_item(cls.table)
            cls.table = None

        for d in tour_type_data:
            data.append([
                d.id,
                d.name
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
        tour_type_name = dpg.add_input_text(label="Name ", parent=window)
        
        group = dpg.add_group(horizontal=True, parent=window)
        button = dpg.add_button(label="Add new characterisitc", callback=cls.create_window_callback, parent=group)
        status = dpg.add_text(default_value="Status", parent=group)
        dpg.set_item_user_data(
            button, 
            {
                'window': window,
                'status': status, 
                'items': [
                    {
                        'field': 'name',
                        'name': 'Type name',
                        'item': tour_type_name,
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
            
            tour_obj = TourType(
                id=0,
                name=request_data['name']
            ) 
            tour_type_bus = TourTypeBUS()
            error = tour_type_bus.create(tour_obj)
            
            if error.status is True:
                dpg.configure_item(user_data['status'], default_value=f'Status: {error.message}', color=[255, 92, 88])
            else:
                dpg.delete_item(user_data['window'])
                cls.content_render("tour_type")
                
    @classmethod
    def modified_window(cls, sender, app_data, user_data):
        tour_types = TourTypeBUS().objects
        
        tour_type = [t for t in tour_types if t.id == user_data][0]
        
        window = dpg.add_window(label="Modified the type", width=400, autosize=True, pos=[500, 200])
        dpg.add_text(default_value=f"id: {tour_type.id}", parent=window)
        tour_name = dpg.add_input_text(label="Name ", parent=window, default_value=tour_type.name)
        
        group = dpg.add_group(horizontal=True, parent=window)
        button = dpg.add_button(label="Save the type", callback=cls.modified_window_callback, parent=group)
        status = dpg.add_text(default_value="Status", parent=group)
        dpg.set_item_user_data(
            button, 
            {
                'window': window,
                'status': status, 
                'id': tour_type.id,
                'items': [
                    {
                        'field': 'name',
                        'name': 'Type name',
                        'item': tour_name,
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
            
            tour_type_obj = TourType(
                id=user_data['id'],
                name=request_data['name']
            ) 
            tour_type_bus = TourTypeBUS()
            error = tour_type_bus.update(tour_type_obj)
            
            if error.status is True:
                dpg.configure_item(user_data['status'], default_value=f'Status: {error.message}', color=[255, 92, 88])
            else:
                dpg.delete_item(user_data['window'])
                cls.content_render('tour_type')
        
    @classmethod
    def delete_window(cls, sender, app_data, user_data):
        tour_type_id = user_data
        window = dpg.add_window(label="Delete the type", width=400, autosize=True, pos=[500, 200])

        question = dpg.add_text(default_value=f"Do you want to delete the type (id: {tour_type_id})?", parent=window)
        status = dpg.add_text(default_value="Status", parent=window)
        
        group = dpg.add_group(horizontal=True, parent=window)
        
        user_data = {
            'tour_type_id': tour_type_id,
            'status': status,
            'window': window
        }
        button_yes = dpg.add_button(label="Yes", callback=cls.delete_window_callback, user_data=user_data, parent=group)
        button_no = dpg.add_button(label="Cancel", callback=lambda :dpg.delete_item(window), parent=group)
        
    @classmethod
    def delete_window_callback(cls, sender, app_data, user_data):
        error = TourTypeBUS().delete(user_data['tour_type_id'])
        if error.status is True:
            dpg.configure_item(user_data['status'], default_value=f'Status: {error.message}', color=[255, 92, 88])
        else:
            dpg.configure_item(user_data['status'], default_value=f'Status: OK', color=[128, 237, 153])
            dpg.delete_item(user_data['window'])
            cls.content_render('tour_type')
            
    @classmethod
    def view_window(cls, sender, app_data, user_data):
        tour_types = TourTypeBUS().objects
        tour_type = [t for t in tour_types if t.id == user_data][0]
        
        window = dpg.add_window(label="View the Type", width=400, autosize=True, pos=[500, 200])
        dpg.add_text(default_value=f"id: {tour_type.id}", parent=window)
        dpg.add_text(default_value=f"Name: {tour_type.name}", parent=window)
        dpg.add_button(label="Close", callback=lambda :dpg.delete_item(window), parent=window)

    @classmethod
    def search_callback(cls,sender, app_data, user_data):
        tour_type_bus = TourTypeBUS()
        tour_type = tour_type_bus.objects
        header = ['id', 'name']
        type_columns = [int, str]
        data = []
        for tt in tour_type:
                search = re.search(app_data, tt.name)
                if (search):
                    data.append([
                        tt.id,
                        tt.name
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