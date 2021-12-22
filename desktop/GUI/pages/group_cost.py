import re
import dearpygui.dearpygui as dpg

from BUS.group import GroupCostTypeBUS
from DTO.group import Group, GroupCost, GroupCostType
from ..base_table import init_table
from BUS.group import GroupCostBUS, GroupBUS

class GroupCostGUI:
    group_content_window = None
    table = None

    
    @classmethod
    def content_render(cls, data, default_choice=None):
        dpg.delete_item(cls.group_content_window, children_only=True)
        cls.table = None

        groups = [f'{g.id} | {g.name}' for g in GroupBUS().objects]
        
        high_top_group = dpg.add_group(horizontal=True, parent=cls.group_content_window)
        dpg.add_text(default_value=data, parent=high_top_group)
        group_combo = dpg.add_combo(label="Group", items=groups, parent=high_top_group, callback=cls.choice_group_combo)
        
        top_group = dpg.add_group(horizontal=True, parent=cls.group_content_window)
        dpg.add_button(label="Add new group cost", callback=cls.create_window, parent=top_group)
        search_text = dpg.add_input_text(label="Search", parent=top_group, on_enter=True)
        column_text = dpg.add_combo(label="Columns", items=['all', 'name', 'price', 'group', 'type'], parent=top_group, default_value='all')
        dpg.set_item_user_data(search_text, {
            'group': group_combo,
            'column': column_text
        })
        dpg.set_item_callback(search_text, cls.search_callback)

        if default_choice is not None:
            dpg.configure_item(group_combo, default_value=default_choice)
            cls.choice_group_combo(group_combo, default_choice)

    @classmethod
    def choice_group_combo(cls, sender, app_data):
        header = ['id', 'name', 'price', 'group', 'type']
        type_columns = [int, str, float, str, str]

        group_id = int(app_data.split('|')[0])

        data = []
        cost_bus = GroupCostBUS()
        cost_data = [c for c in cost_bus.objects if c.group.id == group_id]
        for c in cost_data:
            data.append([
                c.id,
                c.name,
                c.price,
                c.group.name,
                c.type.name
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
        window = dpg.add_window(label="Add new cost", width=400, autosize=True, pos=[500, 200])
        name = dpg.add_input_text(label="Name ", parent=window)
        price = dpg.add_input_text(label="Price ", parent=window)

        groups = GroupBUS().objects
        cost_types = GroupCostTypeBUS().objects

        groups = [f'{g.id} | {g.name}' for g in groups]
        types = [f'{ct.id} | {ct.name}' for ct in cost_types]

        group_combo = dpg.add_combo(label="Group ", items=groups, parent=window)
        type_combo = dpg.add_combo(label="Type ", items=types, parent=window)

        group = dpg.add_group(horizontal=True, parent=window)
        button = dpg.add_button(label="Add new group cost", callback=cls.create_window_callback, parent=group)
        status = dpg.add_text(default_value="Status", parent=group)
        dpg.set_item_user_data(
            button,
            {
                'window': window,
                'status': status, 
                'items': [
                    {
                        'field': 'name',
                        'name': 'Cost name',
                        'item': name
                    },
                    {
                        'field': 'price',
                        'name': 'Cost price',
                        'item': price
                    },
                    {
                        'field': 'group',
                        'name': 'Cost group',
                        'item': group_combo
                    },
                    {
                        'field': 'type',
                        'name': 'Cost type',
                        'item': type_combo
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
            
            group_choice_value = request_data['group']
            request_data['group']  = int(request_data['group'].split('|')[0])                
            request_data['type'] = int(request_data['type'].split('|')[0])        
            
            cost_obj = GroupCost(
                id=0,
                name=request_data['name'],
                price=request_data['price'],
                group=Group(request_data['group'], None, None, None, None, None, None),
                type=GroupCostType(request_data['type'], None)
            ) 
            cost_bus = GroupCostBUS()
            error = cost_bus.create(cost_obj)
            
            if error.status is True:
                dpg.configure_item(user_data['status'], default_value=f'Status: {error.message}', color=[255, 92, 88])
            else:
                dpg.delete_item(user_data['window'])
                cls.content_render("group_cost", default_choice=group_choice_value)

    @classmethod
    def modified_window(cls, sender, app_data, user_data):
        costs = GroupCostBUS().objects
        cost = [c for c in costs if c.id == user_data][0]

        window = dpg.add_window(label="Add new cost", width=400, autosize=True, pos=[500, 200])
        dpg.add_text(default_value=f"id: {cost.id}", parent=window)
        name = dpg.add_input_text(label="Name ", parent=window, default_value=cost.name)
        price = dpg.add_input_text(label="Price ", parent=window, default_value=cost.price)

        groups = GroupBUS().objects
        cost_types = GroupCostTypeBUS().objects

        groups = [f'{g.id} | {g.name}' for g in groups]
        types = [f'{ct.id} | {ct.name}' for ct in cost_types]
        
        group_cost = f'{cost.group.id} | {cost.group.name}'
        cost_type = f'{cost.type.id} | {cost.type.name}'

        group_combo = dpg.add_combo(label="Group ", items=groups, parent=window, default_value=group_cost)
        type_combo = dpg.add_combo(label="Type ", items=types, parent=window, default_value=cost_type)

        group = dpg.add_group(horizontal=True, parent=window)
        button = dpg.add_button(label="Modifiedgroup cost", callback=cls.modified_window_callback, parent=group)
        status = dpg.add_text(default_value="Status", parent=group)
        dpg.set_item_user_data(
            button,
            {
                'window': window,
                'status': status,
                'id': cost.id,
                'items': [
                    {
                        'field': 'name',
                        'name': 'Cost name',
                        'item': name
                    },
                    {
                        'field': 'price',
                        'name': 'Cost price',
                        'item': price
                    },
                    {
                        'field': 'group',
                        'name': 'Cost group',
                        'item': group_combo
                    },
                    {
                        'field': 'type',
                        'name': 'Cost type',
                        'item': type_combo
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
            
            group_choice_value = request_data['group']
            request_data['group']  = int(request_data['group'].split('|')[0])                
            request_data['type'] = int(request_data['type'].split('|')[0])        
            print(f"{request_data['name']}, {request_data['price']}, {request_data['group']}, {request_data['type']}")
            cost_obj = GroupCost(
                id=user_data['id'],
                name=request_data['name'],
                price=request_data['price'],
                group=Group(request_data['group'], None, None, None, None, None, None),
                type=GroupCostType(request_data['type'], None)
            ) 
            cost_bus = GroupCostBUS()
            error = cost_bus.update(cost_obj)
            
            if error.status is True:
                dpg.configure_item(user_data['status'], default_value=f'Status: {error.message}', color=[255, 92, 88])
            else:
                dpg.delete_item(user_data['window'])
                cls.content_render("group_cost", default_choice=group_choice_value)
        
    @classmethod
    def delete_window(cls, sender, app_data, user_data):
        cost_id = user_data
        window = dpg.add_window(label="Delete the group cost", width=400, autosize=True, pos=[500, 200])

        question = dpg.add_text(default_value=f"Do you want to delete the group cost (id: {cost_id})?", parent=window)
        status = dpg.add_text(default_value="Status", parent=window)
        
        group = dpg.add_group(horizontal=True, parent=window)
        
        user_data = {
            'cost_id': cost_id,
            'status': status,
            'window': window
        }
        button_yes = dpg.add_button(label="Yes", callback=cls.delete_window_callback, user_data=user_data, parent=group)
        button_no = dpg.add_button(label="Cancel", callback=lambda :dpg.delete_item(window), parent=group)
        
    @classmethod
    def delete_window_callback(cls, sender, app_data, user_data):
        error = GroupCostBUS().delete(user_data['cost_id'])
        if error.status is True:
            dpg.configure_item(user_data['status'], default_value=f'Status: {error.message}', color=[255, 92, 88])
        else:
            dpg.configure_item(user_data['status'], default_value=f'Status: OK', color=[128, 237, 153])
            dpg.delete_item(user_data['window'])
            cls.content_render('group_cost')
            
    @classmethod
    def view_window(cls, sender, app_data, user_data):
        cost = [c for c in GroupCostBUS().objects if c.id == user_data][0]

        group = [f'{g.id} | {g.name}' for g in GroupBUS().objects if g.id == cost.group.id][0]
        cost_type = [f'{ct.id} | {ct.name}' for ct in GroupCostTypeBUS().objects if ct.id == cost.type.id][0]
        
        window = dpg.add_window(label="Modified the tour", width=400, autosize=True, pos=[500, 200])
        dpg.add_text(default_value=f"id: {cost.id}", parent=window)
        dpg.add_text(default_value=f"Name: {cost.name}", parent=window)
        dpg.add_text(default_value=f"Price: {cost.price}", parent=window)
        dpg.add_text(default_value=f"Group: {group}", parent=window)
        dpg.add_text(default_value=f"Type: {cost_type}", parent=window)
    
    @classmethod
    def search_callback(cls,sender, app_data, user_data):
        group_id = int(dpg.get_value(user_data['group']).split('|')[0])

        cost_bus = GroupCostBUS()
        cost = [ c for c in cost_bus.objects if c.group.id == group_id]
        header = ['id', 'name', 'price', 'group', 'type']
        type_columns = [int, str, float, str, str]
        data = []
        column_search = dpg.get_value(user_data['column'])
        if (column_search == 'all'):
            for c in cost:
                multi_strings = f"{c.id} | {c.name} | {c.price} | {c.group.name} | {c.type.name}"
                search = re.search(app_data, multi_strings)
                if (search):
                    data.append([
                        c.id,
                        c.name,
                        c.price,
                        c.group.name,
                        c.type.name
                    ])
        if (column_search == 'name'):
            for c in cost:
                search = re.search(app_data, c.name)
                if (search):
                    data.append([
                        c.id,
                        c.name,
                        c.price,
                        c.group.name,
                        c.type.name
                    ])
        if (column_search == 'price'):
            for c in cost:
                search = re.search(app_data, str(c.price))
                if (search):
                    data.append([
                        c.id,
                        c.name,
                        c.price,
                        c.group.name,
                        c.type.name
                    ])
        if (column_search == 'group'):
            for c in cost:
                search = re.search(app_data, c.group.name)
                if (search):
                    data.append([
                        c.id,
                        c.name,
                        c.price,
                        c.group.name,
                        c.type.name
                    ])
        if (column_search == 'type'):
            for c in cost:
                search = re.search(app_data, c.type.name)
                if (search):
                    data.append([
                        c.id,
                        c.name,
                        c.price,
                        c.group.name,
                        c.type.name
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

    

    