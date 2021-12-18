import re
import dearpygui.dearpygui as dpg

from ..base_table import init_table
from BUS.staff import StaffTypeBUS
from DTO.staff import StaffType

class CustomerStaffTypeGUI:
    group_content_window = None
    table = None

    @classmethod
    def content_render(cls, data):
        dpg.delete_item(cls.group_content_window, children_only=True)
        dpg.add_text(default_value=data, parent=cls.group_content_window)
        cls.table = None
        
        top_group = dpg.add_group(horizontal=True, parent=cls.group_content_window)
        dpg.add_button(label="Add new staff type", callback=cls.create_window, parent=top_group)
        search_text = dpg.add_input_text(label="Search", parent=top_group, on_enter=True, callback=cls.search_callback)

        header = ['id', 'name']
        type_columns = [int, str]
        staff_type_bus = StaffTypeBUS()
        staff_type_data = staff_type_bus.objects

        if cls.table is not None:
            dpg.delete_item(cls.table)
            cls.table = None
        
        data = []
        for st in staff_type_data:
            data.append([
                st.id,
                st.name
        ])

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

    @classmethod
    def create_window(cls):
        window = dpg.add_window(label="Add new staff type", width=400, autosize=True, pos=[500, 200])
        staff_name = dpg.add_input_text(label="Name ", parent=window)
        
        group = dpg.add_group(horizontal=True, parent=window)
        button = dpg.add_button(label="Add new staff type", callback=cls.create_window_callback, parent=group)
        status = dpg.add_text(default_value="Status", parent=group)
        dpg.set_item_user_data(
            button, 
            {
                'window': window,
                'status': status, 
                'items': [
                    {
                        'field': 'name',
                        'name': 'Staff name',
                        'item': staff_name,
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
                request_data[item['field']] = data
            else:
                is_valid = False
                dpg.configure_item(user_data['status'], default_value=f'Status: {item["name"]} is invalid', color=[255, 92, 88])               
                break
            
        if is_valid:
            dpg.configure_item(user_data['status'], default_value=f'Status: OK', color=[128, 237, 153])    
            
            staff_type_obj = StaffType(
                id=0,
                name=request_data['name']
            ) 
            staff_type_bus = StaffTypeBUS()
            error = staff_type_bus.create(staff_type_obj)
            
            if error.status is True:
                dpg.configure_item(user_data['status'], default_value=f'Status: {error.message}', color=[255, 92, 88])
            else:
                dpg.delete_item(user_data['window'])
                cls.content_render("staff_type")

    @classmethod
    def modified_window(cls, sender, app_data, user_data):
        staff_types = StaffTypeBUS().objects
        
        staff_type = [st for st in staff_types if st.id == user_data][0]
        
        window = dpg.add_window(label="Modified the staff type", width=400, autosize=True, pos=[500, 200])
        staff_type_id = dpg.add_text(default_value=f"id: {staff_type.id}", parent=window)
        staff_type_name = dpg.add_input_text(label="Name ", parent=window, default_value=staff_type.name)
        
        group = dpg.add_group(horizontal=True, parent=window)
        button = dpg.add_button(label="Save the tour", callback=cls.modified_window_callback, parent=group)
        status = dpg.add_text(default_value="Status", parent=group)
        dpg.set_item_user_data(
            button, 
            {
                'window': window,
                'status': status, 
                'id': staff_type.id,
                'items': [
                    {
                        'field': 'name',
                        'name': 'Staff type name',
                        'item': staff_type_name,
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
                request_data[item['field']] = data
            else:
                is_valid = False
                dpg.configure_item(user_data['status'], default_value=f'Status: {item["name"]} is invalid', color=[255, 92, 88])               
                break
            
        if is_valid:
            dpg.configure_item(user_data['status'], default_value=f'Status: OK', color=[128, 237, 153])    
            
            staff_type_obj = StaffType(
                id=user_data['id'],
                name=request_data['name']
            ) 
            staff_type_bus = StaffTypeBUS()
            error = staff_type_bus.update(staff_type_obj)
            
            if error.status is True:
                dpg.configure_item(user_data['status'], default_value=f'Status: {error.message}', color=[255, 92, 88])
            else:
                dpg.delete_item(user_data['window'])
                cls.content_render('staff_type')

    @classmethod
    def delete_window(cls, sender, app_data, user_data):
        staff_type_id = user_data
        window = dpg.add_window(label="Modified the staff type", width=400, autosize=True, pos=[500, 200])

        question = dpg.add_text(default_value=f"Do you want to delete the staff type (id: {staff_type_id})?", parent=window)
        status = dpg.add_text(default_value="Status", parent=window)
        
        group = dpg.add_group(horizontal=True, parent=window)
        
        user_data = {
            'staff_type_id': staff_type_id,
            'status': status,
            'window': window
        }
        button_yes = dpg.add_button(label="Yes", callback=cls.delete_window_callback, user_data=user_data, parent=group)
        button_no = dpg.add_button(label="Cancel", callback=lambda :dpg.delete_item(window), parent=group)

    @classmethod
    def delete_window_callback(cls, sender, app_data, user_data):
        error = StaffTypeBUS().delete(user_data['staff_type_id'])
        if error.status is True:
            dpg.configure_item(user_data['status'], default_value=f'Status: {error.message}', color=[255, 92, 88])
        else:
            dpg.configure_item(user_data['status'], default_value=f'Status: OK', color=[128, 237, 153])
            dpg.delete_item(user_data['window'])
            cls.content_render('staff_type')

    @classmethod
    def view_window(cls, sender, app_data, user_data):
        staff_types = StaffTypeBUS().objects
        staff_type = [st for st in staff_types if st.id == user_data][0]
        
        window = dpg.add_window(label="Modified the tour", width=400, autosize=True, pos=[500, 200])
        dpg.add_text(default_value=f"id: {staff_type.id}", parent=window)
        dpg.add_text(default_value=f"Name: {staff_type.name}", parent=window)
        dpg.add_button(label="Close", callback=lambda :dpg.delete_item(window), parent=window)

    @classmethod
    def search_callback(cls,sender, app_data, user_data):
        staff_type_bus = StaffTypeBUS()
        staff_type = staff_type_bus.objects
        header = ['id', 'name']
        type_columns = [int, str]
        data = []
        for st in staff_type:
                search = re.search(app_data, st.name)
                if (search):
                    data.append([
                        st.id,
                        st.name
                    ])
        
        dpg.delete_item(cls.table)
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

    

    