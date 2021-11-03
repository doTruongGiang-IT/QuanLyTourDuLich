import dearpygui.dearpygui as dpg

from .base_window import init_content_window, init_menu_window

MENU_STATUS = {
    'menu': True,
    'content': True
}
 
def onclose_menu_window():
    MENU_STATUS['menu'] = False
    dpg.configure_item("menu_menu_window", default_value = False)
    
def onclose_content_window():
    MENU_STATUS['content'] = False
    dpg.configure_item("menu_content_window", default_value = False)

def init_onclose():
    dpg.configure_item("menu_window", on_close=onclose_menu_window)
    dpg.configure_item("content_window", on_close=onclose_content_window)

def menu_menu(sender, app_data):
    if MENU_STATUS['menu'] is False:
        if dpg.does_alias_exist("menu_window"):
            dpg.remove_alias("menu_window")
        init_menu_window()
        dpg.configure_item("menu_window", on_close=onclose_menu_window)
    else:
        dpg.delete_item("menu_window")
    
    MENU_STATUS['menu'] = not MENU_STATUS['menu']

def menu_content(sender, app_data):
    if MENU_STATUS['content'] is False:
        if dpg.does_alias_exist("content_window"):
            dpg.remove_alias("content_window")
        init_content_window()
        dpg.configure_item("content_window", on_close=onclose_content_window)
    else:
        dpg.delete_item("content_window")
    
    MENU_STATUS['content'] = not MENU_STATUS['content']
