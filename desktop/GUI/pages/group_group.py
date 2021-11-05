from datetime import date, datetime

import dearpygui.dearpygui as dpg
from BUS.group import GroupBUS, GroupJourneyBUS
from BUS.tour import TourBUS
from DTO.group import Group, GroupJourney

from ..base_table import init_table


class GroupGroupGUI:
    group_content_window = None
    table = None

    @classmethod
    def content_render(cls, data):
        dpg.delete_item(cls.group_content_window, children_only=True)
        
        tours = [f'{t.id} | {t.name}' for t in TourBUS().objects]
        
        high_top_group = dpg.add_group(horizontal=True, parent=cls.group_content_window)
        dpg.add_text(default_value=data, parent=high_top_group)
        dpg.add_combo(label="Tour", items=tours, parent=high_top_group, callback=cls.choice_tour_combo)
        
        top_group = dpg.add_group(horizontal=True, parent=cls.group_content_window)
        dpg.add_button(label="Add new group", callback=cls.create_window, parent=top_group)
        dpg.add_input_text(label="Search", parent=top_group)
        dpg.add_combo(label="Columns", items=['column1', 'column2', 'column3'], parent=top_group)
        
    @classmethod
    def choice_tour_combo(cls, sender, app_data):
        tour_id = int(app_data.split('|')[0])
        
        header = ['id', 'name', 'start_date', "end_date", "revenue"]
        datetime_type = lambda d: datetime.strptime(d, '%Y-%m-%d')
        type_columns = [int, str, datetime_type, datetime_type, int, str]
        data = []
        group_bus = GroupBUS()
        group_data = [g for g in group_bus.objects if g.tour == tour_id]
        print(group_bus.objects[0].start_date)
        
        for d in group_data:
            data.append([
                d.id,
                d.name,
                d.start_date.strftime("%Y-%m-%d"),
                d.end_date.strftime("%Y-%m-%d"),
                d.revenue
            ])
        
        if cls.table is not None:
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
        
    @classmethod
    def create_window(cls):
        window = dpg.add_window(label="Add new group", width=400, autosize=True, pos=[500, 200])
        group_name = dpg.add_input_text(label="Name ", parent=window)

        tours = [f'{t.id} | {t.name}' for t in TourBUS().objects]
        group_tour = dpg.add_combo(label="Tour", items=tours, parent=window)

        datenow = {
            'month_day': date.today().day,
            'year': date.today().year-1970+70,
            'month': date.today().month-1
        }
        group_start_date = dpg.add_date_picker(label="Start Date ", parent=window, default_value=datenow)
        group_end_date = dpg.add_date_picker(label="End Date ", parent=window, default_value=datenow)
        group_revenue = dpg.add_input_text(label="Revenue ", parent=window)
        
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
                    },
                    {
                        'field': 'revenue',
                        'name': 'Revenue',
                        'item': group_revenue,
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
            print(request_data)
            
            request_data['tour']  = int(request_data['tour'].split('|')[0])

            start_date = datetime(request_data['start_date']['year']-70+1970, request_data['start_date']['month']+1, request_data['start_date']['month_day'])
            end_date = datetime(request_data['end_date']['year']-70+1970, request_data['end_date']['month']+1, request_data['end_date']['month_day'])

            request_data['revenue'] = int(request_data['revenue'])
            
            group_obj = Group(
                id = 0,
                name = request_data['name'],
                tour = request_data['tour'],
                start_date = start_date,
                end_date = end_date,
                revenue = request_data['revenue'],
                journey = []
            )

            group_bus = GroupBUS()
            error = group_bus.create(group_obj)
            
            if error.status is True:
                dpg.configure_item(user_data['status'], default_value=f'Status: {error.message}', color=[255, 92, 88])
            else:
                dpg.delete_item(user_data['window'])
                cls.content_render("group")
                
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
            'year': group_object.start_date.year-1970+70,
            'month': group_object.start_date.month-1
        }
        end_date={
            'month_day': group_object.end_date.day,
            'year': group_object.end_date.year-1970+70,
            'month': group_object.end_date.month-1
        }
        group_start_date = dpg.add_date_picker(label="Start Date ", parent=window, default_value=start_date)
        group_end_date = dpg.add_date_picker(label="End Date ", parent=window, default_value=end_date)
        group_revenue = dpg.add_input_text(label="Revenue ", parent=window, default_value=group_object.revenue)
        
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
                    },
                    {
                        'field': 'revenue',
                        'name': 'Revenue',
                        'item': group_revenue,
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
            print(request_data)
            
            request_data['tour']  = int(request_data['tour'].split('|')[0])

            start_date = datetime(request_data['start_date']['year']-70+1970, request_data['start_date']['month']+1, request_data['start_date']['month_day'])
            end_date = datetime(request_data['end_date']['year']-70+1970, request_data['end_date']['month']+1, request_data['end_date']['month_day'])

            request_data['revenue'] = int(request_data['revenue'])
            
            group_obj = Group(
                id = user_data['id'],
                name = request_data['name'],
                tour = request_data['tour'],
                start_date = start_date,
                end_date = end_date,
                revenue = request_data['revenue'],
                journey = []
            )

            group_bus = GroupBUS()
            error = group_bus.update(group_obj)
            
            if error.status is True:
                dpg.configure_item(user_data['status'], default_value=f'Status: {error.message}', color=[255, 92, 88])
            else:
                dpg.delete_item(user_data['window'])
                cls.content_render("group")
        
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
        journey = ""
        for j in group.journey:
                start_hour = str(j.start_date.hour) + " h " + str(j.start_date.minute)
                end_hour = str(j.end_date.hour) + " h " + str(j.end_date.minute)
                journey +=  start_hour + " - " + end_hour + ": " + j.content + "\n"
        dpg.add_text(default_value=f"Journey: {journey}", parent=window)
        dpg.add_text(default_value=f"Revenue: {group.revenue}", parent=window)
        dpg.add_button(label="Close", callback=lambda :dpg.delete_item(window), parent=window)
