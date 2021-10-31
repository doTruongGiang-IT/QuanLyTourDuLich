import dearpygui.dearpygui as dpg

from ..base_table import init_table
from BUS.tour import TourBUS, TourCharacteristicBUS, TourTypeBUS, TourPriceBUS, LocationBUS


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
        window = dpg.add_window(label="Add new tour", width=400, autosize=True)
        dpg.add_input_text(label="Name ", parent=window)
        
        tour_characteristics    = TourCharacteristicBUS().objects
        tour_types              = TourTypeBUS().objects
        tour_prices             = TourPriceBUS().objects
        locations               = LocationBUS().objects
        
        tour_characteristics    = [f'{d.id} | {d.name}' for d in tour_characteristics]
        tour_types              = [f'{d.id} | {d.name}' for d in tour_types]
        tour_prices             = [f'{d.id} | {d.name}' for d in tour_prices]
        locations               = [f'{d.id} | {d.name}' for d in locations]
        
        dpg.add_combo(label="Characteristic", items=tour_characteristics, parent=window)
        dpg.add_combo(label="Type", items=tour_types, parent=window)
        dpg.add_combo(label="Price", items=tour_prices, parent=window)
        dpg.add_combo(label="Location", items=locations, parent=window)
        
        dpg.add_button(label="Add new tour", parent=window)