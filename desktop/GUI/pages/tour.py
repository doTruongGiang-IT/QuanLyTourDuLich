import dearpygui.dearpygui as dpg

from ..base_table import init_table
from BUS.tour import TourBUS, TourCharacteristicBUS, TourTypeBUS, TourPriceBUS, LocationBUS
from DTO.tour import Tour, TourCharacteristic, TourType, TourPrice, Location


class TourGUI:
    content_window = "content_window"
    group_content_window = None
    CONTENT_TAB_BAR = [
        ["tour_tab_bar_menu_window", "Tour", "tour_render"],
        ["tour_characteristic_tab_bar_menu_window", "Tour Characteristic", "tour_characteristic_render"],
        ["tour_type_tab_bar_menu_window", "Tour Type", "tour_type_render"],
        ["tour_price_tab_bar_menu_window", "Tour Price", "tour_price_render"],
        ["location_tab_bar_menu_window", "Location", "location_render"]
    ]
    
    @classmethod
    def tab_bar_call_back(cls, sender, data):
        for tab in cls.CONTENT_TAB_BAR:
            if dpg.get_item_label(data) == tab[1]:
                getattr(cls, tab[2])(tab[1])
                break
    
    @classmethod    
    def init_content_window(cls):
        cls.delete_window()
        tab_bar = dpg.add_tab_bar(parent=cls.content_window, callback=cls.tab_bar_call_back)
        for tab in cls.CONTENT_TAB_BAR:
            dpg.add_tab(label=tab[1], parent=tab_bar)
            
        cls.group_content_window = dpg.add_group(parent=cls.content_window)
                
    @classmethod
    def delete_window(cls):
        dpg.delete_item(cls.content_window, children_only=True)
    
    @classmethod
    def delete_group(cls, children_only=False):
        if cls.group_content_window:
            dpg.delete_item(cls.group_content_window, children_only=children_only)
                
    @classmethod
    def tour_render_callback(cls, sender, app_data):
        cls.init_content_window()
        cls.tour_render(str(sender))

    @classmethod
    def tour_characteristic_render_callback(cls, sender, app_data):
        cls.init_content_window()
        cls.tour_characteristic_render(str(sender))

    @classmethod
    def tour_type_render_callback(cls, sender, app_data):
        cls.init_content_window()
        cls.tour_type_render(str(sender))

    @classmethod
    def tour_price_render_callback(cls, sender, app_data):
        cls.init_content_window()
        cls.tour_price_render(str(sender))

    @classmethod
    def location_render_callback(cls, sender, app_data):
        cls.init_content_window()
        cls.location_render(str(sender))

    @classmethod
    def tour_render(cls, data):
        cls.delete_group(children_only=True)
        dpg.add_text(default_value=data, parent=cls.group_content_window)
        dpg.add_button(label="Add new tour", callback=cls.tour_create_window, parent=cls.group_content_window)
        
        header = ['id', 'name', 'characteristic', "type", "price", "location"]
        data = []
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
            parent=cls.group_content_window
        )
        
    @classmethod
    def tour_characteristic_render(cls, data):
        cls.delete_group(children_only=True)
        dpg.add_text(default_value=data, parent=cls.group_content_window)
        
    @classmethod
    def tour_type_render(cls, data):
        cls.delete_group(children_only=True)
        dpg.add_text(default_value=data, parent=cls.group_content_window)
        
    @classmethod
    def tour_price_render(cls, data):
        cls.delete_group(children_only=True)
        dpg.add_text(default_value=data, parent=cls.group_content_window)
        
    @classmethod
    def location_render(cls, data):
        cls.delete_group(children_only=True)
        dpg.add_text(default_value=data, parent=cls.group_content_window)
        
    @classmethod
    def tour_create_window(cls):
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
        
        tour_characteristics = dpg.add_combo(label="Characteristic", items=tour_characteristics, parent=window)
        tour_types = dpg.add_combo(label="Type", items=tour_types, parent=window)
        tour_prices = dpg.add_combo(label="Price", items=tour_prices, parent=window)
        locations = dpg.add_combo(label="Location", items=locations, parent=window)
        
        group = dpg.add_group(horizontal=True, parent=window)
        button = dpg.add_button(label="Add new tour", callback=cls.tour_create_window_callback, parent=group)
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
    def tour_create_window_callback(cls, sender, app_data, user_data):
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
                dpg.configure_item(user_data['status'], default_value=f'Status: {error["message"]}', color=[255, 92, 88])
            else:
                dpg.delete_item(user_data['window'])
                
            