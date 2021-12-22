import dearpygui.dearpygui as dpg
import re

from BUS.group import GroupBUS
from BUS.staff import StaffBUS, GroupStaffBUS
from DTO.staff import Staff
from ..base_table import init_table


class CustomerStaffGUI:
    group_content_window = None
    table = None

    @classmethod
    def content_render(cls, data, choice_default=None):
        dpg.delete_item(cls.group_content_window, children_only=True)
        #dpg.add_text(default_value=data, parent=cls.group_content_window)
        cls.table = None

        if choice_default is None:
            choice_default = 'All'

        groups = ['All']
        groups += [f'{g.id} | {g.name}' for g in GroupBUS().objects]

        high_top_group = dpg.add_group(horizontal=True, parent=cls.group_content_window)
        dpg.add_text(default_value=data, parent=high_top_group)
        group_combo = dpg.add_combo(label="Group", items=groups, parent=high_top_group, default_value=choice_default, callback=cls.choice_group_combo)
        
        top_group = dpg.add_group(horizontal=True, parent=cls.group_content_window)
        dpg.add_button(label="Add new staff", callback=cls.create_window, parent=top_group)
        #dpg.add_button(label="Add a customer to a group", parent=top_group)
        search_text = dpg.add_input_text(label="Search", parent=top_group, on_enter=True, callback=cls.search_callback, user_data=group_combo)

        cls.choice_group_combo(group_combo, choice_default)
    
    @classmethod
    def choice_group_combo(cls, sender, app_data):
        header = ['id', 'name']
        type_columns = [int, str]

        if app_data == 'All':
            data = []
            staff_bus = StaffBUS()
            staff_data = staff_bus.objects
            for s in staff_data:
                data.append([
                    s.id,
                    s.name
                ])
        else:
            group_id = int(app_data.split('|')[0])

            data = []
            group_staff_bus = GroupStaffBUS()
            group_staff_data = group_staff_bus.group_objects(group_id)
            for gs in group_staff_data:
                data.append([
                    gs.staff.id,
                    gs.staff.name
                ])
            
        if cls.table is not None:
            dpg.delete_item(cls.table)
            cls.table = None

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
        window = dpg.add_window(label="Add new staff", width=400, autosize=True, pos=[500, 200])

        customer_name = dpg.add_input_text(label="Name ", parent=window)
        
        group = dpg.add_group(horizontal=True, parent=window)
        button = dpg.add_button(label="Add new staff", callback=cls.create_window_callback, parent=group)
        status = dpg.add_text(default_value="Status", parent=group)
        dpg.set_item_user_data(
            button,
            {
                'window': window,
                'status': status, 
                'items': [
                    {
                        'field': 'name',
                        'name': 'Customer name',
                        'item': customer_name,
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
            
            staff_obj = Staff(
                id=0,
                name=request_data['name']
            ) 
            staff_bus = StaffBUS()
            error = staff_bus.create(staff_obj)
            
            if error.status is True:
                dpg.configure_item(user_data['status'], default_value=f'Status: {error.message}', color=[255, 92, 88])
            else:
                dpg.delete_item(user_data['window'])
                cls.content_render("staff")

    @classmethod
    def modified_window(cls, sender, app_data, user_data):
        staffs = StaffBUS().objects
        
        staff = [c for c in staffs if c.id == user_data][0]
        
        window = dpg.add_window(label="Modified the staff", width=400, autosize=True, pos=[500, 200])
        staff_id = dpg.add_text(default_value=f"id: {staff.id}", parent=window)
        staff_name = dpg.add_input_text(label="Name ", default_value=staff.name, parent=window)
        
        group = dpg.add_group(horizontal=True, parent=window)
        button = dpg.add_button(label="Save the staff", callback=cls.modified_window_callback, parent=group)
        status = dpg.add_text(default_value="Status", parent=group)
        dpg.set_item_user_data(
            button, 
            {
                'window': window,
                'status': status,
                'id': staff.id,
                'items': [
                    {
                        'field': 'name',
                        'name': 'Customer name',
                        'item': staff_name,
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
            
            staff_obj = Staff(
                id=user_data['id'],
                name=request_data['name']
            ) 
            staff_bus = StaffBUS()
            error = staff_bus.update(staff_obj)
            
            if error.status is True:
                dpg.configure_item(user_data['status'], default_value=f'Status: {error.message}', color=[255, 92, 88])
            else:
                dpg.delete_item(user_data['window'])
                cls.content_render("staff")

    @classmethod
    def delete_window(cls, sender, app_data, user_data):
        staff_id = user_data
        window = dpg.add_window(label="Delete the staff", width=400, autosize=True, pos=[500, 200])

        question = dpg.add_text(default_value=f"Do you want to delete the staff (id: {staff_id})?", parent=window)
        status = dpg.add_text(default_value="Status", parent=window)
        
        group = dpg.add_group(horizontal=True, parent=window)
        
        user_data = {
            'staff_id': staff_id,
            'status': status,
            'window': window
        }
        button_yes = dpg.add_button(label="Yes", callback=cls.delete_window_callback, user_data=user_data, parent=group)
        button_no = dpg.add_button(label="Cancel", callback=lambda :dpg.delete_item(window), parent=group)
    
    @classmethod
    def delete_window_callback(cls, sender, app_data, user_data):
        error = StaffBUS().delete(user_data['staff_id'])
        if error.status is True:
            dpg.configure_item(user_data['status'], default_value=f'Status: {error.message}', color=[255, 92, 88])
        else:
            dpg.configure_item(user_data['status'], default_value=f'Status: OK', color=[128, 237, 153])
            dpg.delete_item(user_data['window'])
            cls.content_render('staff')

    @classmethod
    def view_window(cls, sender, app_data, user_data):
        staff = [s for s in StaffBUS().objects if s.id == user_data][0]
        
        window = dpg.add_window(label="Modified the tour", width=400, autosize=True, pos=[500, 200])
        dpg.add_text(default_value=f"id: {staff.id}", parent=window)
        dpg.add_text(default_value=f"Name: {staff.name}", parent=window)

        dpg.add_button(label="Close", callback=lambda :dpg.delete_item(window), parent=window)

    @classmethod
    def search_callback(cls,sender, app_data, user_data):
        staff_bus = StaffBUS()
        staff = []
        if dpg.get_value(user_data) != 'All':
            group_id = int(dpg.get_value(user_data).split('|')[0])
            group_staff_bus = GroupStaffBUS()
            group_customer_data = group_staff_bus.group_objects(group_id)
            for gc in group_customer_data:
                staff.append(gc.staff)
        if dpg.get_value(user_data) == 'All':
            staff = staff_bus.objects
        header = ['id', 'name', 'id number', "address", "gender", "phone number"]
        type_columns = [int, str, str, str, str, str]
        data = []
        for s in staff:
            search = re.search(app_data, s.name)
            if (search):
                data.append([
                    s.id,
                    s.name
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