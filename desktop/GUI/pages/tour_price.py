from datetime import datetime

import dearpygui.dearpygui as dpg
from BUS.tour import TourPriceBUS
from DTO.tour import TourPrice

from ..base_table import init_table


class TourPriceGUI:
    group_content_window = None

    @classmethod
    def content_render(cls, data):
        dpg.delete_item(cls.group_content_window, children_only=True)
        dpg.add_text(default_value=data, parent=cls.group_content_window)
        
        top_group = dpg.add_group(horizontal=True, parent=cls.group_content_window)
        dpg.add_button(label="Add new price", callback=cls.create_window, parent=top_group)
        dpg.add_input_text(label="Search", parent=top_group)
        dpg.add_combo(label="Columns", items=['column1', 'column2', 'column3'], parent=top_group)
        
        header = ['id', 'name', 'price', 'start_date', 'end_date']
        datetime_type = lambda d: datetime.strptime(d, '%Y-%m-%d')
        type_columns = [int, str, int, datetime_type, datetime_type]
        data = []
        tour_price_bus = TourPriceBUS()
        tour_price_data = tour_price_bus.objects
        
        for d in tour_price_data:
            data.append([
                d.id,
                d.name,
                d.price,
                d.start_date.strftime("%Y-%m-%d"),
                d.end_date.strftime("%Y-%m-%d")
            ])
        
        table = init_table(
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
        window = dpg.add_window(label="Add new price", width=400, autosize=True, pos=[500, 200])
        tour_price_name = dpg.add_input_text(label="Name ", parent=window)
        tour_price_price = dpg.add_input_int(label="Price ", parent=window)
        tour_start_date = dpg.add_date_picker(label='Start Date', parent=window)
        tour_end_date = dpg.add_date_picker(label='End Date', parent=window)
        
        
        group = dpg.add_group(horizontal=True, parent=window)
        button = dpg.add_button(label="Add new price", callback=cls.create_window_callback, parent=group)
        status = dpg.add_text(default_value="Status", parent=group)
        dpg.set_item_user_data(
            button, 
            {
                'window': window,
                'status': status, 
                'items': [
                    {
                        'field': 'name',
                        'name': 'Price name',
                        'item': tour_price_name,
                    },
                    {
                        'field': 'price',
                        'name': 'Price price',
                        'item': tour_price_price,
                    },
                    {
                        'field': 'start_date',
                        'name': 'Price start date',
                        'item': tour_start_date,
                    },
                    {
                        'field': 'end_date',
                        'name': 'Price end date',
                        'item': tour_end_date,
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
                if item['field'] in ('start_date', 'end_date'):
                    data = f"{data['year'] + 1900}-{data['month'] + 1}-{data['month_day']}" 
                request_data[item['field']] = data
            else:
                is_valid = False
                dpg.configure_item(user_data['status'], default_value=f'Status: {item["name"]} is invalid', color=[255, 92, 88])               
                break
            
        if is_valid:
            dpg.configure_item(user_data['status'], default_value=f'Status: OK', color=[128, 237, 153])
            
            start_date = datetime.strptime(request_data['start_date'], '%Y-%m-%d')
            end_date = datetime.strptime(request_data['end_date'], '%Y-%m-%d')
            
            tour_obj = TourPrice(
                id=0,
                name=request_data['name'],
                price=request_data['price'],
                start_date=start_date,
                end_date=end_date,
            ) 
            tour_price_bus = TourPriceBUS()
            error = tour_price_bus.create(tour_obj)
            
            if error.status is True:
                dpg.configure_item(user_data['status'], default_value=f'Status: {error.message}', color=[255, 92, 88])
            else:
                dpg.delete_item(user_data['window'])
                cls.content_render("tour_price")
                
    @classmethod
    def modified_window(cls, sender, app_data, user_data):
        tour_prices = TourPriceBUS().objects
        
        tour_price = [t for t in tour_prices if t.id == user_data][0]
        
        window = dpg.add_window(label="Modified the price", width=400, autosize=True, pos=[500, 200])
        dpg.add_text(default_value=f"id: {tour_price.id}", parent=window)
        price_name = dpg.add_input_text(label="Name ", parent=window, default_value=tour_price.name)
        price_price = dpg.add_input_int(label="Price ", parent=window, default_value=tour_price.price)
        price_start_date = dpg.add_date_picker(label='Start Date', parent=window, default_value={'month': tour_price.start_date.month - 1, 'year':tour_price.start_date.year - 1900, 'month_day':tour_price.start_date.day})
        price_end_date = dpg.add_date_picker(label='End Date', parent=window, default_value={'month': tour_price.end_date.month - 1, 'year':tour_price.end_date.year - 1900, 'month_day':tour_price.end_date.day})
        
        group = dpg.add_group(horizontal=True, parent=window)
        button = dpg.add_button(label="Save the price", callback=cls.modified_window_callback, parent=group)
        status = dpg.add_text(default_value="Status", parent=group)
        dpg.set_item_user_data(
            button, 
            {
                'window': window,
                'status': status, 
                'id': tour_price.id,
                'items': [
                    {
                        'field': 'name',
                        'name': 'Price name',
                        'item': price_name,
                    },
                    {
                        'field': 'price',
                        'name': 'Price price',
                        'item': price_price,
                    },
                    {
                        'field': 'start_date',
                        'name': 'Price start date',
                        'item': price_start_date,
                    },
                    {
                        'field': 'end_date',
                        'name': 'Price end date',
                        'item': price_end_date,
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
                if item['field'] in ('start_date', 'end_date'):
                    data = f"{data['year'] + 1900}-{data['month'] + 1}-{data['month_day']}" 
                request_data[item['field']] = data
            else:
                is_valid = False
                dpg.configure_item(user_data['status'], default_value=f'Status: {item["name"]} is invalid', color=[255, 92, 88])               
                break
            
        if is_valid:
            dpg.configure_item(user_data['status'], default_value=f'Status: OK', color=[128, 237, 153])
            
            start_date = datetime.strptime(request_data['start_date'], '%Y-%m-%d')
            end_date = datetime.strptime(request_data['end_date'], '%Y-%m-%d')
            
            tour_price_obj = TourPrice(
                id=user_data['id'],
                name=request_data['name'],
                price=request_data['price'],
                start_date=start_date,
                end_date=end_date,
            ) 
            tour_price_bus = TourPriceBUS()
            error = tour_price_bus.update(tour_price_obj)
            
            if error.status is True:
                dpg.configure_item(user_data['status'], default_value=f'Status: {error.message}', color=[255, 92, 88])
            else:
                dpg.delete_item(user_data['window'])
                cls.content_render('tour_price')
        
    @classmethod
    def delete_window(cls, sender, app_data, user_data):
        tour_price_id = user_data
        window = dpg.add_window(label="Delete the price", width=400, autosize=True, pos=[500, 200])

        question = dpg.add_text(default_value=f"Do you want to delete the price (id: {tour_price_id})?", parent=window)
        status = dpg.add_text(default_value="Status", parent=window)
        
        group = dpg.add_group(horizontal=True, parent=window)
        
        user_data = {
            'tour_price_id': tour_price_id,
            'status': status,
            'window': window
        }
        button_yes = dpg.add_button(label="Yes", callback=cls.delete_window_callback, user_data=user_data, parent=group)
        button_no = dpg.add_button(label="Cancel", callback=lambda :dpg.delete_item(window), parent=group)
        
    @classmethod
    def delete_window_callback(cls, sender, app_data, user_data):
        error = TourPriceBUS().delete(user_data['tour_price_id'])
        if error.status is True:
            dpg.configure_item(user_data['status'], default_value=f'Status: {error.message}', color=[255, 92, 88])
        else:
            dpg.configure_item(user_data['status'], default_value=f'Status: OK', color=[128, 237, 153])
            dpg.delete_item(user_data['window'])
            cls.content_render('tour_price')
            
    @classmethod
    def view_window(cls, sender, app_data, user_data):
        tour_prices = TourPriceBUS().objects
        tour_price = [t for t in tour_prices if t.id == user_data][0]
        
        window = dpg.add_window(label="View the Price", width=400, autosize=True, pos=[500, 200])
        dpg.add_text(default_value=f"id: {tour_price.id}", parent=window)
        dpg.add_text(default_value=f"Name: {tour_price.name}", parent=window)
        dpg.add_text(default_value=f"Price: {tour_price.price}", parent=window)
        dpg.add_text(default_value=f"Start date: {tour_price.start_date.strftime('%Y-%m-%d')}", parent=window)
        dpg.add_text(default_value=f"End date: {tour_price.end_date.strftime('%Y-%m-%d')}", parent=window)
        dpg.add_button(label="Close", callback=lambda :dpg.delete_item(window), parent=window)
