import dearpygui.dearpygui as dpg

from ..base_table import init_table
from BUS.tour import TourBUS, TourCharacteristicBUS, TourTypeBUS, TourPriceBUS, LocationBUS
from DTO.tour import Tour, TourCharacteristic, TourType, TourPrice, Location


class TourTourGUI:
    group_content_window = None

    @classmethod
    def content_render(cls, data):
        dpg.delete_item(cls.group_content_window, children_only=True)
        dpg.add_text(default_value=data, parent=cls.group_content_window)
        
        top_group = dpg.add_group(horizontal=True, parent=cls.group_content_window)
        dpg.add_button(label="Add new tour", callback=cls.create_window, parent=top_group)
        dpg.add_input_text(label="Search", parent=top_group)
        dpg.add_combo(label="Columns", items=['column1', 'column2', 'column3'], parent=top_group)
        
        header = ['id', 'name', 'characteristic', "type", "price", "location"]
        data = []
        width_columns = [32, 148, 100, 110, 50, 104]
        tour_bus = TourBUS()
        tour_data = tour_bus.objects
        
        for d in tour_data:
            data.append([
                d.id,
                d.name,
                d.characteristic.name,
                d.type.name,
                d.price.price,
                d.location.name
            ])
        
        table = init_table(
            header=header,
            data=data,
            parent=cls.group_content_window,
            width_columns=width_columns,
            is_action=True,
            modified_callback=cls.modified_window,
            delete_callback=cls.delete_window,
            view_callback=cls.view_window
        )
        
    @classmethod
    def create_window(cls):
        window = dpg.add_window(label="Add new tour", width=400, autosize=True, pos=[500, 200])
        tour_name = dpg.add_input_text(label="Name ", parent=window)
        
        tour_characteristics    = TourCharacteristicBUS().objects
        tour_types              = TourTypeBUS().objects
        tour_prices             = TourPriceBUS().objects
        locations               = LocationBUS().objects
        
        tour_characteristics    = [f'{d.id} | {d.name}' for d in tour_characteristics]
        tour_types              = [f'{d.id} | {d.name}' for d in tour_types]
        tour_prices             = [f'{d.id} | {d.name}' for d in tour_prices]
        locations               = [f'{d.id} | {d.name}' for d in locations]
        
        tour_characteristics    = dpg.add_combo(label="Characteristic", items=tour_characteristics, parent=window)
        tour_types              = dpg.add_combo(label="Type", items=tour_types, parent=window)
        tour_prices             = dpg.add_combo(label="Price", items=tour_prices, parent=window)
        locations               = dpg.add_combo(label="Location", items=locations, parent=window)
        
        group = dpg.add_group(horizontal=True, parent=window)
        button = dpg.add_button(label="Add new tour", callback=cls.create_window_callback, parent=group)
        status = dpg.add_text(default_value="Status", parent=group)
        dpg.set_item_user_data(
            button, 
            {
                'window': window,
                'status': status, 
                'items': [
                    {
                        'field': 'name',
                        'name': 'Tour name',
                        'item': tour_name,
                    },
                    {
                        'field': 'characteristic',
                        'name': 'Tour characteristic',
                        'item': tour_characteristics,
                    },
                    {
                        'field': 'type',
                        'name': 'Tour type',
                        'item': tour_types,
                    },
                    {
                        'field': 'price',
                        'name': 'Tour price',
                        'item': tour_prices,
                    },
                    {
                        'field': 'location',
                        'name': 'Location',
                        'item': locations,
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
            
            request_data['characteristic']  = int(request_data['characteristic'].split('|')[0])        
            request_data['type']            = int(request_data['type'].split('|')[0])        
            request_data['price']           = int(request_data['price'].split('|')[0])        
            request_data['location']        = int(request_data['location'].split('|')[0])    
            
            print(request_data)
            
            tour_obj = Tour(
                id=0,
                name=request_data['name'],
                characteristic=TourCharacteristic(request_data['characteristic'], None),
                type=TourType(request_data['type'], None),
                price=TourPrice(request_data['price'], None, None, None, None),
                location=Location(request_data['location'], None, None, None)
            ) 
            tour_bus = TourBUS()
            error = tour_bus.create(tour_obj)
            
            if error.status is True:
                dpg.configure_item(user_data['status'], default_value=f'Status: {error.message}', color=[255, 92, 88])
            else:
                dpg.delete_item(user_data['window'])
                cls.content_render("tour")
                
    @classmethod
    def modified_window(cls, sender, app_data, user_data):
        tours = TourBUS().objects
        
        tour = [t for t in tours if t.id == user_data][0]
        
        window = dpg.add_window(label="Modified the tour", width=400, autosize=True, pos=[500, 200])
        tour_id = dpg.add_text(default_value=f"id: {tour.id}", parent=window)
        tour_name = dpg.add_input_text(label="Name ", parent=window, default_value=tour.name)
        
        tour_characteristics    = TourCharacteristicBUS().objects
        tour_types              = TourTypeBUS().objects
        tour_prices             = TourPriceBUS().objects
        locations               = LocationBUS().objects
        
        tour_characteristics    = [f'{d.id} | {d.name}' for d in tour_characteristics]
        tour_types              = [f'{d.id} | {d.name}' for d in tour_types]
        tour_prices             = [f'{d.id} | {d.name}' for d in tour_prices]
        locations               = [f'{d.id} | {d.name}' for d in locations]
        
        tour_characteristics    = dpg.add_combo(label="Characteristic", items=tour_characteristics, default_value=f'{tour.characteristic.id} | {tour.characteristic.name}', parent=window)
        tour_types              = dpg.add_combo(label="Type", items=tour_types, default_value=f'{tour.type.id} | {tour.type.name}', parent=window)
        tour_prices             = dpg.add_combo(label="Price", items=tour_prices, default_value=f'{tour.price.id} | {tour.price.name}', parent=window)
        locations               = dpg.add_combo(label="Location", items=locations, default_value=f'{tour.location.id} | {tour.location.name}', parent=window)
        
        group = dpg.add_group(horizontal=True, parent=window)
        button = dpg.add_button(label="Save the tour", callback=cls.modified_window_callback, parent=group)
        status = dpg.add_text(default_value="Status", parent=group)
        dpg.set_item_user_data(
            button, 
            {
                'window': window,
                'status': status, 
                'id': tour.id,
                'items': [
                    {
                        'field': 'name',
                        'name': 'Tour name',
                        'item': tour_name,
                    },
                    {
                        'field': 'characteristic',
                        'name': 'Tour characteristic',
                        'item': tour_characteristics,
                    },
                    {
                        'field': 'type',
                        'name': 'Tour type',
                        'item': tour_types,
                    },
                    {
                        'field': 'price',
                        'name': 'Tour price',
                        'item': tour_prices,
                    },
                    {
                        'field': 'location',
                        'name': 'Location',
                        'item': locations,
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
            
            request_data['characteristic']  = int(request_data['characteristic'].split('|')[0])        
            request_data['type']            = int(request_data['type'].split('|')[0])        
            request_data['price']           = int(request_data['price'].split('|')[0])        
            request_data['location']        = int(request_data['location'].split('|')[0])    
            
            print(request_data)
            
            tour_obj = Tour(
                id=user_data['id'],
                name=request_data['name'],
                characteristic=TourCharacteristic(request_data['characteristic'], None),
                type=TourType(request_data['type'], None),
                price=TourPrice(request_data['price'], None, None, None, None),
                location=Location(request_data['location'], None, None, None)
            ) 
            tour_bus = TourBUS()
            error = tour_bus.update(tour_obj)
            
            if error.status is True:
                dpg.configure_item(user_data['status'], default_value=f'Status: {error.message}', color=[255, 92, 88])
            else:
                dpg.delete_item(user_data['window'])
                cls.content_render('tour')
        
    @classmethod
    def delete_window(cls, sender, app_data, user_data):
        tour_id = user_data
        window = dpg.add_window(label="Modified the tour", width=400, autosize=True, pos=[500, 200])

        question = dpg.add_text(default_value=f"Do you want to delete the tour (id: {tour_id})?", parent=window)
        status = dpg.add_text(default_value="Status", parent=window)
        
        group = dpg.add_group(horizontal=True, parent=window)
        
        user_data = {
            'tour_id': tour_id,
            'status': status,
            'window': window
        }
        button_yes = dpg.add_button(label="Yes", callback=cls.delete_window_callback, user_data=user_data, parent=group)
        button_no = dpg.add_button(label="Cancel", callback=lambda :dpg.delete_item(window), parent=group)
        
    @classmethod
    def delete_window_callback(cls, sender, app_data, user_data):
        error = TourBUS().delete(user_data['tour_id'])
        if error.status is True:
            dpg.configure_item(user_data['status'], default_value=f'Status: {error.message}', color=[255, 92, 88])
        else:
            dpg.configure_item(user_data['status'], default_value=f'Status: OK', color=[128, 237, 153])
            dpg.delete_item(user_data['window'])
            cls.content_render('tour')
            
    @classmethod
    def view_window(cls, sender, app_data, user_data):
        tours = TourBUS().objects
        tour = [t for t in tours if t.id == user_data][0]
        
        window = dpg.add_window(label="Modified the tour", width=400, autosize=True, pos=[500, 200])
        dpg.add_text(default_value=f"id: {tour.id}", parent=window)
        dpg.add_text(default_value=f"Name: {tour.name}", parent=window)
        dpg.add_text(default_value=f"Characteristic: {tour.characteristic.id} | {tour.characteristic.name}", parent=window)
        dpg.add_text(default_value=f"Type: {tour.type.id} | {tour.type.name}", parent=window)
        dpg.add_text(default_value=f"Price: {tour.price.id} | {tour.price.name}", parent=window)
        dpg.add_text(default_value=f"Location: {tour.location.id} | {tour.location.name}", parent=window)
        dpg.add_button(label="Close", callback=lambda :dpg.delete_item(window), parent=window)