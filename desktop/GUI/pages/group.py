import dearpygui.dearpygui as dpg

from .group_group import GroupGroupGUI


class GroupGUI:
    content_window = "content_window"
    group_content_window = None
    CONTENT_TAB_BAR = [
        ["group_tab_bar_menu_window", "Group", GroupGroupGUI],
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
    def group_render_callback(cls, sender, app_data):
        cls.init_content_window()
        GroupGroupGUI.group_content_window = cls.group_content_window
        GroupGroupGUI.content_render(str(sender))
