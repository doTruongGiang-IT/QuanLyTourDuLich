from datetime import date, datetime
import re

import dearpygui.dearpygui as dpg
from BUS.group import GroupBUS, GroupJourneyBUS
from BUS.tour import LocationBUS, TourBUS
from BUS.customer import CustomerBUS, GroupCustomerBUS
from DTO.group import Group, GroupJourney
from DTO.customer import Customer, GroupCustomer
from DTO.staff import GroupStaff
from BUS.staff import GroupStaffBUS, StaffBUS, StaffTypeBUS
from DTO.staff import StaffType, Staff
from .customer_customer import CustomerCustomerGUI
from .customer import CustomerGUI

from ..base_table import init_table


class GroupGroupGUI:
    group_content_window = None
    table = None

    @classmethod
    def content_render(cls, data, default_choice=None):
        dpg.delete_item(cls.group_content_window, children_only=True)
        cls.table = None
        
        tours = [f'{t.id} | {t.name}' for t in TourBUS().objects]
        
        high_top_group = dpg.add_group(horizontal=True, parent=cls.group_content_window)
        dpg.add_text(default_value=data, parent=high_top_group)
        tour_combo = dpg.add_combo(label="Tour", items=tours, parent=high_top_group, callback=cls.choice_tour_combo)
        
        top_group = dpg.add_group(horizontal=True, parent=cls.group_content_window)
        dpg.add_button(label="Add new group", callback=cls.create_window, parent=top_group)
        search_text = dpg.add_input_text(label="Search", parent=top_group, on_enter=True)
        column_text = dpg.add_combo(label="Columns", items=['all', 'name', 'start_date', 'end_date', 'revenue'], parent=top_group, default_value='all')
        dpg.set_item_user_data(search_text, {
            'tour': tour_combo,
            'column': column_text
        })
        dpg.set_item_callback(search_text, cls.search_callback)


        if default_choice is not None:
            dpg.configure_item(tour_combo, default_value=default_choice)
            cls.choice_tour_combo(tour_combo, default_choice)
        
    @classmethod
    def choice_tour_combo(cls, sender, app_data):
        tour_id = int(app_data.split('|')[0])
        
        header = ['id', 'name', 'start_date', "end_date", "revenue", "journey"]
        datetime_type = lambda d: datetime.strptime(d, '%Y-%m-%d')
        type_columns = [int, str, datetime_type, datetime_type, int, str]
        data = []
        group_bus = GroupBUS()
        group_data = [g for g in group_bus.objects if g.tour == tour_id]
        
        for d in group_data:
            data.append([
                d.id,
                d.name,
                d.start_date.strftime("%Y-%m-%d"),
                d.end_date.strftime("%Y-%m-%d"),
                d.revenue,
                d.journey
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
        window = dpg.add_window(label="Add new group", width=400, autosize=True, pos=[500, 200])
        group_name = dpg.add_input_text(label="Name ", parent=window)

        tours = [f'{t.id} | {t.name}' for t in TourBUS().objects]
        group_tour = dpg.add_combo(label="Tour", items=tours, parent=window)

        datenow = {
            'month_day': date.today().day,
            'year': date.today().year-1900,
            'month': date.today().month-1
        }
        group_start_date = dpg.add_date_picker(label="Start Date ", parent=window, default_value=datenow)
        group_end_date = dpg.add_date_picker(label="End Date ", parent=window, default_value=datenow)
        
        dpg.add_button(label="Add Journey", callback=cls.create_journey_list_window_callback, parent=window, user_data=group_tour)
        
        group = dpg.add_group(horizontal=True, parent=window)
        button = dpg.add_button(label="Add new group", callback=cls.create_window_callback, parent=group)
        status = dpg.add_text(default_value="Status", parent=group)
        dpg.set_item_user_data(
            button, 
            {
                'window': window,
                'status': status, 
                'items': [
                    {
                        'field': 'name',
                        'name': 'Group name',
                        'item': group_name,
                    },
                    {
                        'field': 'tour',
                        'name': 'Tour',
                        'item': group_tour,
                    },
                    {
                        'field': 'start_date',
                        'name': 'Start date',
                        'item': group_start_date,
                    },
                    {
                        'field': 'end_date',
                        'name': 'End date',
                        'item': group_end_date,
                    }
                ]
            }
        )
        
    @classmethod
    def create_journey_list_window_callback(cls, sender, app_data, user_data):
        group_id = dpg.get_value(user_data)
        int(group_id.split('|')[0])
            
        window = dpg.add_window(label="Add Journey list", width=400, autosize=True, pos=[500, 200])
        title = dpg.add_text(default_value="Journey List (0)", parent=window)
        group = dpg.add_group(parent=window)
        user_data = {
            'title': title,
            'group': group,
            'group_id': group_id
        }
        dpg.add_button(label="[+] New Journey", callback=cls.add_journey_window_callback, user_data=user_data, parent=window)
        
    @classmethod
    def add_journey_window_callback(cls, sender, app_data, user_data):
        window = dpg.add_window(label="New Journey", width=400, autosize=True, pos=[500, 200])
        
        content = dpg.add_input_text(label="Content ", parent=window,)
        datenow = {
            'month_day': date.today().day,
            'year': date.today().year-1900,
            'month': date.today().month-1
        }
        start_date = dpg.add_date_picker(label="Start Date ", parent=window, default_value=datenow)
        end_date = dpg.add_date_picker(label="End Date ", parent=window, default_value=datenow)
        
        location = LocationBUS().objects
        location = [f'{d.id} | {d.name}' for d in location]
        location = dpg.add_combo(label="Location", items=location, parent=window)
        group = dpg.add_group(horizontal=True, parent=window)
        add_button = dpg.add_button(label="[+] Add", callback=cls.add_journey_callback, parent=group)
        status = dpg.add_text(default_value="Status", parent=group)
        
        dpg.set_item_user_data(
            add_button, 
            {
                'window': window,
                'status': status, 
                'journey_list_window': user_data['group'],
                'items': [
                    {
                        'field': 'content',
                        'name': 'Journey content',
                        'item': content,
                    },
                    {
                        'field': 'start_date',
                        'name': 'Start date',
                        'item': start_date,
                    },
                    {
                        'field': 'end_date',
                        'name': 'End date',
                        'item': end_date,
                    },
                    {
                        'field': 'location',
                        'name': 'Location',
                        'item': location,
                    }
                ]
            }
        )
        
    @classmethod
    def add_journey_callback(cls, sender, app_data, user_data):
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
            
            request_data['location']  = int(request_data['location'].split('|')[0])
            location = [l for l in LocationBUS().objects if l.id == request_data['location']][0]
            
            start_date = datetime(request_data['start_date']['year']+1900, request_data['start_date']['month']+1, request_data['start_date']['month_day'])
            end_date = datetime(request_data['end_date']['year']+1900, request_data['end_date']['month']+1, request_data['end_date']['month_day'])
            
            journey_obj = GroupJourney(
                id = 0,
                group = 1,
                content = request_data['content'],
                start_date = start_date,
                end_date = end_date,
                location = location
            )

            journey_bus = GroupJourneyBUS()
            error = journey_bus.create(journey_obj)
            
            if error.status is True:
                dpg.configure_item(user_data['status'], default_value=f'Status: {error.message}', color=[255, 92, 88])
            else:
                dpg.delete_item(user_data['window'])
                journey_list_window = user_data['journey_list_window']
                group_journey = dpg.add_group(horizontal=True, parent=journey_list_window)
                content = dpg.add_text(default_value=journey_obj.content, parent=group_journey)
                modified_button = dpg.add_button(label="[Modified]", parent=group_journey)
                delete_button = dpg.add_button(label="[Delete]", parent=group_journey)
        
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
            
            tour_choice_value = request_data['tour']
            request_data['tour']  = int(request_data['tour'].split('|')[0])

            start_date = datetime(request_data['start_date']['year']+1900, request_data['start_date']['month']+1, request_data['start_date']['month_day'])
            end_date = datetime(request_data['end_date']['year']+1900, request_data['end_date']['month']+1, request_data['end_date']['month_day'])
            
            group_obj = Group(
                id = 0,
                name = request_data['name'],
                tour = request_data['tour'],
                start_date = start_date,
                end_date = end_date,
                revenue = 0,
                journey = []
            )

            group_bus = GroupBUS()
            error = group_bus.create(group_obj)
            
            if error.status is True:
                dpg.configure_item(user_data['status'], default_value=f'Status: {error.message}', color=[255, 92, 88])
            else:
                dpg.delete_item(user_data['window'])
                cls.content_render("group", default_choice=tour_choice_value)
                
    @classmethod
    def modified_window(cls, sender, app_data, user_data):
        groups = GroupBUS().objects
        
        group_object = [g for g in groups if g.id == user_data][0]
        
        window = dpg.add_window(label="Modified the group", width=400, autosize=True, pos=[500, 200])

        group_id = dpg.add_text(default_value=f"id: {group_object.id}", parent=window)
        group_name = dpg.add_input_text(label="Name ", parent=window, default_value=group_object.name)

        tours = [f'{t.id} | {t.name}' for t in TourBUS().objects]
        tour = [f'{t.id} | {t.name}' for t in TourBUS().objects if t.id == group_object.tour][0]
        group_tour = dpg.add_combo(label="Tour", items=tours, parent=window, default_value=tour)

        start_date={
            'month_day': group_object.start_date.day,
            'year': group_object.start_date.year-1900,
            'month': group_object.start_date.month-1
        }
        end_date={
            'month_day': group_object.end_date.day,
            'year': group_object.end_date.year-1900,
            'month': group_object.end_date.month-1
        }
        group_start_date = dpg.add_date_picker(label="Start Date ", parent=window, default_value=start_date)
        group_end_date = dpg.add_date_picker(label="End Date ", parent=window, default_value=end_date)
        
        group = dpg.add_group(horizontal=True, parent=window)
        button = dpg.add_button(label="Save the group", callback=cls.modified_window_callback, parent=group)
        status = dpg.add_text(default_value="Status", parent=group)
        dpg.set_item_user_data(
            button, 
            {
                'window': window,
                'status': status, 
                'id': group_object.id,
                'items': [
                    {
                        'field': 'name',
                        'name': 'Group name',
                        'item': group_name,
                    },
                    {
                        'field': 'tour',
                        'name': 'Tour',
                        'item': group_tour,
                    },
                    {
                        'field': 'start_date',
                        'name': 'Start date',
                        'item': group_start_date,
                    },
                    {
                        'field': 'end_date',
                        'name': 'End date',
                        'item': group_end_date,
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
            
            tour_choice_value = request_data['tour']
            request_data['tour']  = int(request_data['tour'].split('|')[0])

            start_date = datetime(request_data['start_date']['year']+1900, request_data['start_date']['month']+1, request_data['start_date']['month_day'])
            end_date = datetime(request_data['end_date']['year']+1900, request_data['end_date']['month']+1, request_data['end_date']['month_day'])
            
            group_obj = Group(
                id = user_data['id'],
                name = request_data['name'],
                tour = request_data['tour'],
                start_date = start_date,
                end_date = end_date,
                revenue = 0,
                journey = []
            )

            group_bus = GroupBUS()
            error = group_bus.update(group_obj)
            
            if error.status is True:
                dpg.configure_item(user_data['status'], default_value=f'Status: {error.message}', color=[255, 92, 88])
            else:
                dpg.delete_item(user_data['window'])
                cls.content_render("group", default_choice=tour_choice_value)
        
    @classmethod
    def delete_window(cls, sender, app_data, user_data):
        group_id = user_data
        window = dpg.add_window(label="Modified the tour", width=400, autosize=True, pos=[500, 200])

        question = dpg.add_text(default_value=f"Do you want to delete the group (id: {group_id})?", parent=window)
        status = dpg.add_text(default_value="Status", parent=window)
        
        group = dpg.add_group(horizontal=True, parent=window)
        
        user_data = {
            'group_id': group_id,
            'status': status,
            'window': window
        }
        button_yes = dpg.add_button(label="Yes", callback=cls.delete_window_callback, user_data=user_data, parent=group)
        button_no = dpg.add_button(label="Cancel", callback=lambda :dpg.delete_item(window), parent=group)
        
    @classmethod
    def delete_window_callback(cls, sender, app_data, user_data):
        error = GroupBUS().delete(user_data['group_id'])
        if error.status is True:
            dpg.configure_item(user_data['status'], default_value=f'Status: {error.message}', color=[255, 92, 88])
        else:
            dpg.configure_item(user_data['status'], default_value=f'Status: OK', color=[128, 237, 153])
            dpg.delete_item(user_data['window'])
            cls.content_render('group')
            
    @classmethod
    def view_window(cls, sender, app_data, user_data):
        group = [g for g in GroupBUS().objects if g.id == user_data][0]

        tour = [f'{t.id} | {t.name}' for t in TourBUS().objects if t.id == group.tour][0]
        
        window = dpg.add_window(label="Modified the tour", width=400, autosize=True, pos=[500, 200])
        dpg.add_text(default_value=f"id: {group.id}", parent=window)
        dpg.add_text(default_value=f"Name: {group.name}", parent=window)
        dpg.add_text(default_value=f"Tour: {tour}", parent=window)
        dpg.add_text(default_value=f"Start date: {group.start_date}", parent=window)
        dpg.add_text(default_value=f"End date: {group.end_date}", parent=window)
        dpg.add_text(default_value=f"Journey:", parent=window)
        
        for journey in group.journey:
                start_hour = "{:02d}h{:02d}".format(journey.start_date.hour, journey.start_date.minute)
                end_hour = "{:02d}h{:02d}".format(journey.end_date.hour, journey.end_date.minute)
                journey =  start_hour + " - " + end_hour + ": " + journey.content + "\n"
                
                dpg.add_text(default_value=journey, bullet=True, parent=window)

        dpg.add_text(default_value=f"Revenue: {group.revenue}", parent=window)

        group_bottom = dpg.add_group(horizontal=True, parent=window)
        dpg.add_button(label="Customers", callback=lambda :cls.customers_callback(group.id), parent=group_bottom)
        dpg.add_button(label="Staffs", callback=lambda :cls.staffs_callback(group.id), parent=group_bottom)
        dpg.add_button(label="Close", callback=lambda :dpg.delete_item(window), parent=group_bottom)

    @classmethod
    def customers_callback(cls, sender):
        group_customer_bus = GroupCustomerBUS()
        group_customer=group_customer_bus.read(sender)

        window = dpg.add_window(label="Customers of the group", width=600, height=325, pos=[500, 200])
        header = ['id', 'name', 'id number', "address", "gender", "phone number"]
        type_columns = [int, str, str, str, str, str]
        data = []
        customer_bus = CustomerBUS()

        for gc in group_customer:
            customer = [c for c in customer_bus.objects if c.id == gc.customer][0]
            data.append([
                customer.id,
                customer.name,
                customer.id_number,
                customer.address,
                customer.gender,
                customer.phone_number
            ])

        table = dpg.add_table(
            header_row=True, 
            borders_innerH=True, 
            borders_outerH=True,
            borders_innerV=True, 
            borders_outerV=True, 
            row_background=True,
            resizable=True,
            sortable=True,
            hideable=True,
            precise_widths=True,
            no_host_extendX=True,
            callback=None,
            parent=window,
            height=200)

        type_column_map = {}
    
        for ind, column in enumerate(header):
            col = dpg.add_table_column(label=column, width_fixed=True, parent=table)
            if type_columns:
                type_column_map[col] = (ind, type_columns[ind])

        dpg.add_table_column(label="Action", parent=table, no_sort=True)

        for row in data:
            table_row = dpg.add_table_row(parent=table)
            for d in row:
                dpg.add_text(d, parent=table_row)

            remove_customer_button = dpg.add_button(label='Remove', parent=table_row, callback=cls.remove_customer)
            dpg.set_item_user_data(
                remove_customer_button,
                {
                    'window': window,
                    'group_id': sender,
                    'customer_id': row[0]
                }
            )
        
        customer_bus = CustomerBUS()
        customers = [f'{c.id} | {c.name}' for c in customer_bus.objects]
        customer_combo = dpg.add_combo(label='Customer', parent=window, items=customers, default_value=customers[0])
        status = dpg.add_text(default_value="Status", parent=window)
        bottom_group = dpg.add_group(horizontal=True, parent=window)
        add_customer_button = dpg.add_button(label="Add customer", parent=bottom_group, callback=cls.add_customer_callback)
        dpg.add_button(label="Close", parent=bottom_group, callback=lambda :dpg.delete_item(window))
        dpg.set_item_user_data(
            add_customer_button,
            {
                'window': window,
                'status': status,
                'group_id': sender,
                'customer': customer_combo
            }
        )

    @classmethod
    def remove_customer(cls, sender, app_data, user_data):
        window = dpg.add_window(label="Remove the customer from group", width=400, autosize=True, pos=[500, 200])
        question = dpg.add_text(default_value=f"Do you want to remove the customer (id: {user_data['customer_id']} from ther group (id: {user_data['group_id']})?", parent=window)
        status = dpg.add_text(default_value="Status", parent=window)
        
        group = dpg.add_group(horizontal=True, parent=window)
        
        user_data = {
            'group_id': user_data['group_id'],
            'customer_id': user_data['customer_id'],
            'status': status,
            'question_window': window,
            'customer_window': user_data['window']

        }
        button_yes = dpg.add_button(label="Yes", callback=cls.remove_customer_callback, user_data=user_data, parent=group)
        button_no = dpg.add_button(label="Cancel", callback=lambda :dpg.delete_item(window), parent=group)

    @classmethod
    def remove_customer_callback(cls, sender, app_data, user_data):
        group_customer_bus = GroupCustomerBUS()
        error = group_customer_bus.delete(user_data['group_id'], user_data['customer_id'])
        if error.status is True:
            dpg.configure_item(user_data['status'], default_value=f'Status: {error.message}', color=[255, 92, 88])
        else:
            dpg.configure_item(user_data['status'], default_value=f'Status: OK', color=[128, 237, 153])
            dpg.delete_item(user_data['question_window'])            
            cls.customers_callback(user_data['group_id'])
            dpg.delete_item(user_data['customer_window'])


    @classmethod
    def add_customer_callback(cls, sender, app_data, user_data):
        customer_id = int(dpg.get_value(user_data['customer']).split('|')[0])
        group_customer_bus = GroupCustomerBUS()
        group_customer_obj = GroupCustomer(
            id = 0,
            group = user_data['group_id'],
            customer = customer_id
        )
        error = group_customer_bus.create(group_customer_obj)
        if error.status is True:
            dpg.configure_item(user_data['status'], default_value=f'Status: {error.message}', color=[255, 92, 88])
        else:
            cls.customers_callback(user_data['group_id'])
            dpg.delete_item(user_data['window'])

    @classmethod
    def search_callback(cls,sender, app_data, user_data):
        tour_id = int(dpg.get_value(user_data['tour']).split('|')[0])

        group_bus = GroupBUS()
        group = [ g for g in group_bus.objects if g.tour == tour_id]
        header = ['id', 'name', 'start_date', "end_date", "revenue", "journey"]
        datetime_type = lambda d: datetime.strptime(d, '%Y-%m-%d')
        type_columns = [int, str, datetime_type, datetime_type, int, str]
        data = []
        column_search = dpg.get_value(user_data['column'])
        if (column_search == 'all'):
            for g in group:
                start_date_string = g.start_date.strftime("%Y-%m-%d")
                end_date_string = g.end_date.strftime("%Y-%m-%d")
                multi_strings = f"{g.id} | {g.name} | {start_date_string} | {end_date_string} | {g.revenue}"
                search = re.search(app_data, multi_strings)
                if (search):
                    data.append([
                        g.id,
                        g.name,
                        g.start_date.strftime("%Y-%m-%d"),
                        g.end_date.strftime("%Y-%m-%d"),
                        g.revenue
                    ])
        if (column_search == 'name'):
            for g in group:
                search = re.search(app_data, g.name)
                if (search):
                    data.append([
                        g.id,
                        g.name,
                        g.start_date.strftime("%Y-%m-%d"),
                        g.end_date.strftime("%Y-%m-%d"),
                        g.revenue
                    ])
        if (column_search == 'start_date'):
            for g in group:
                search = re.search(app_data, g.start_date.strftime("%Y-%m-%d"))
                if (search):
                    data.append([
                        g.id,
                        g.name,
                        g.start_date.strftime("%Y-%m-%d"),
                        g.end_date.strftime("%Y-%m-%d"),
                        g.revenue
                    ])
        if (column_search == 'end_date'):
            for g in group:
                search = re.search(app_data, g.end_date.strftime("%Y-%m-%d"))
                if (search):
                    data.append([
                        g.id,
                        g.name,
                        g.start_date.strftime("%Y-%m-%d"),
                        g.end_date.strftime("%Y-%m-%d"),
                        g.revenue
                    ])
        if (column_search == 'revenue'):
            for g in group:
                search = re.search(app_data, str(g.revenue))
                if (search):
                    data.append([
                        g.id,
                        g.name,
                        g.start_date.strftime("%Y-%m-%d"),
                        g.end_date.strftime("%Y-%m-%d"),
                        g.revenue
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

    @classmethod
    def staffs_callback(cls, sender):
        group_staff_bus = GroupStaffBUS()
        group_staff = group_staff_bus.group_objects(sender)

        window = dpg.add_window(label="Staff of the group", width=600, height=350, pos=[500, 200])
        header = ['id', 'staff', 'staff_type']
        type_columns = [int, str, str]
        data = []

        for gs in group_staff:
            data.append([
                gs.id,
                gs.staff.name,
                gs.staff_type.name
            ])

        table = dpg.add_table(
            header_row=True, 
            borders_innerH=True, 
            borders_outerH=True,
            borders_innerV=True, 
            borders_outerV=True, 
            row_background=True,
            resizable=True,
            sortable=True,
            hideable=True,
            precise_widths=True,
            no_host_extendX=True,
            callback=None,
            parent=window,
            height=200)

        type_column_map = {}
    
        for ind, column in enumerate(header):
            col = dpg.add_table_column(label=column, width_fixed=True, parent=table)
            if type_columns:
                type_column_map[col] = (ind, type_columns[ind])

        dpg.add_table_column(label="Action", parent=table, no_sort=True)

        for row in data:
            table_row = dpg.add_table_row(parent=table)
            for d in row:
                dpg.add_text(d, parent=table_row)

            remove_staff_button = dpg.add_button(label='Remove', parent=table_row, callback=cls.remove_staff)
            group_staff_row = [gs for gs in group_staff if gs.id == row[0]][0]
            dpg.set_item_user_data(
                remove_staff_button,
                {
                    'window': window,
                    'group_id': sender,
                    'staff_id': group_staff_row.staff.id
                }
            )
        
        staff_bus = StaffBUS()
        staffs = [f'{s.id} | {s.name}' for s in staff_bus.objects]
        staff_type_bus = StaffTypeBUS()
        staff_types = [f'{st.id} | {st.name}' for st in staff_type_bus.objects]
        staff_combo = dpg.add_combo(label='Staff', parent=window, items=staffs, default_value=staffs[0])
        staff_type_combo = dpg.add_combo(label='Staff type', parent=window, items=staff_types, default_value=staff_types[0])
        status = dpg.add_text(default_value="Status", parent=window)
        bottom_group = dpg.add_group(horizontal=True, parent=window)
        add_customer_button = dpg.add_button(label="Add customer", parent=bottom_group, callback=cls.add_staff_callback)
        dpg.add_button(label="Close", parent=bottom_group, callback=lambda :dpg.delete_item(window))
        dpg.set_item_user_data(
            add_customer_button,
            {
                'window': window,
                'status': status,
                'group_id': sender,
                'staff': staff_combo,
                'staff_type': staff_type_combo
            }
        )

    @classmethod
    def remove_staff(cls, sender, app_data, user_data):
        window = dpg.add_window(label="Remove the customer from group", width=400, autosize=True, pos=[500, 200])
        question = dpg.add_text(default_value=f"Do you want to remove the staff (id: {user_data['staff_id']} from ther group (id: {user_data['group_id']})?", parent=window)
        status = dpg.add_text(default_value="Status", parent=window)
        
        group = dpg.add_group(horizontal=True, parent=window)
        
        user_data = {
            'group_id': user_data['group_id'],
            'staff_id': user_data['staff_id'],
            'status': status,
            'question_window': window,
            'staff_window': user_data['window']

        }
        button_yes = dpg.add_button(label="Yes", callback=cls.remove_staff_callback, user_data=user_data, parent=group)
        button_no = dpg.add_button(label="Cancel", callback=lambda :dpg.delete_item(window), parent=group)

    @classmethod
    def remove_staff_callback(cls, sender, app_data, user_data):
        group_staff_bus = GroupStaffBUS()
        error = group_staff_bus.delete(user_data['group_id'], user_data['staff_id'])
        if error.status is True:
            dpg.configure_item(user_data['status'], default_value=f'Status: {error.message}', color=[255, 92, 88])
        else:
            dpg.configure_item(user_data['status'], default_value=f'Status: OK', color=[128, 237, 153])
            dpg.delete_item(user_data['question_window'])            
            cls.staffs_callback(user_data['group_id'])
            dpg.delete_item(user_data['staff_window'])

    @classmethod
    def add_staff_callback(cls, sender, app_data, user_data):
        staff_id = int(dpg.get_value(user_data['staff']).split('|')[0])
        staff_type_id = int(dpg.get_value(user_data['staff_type']).split('|')[0])
        group_staff_bus = GroupStaffBUS()
        group_staff_obj = GroupStaff(
            id = 0,
            group = Group(user_data['group_id'], None, None, None, None, None, None),
            staff = Staff(staff_id, None),
            staff_type = StaffType(staff_type_id, None)
        )
        error = group_staff_bus.create(group_staff_obj)
        if error.status is True:
            dpg.configure_item(user_data['status'], default_value=f'Status: {error.message}', color=[255, 92, 88])
        else:
            cls.staffs_callback(user_data['group_id'])
            dpg.delete_item(user_data['window'])


        
        


        

        
