import dearpygui.dearpygui as dpg
from .statistic_cost_tour import StatsCostTourGUI
from .statistic_tour_performance import StatsTourPerfGUI
from .statistic_cost_group import StatsCostGroupGUI
from .statistics_tours_of_staff import StatsToursOfStaffGUI

class StatisticGUI:
    content_window = "content_window"
    group_content_window = None
    CONTENT_TAB_BAR = [
        ["stats_cost_tour_tab_bar_menu_window", "Stats cost tour", StatsCostTourGUI],
        ["stats_cost_group_tab_bar_menu_window", "Stats cost group", StatsCostGroupGUI],
        ["stats_tour_perf_tab_bar_menu_window", "Stats tour's performance", StatsTourPerfGUI],
        ["customer_tab_bar_menu_window", "Tours Of Staff", StatsToursOfStaffGUI],
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
    def stats_cost_tour_render_callback(cls, sender, app_data):
        cls.init_content_window()
        StatsCostTourGUI.group_content_window = cls.group_content_window
        StatsCostTourGUI.content_render(str(sender))
    
    @classmethod
    def stats_tour_perf_render_callback(cls, sender, app_data):
        cls.init_content_window()
        StatsTourPerfGUI.group_content_window = cls.group_content_window
        StatsTourPerfGUI.content_render(str(sender))

    @classmethod
    def stats_cost_group_render_callback(cls, sender, app_data):
        cls.init_content_window()
        StatsCostGroupGUI.group_content_window = cls.group_content_window
        StatsCostGroupGUI.content_render(str(sender))