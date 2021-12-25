import dearpygui.dearpygui as dpg

from .tour_tour import TourTourGUI
from .tour_characteristic import TourCharacteristicGUI
from .tour_type import TourTypeGUI
from .tour_price import TourPriceGUI
from .tour_location import TourLocationGUI


class TourGUI:
    content_window = "content_window"
    group_content_window = None
    CONTENT_TAB_BAR = [
        ["tour_tab_bar_menu_window", "Tour", TourTourGUI],
        ["tour_characteristic_tab_bar_menu_window", "Tour Characteristic", TourCharacteristicGUI],
        ["tour_type_tab_bar_menu_window", "Tour Type", TourTypeGUI],
        ["tour_price_tab_bar_menu_window", "Tour Price", TourPriceGUI],
        ["location_tab_bar_menu_window", "Location", TourLocationGUI]
    ]
    
    @classmethod
    def tab_bar_call_back(cls, sender, data):
        for tab in cls.CONTENT_TAB_BAR:
            if dpg.get_item_label(data) == tab[1]:
                tab[2].group_content_window = cls.group_content_window
                tab[2].content_render(tab[1])
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
        TourTourGUI.group_content_window = cls.group_content_window
        TourTourGUI.content_render(str(sender))

    @classmethod
    def tour_characteristic_render_callback(cls, sender, app_data):
        cls.init_content_window()
        TourCharacteristicGUI.group_content_window = cls.group_content_window
        TourCharacteristicGUI.content_render(str(sender))

    @classmethod
    def tour_type_render_callback(cls, sender, app_data):
        cls.init_content_window()
        TourTypeGUI.group_content_window = cls.group_content_window
        TourTypeGUI.content_render(str(sender))

    @classmethod
    def tour_price_render_callback(cls, sender, app_data):
        cls.init_content_window()
        TourPriceGUI.group_content_window = cls.group_content_window
        TourPriceGUI.content_render(str(sender))

    @classmethod
    def location_render_callback(cls, sender, app_data):
        cls.init_content_window()
        TourLocationGUI.group_content_window = cls.group_content_window
        TourLocationGUI.content_render(str(sender))
