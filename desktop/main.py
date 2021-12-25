import json
import threading

import dearpygui.dearpygui as dpg

from Base.lazy_loading import async_lazy_loading
from GUI.base_menu import init_onclose, menu_content, menu_menu
from GUI.base_window import init_font, init_window

dpg.create_context()
        
init_font()
init_window()
init_onclose()

lazy_loading_thread = threading.Thread(target=async_lazy_loading, args=(), daemon=True)
lazy_loading_thread.start()
            
# dpg.show_style_editor()
# dpg.show_imgui_demo()
# dpg.show_debug()
# dpg.show_item_registry()


data = open("./GUI/theme_data.json", "r")
data = ''.join(data.readlines())
data = json.loads(data)


def init_style():
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_CellPadding, 8, 2)

def set_classic_theme():
    with dpg.theme(default_theme=True) as classic_theme:
        with dpg.theme_component(dpg.mvAll):
            for attr, value in data['classic_theme'].items():
                dpg.add_theme_color(getattr(dpg, attr), value)
                
        init_style() 
        
    dpg.bind_theme(classic_theme)
    
def set_light_theme():
    with dpg.theme() as light_theme:
        with dpg.theme_component(dpg.mvAll):
            for attr, value in data['light_theme'].items():
                dpg.add_theme_color(getattr(dpg, attr), value)
        
        init_style() 
    
    dpg.bind_theme(light_theme)
    
def set_gruvbox_theme():
    with dpg.theme() as gruvbox_theme:
        with dpg.theme_component(dpg.mvAll):
            for attr, value in data['gruvbox_theme'].items():
                dpg.add_theme_color(getattr(dpg, attr), value)
                
        init_style() 
    
    dpg.bind_theme(gruvbox_theme)
    
dpg.configure_app(docking=True, docking_space=True)
dpg.create_viewport(title='Custom Title', width=1280, height=860)
with dpg.viewport_menu_bar():
    with dpg.menu(label="Window"):
        dpg.add_menu_item(tag="menu_menu_window", label="Show Menu Window", check=True, default_value=True, callback=menu_menu)
        dpg.add_menu_item(tag="menu_content_window", label="Show Content Window", check=True, default_value=True, callback=menu_content)
    with dpg.menu(label="Tools"):
        dpg.add_menu_item(label="Show About")
        dpg.add_menu_item(label="Show Document")
        dpg.add_menu_item(label="Show Metrics", callback=lambda:dpg.show_tool(dpg.mvTool_Metrics))
        dpg.add_menu_item(label="Show Style Editor", callback=lambda:dpg.show_tool(dpg.mvTool_Style))
        dpg.add_menu_item(label="Show Font Manager", callback=lambda:dpg.show_tool(dpg.mvTool_Font))
    with dpg.menu(label="Theme"):
        dpg.add_menu_item(label="Use Classic theme", callback=set_classic_theme)
        dpg.add_menu_item(label="Use Dark theme")
        dpg.add_menu_item(label="Use Light theme", callback=set_light_theme)
        dpg.add_menu_item(label="Use Gruvbox theme", callback=set_gruvbox_theme)
        dpg.add_menu_item(label="Use Green theme")  


dpg.set_viewport_title("Travel Management")
dpg.set_viewport_small_icon("./GUI/icon.ico")
dpg.setup_dearpygui()
dpg.show_viewport()
set_light_theme()
dpg.start_dearpygui()
dpg.destroy_context()
