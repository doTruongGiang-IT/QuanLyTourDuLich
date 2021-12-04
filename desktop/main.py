import threading

import dearpygui.dearpygui as dpg

from Base.lazy_loading import async_lazy_loading
from GUI.base_window import init_font, init_window
from GUI.base_menu import init_onclose, menu_menu, menu_content

dpg.create_context()
        
init_font()
init_window()
init_onclose()

lazy_loading_thread = threading.Thread(target=async_lazy_loading, args=(), daemon=True)
lazy_loading_thread.start()
            
dpg.show_style_editor()
dpg.show_imgui_demo()
# dpg.show_debug()
# dpg.show_item_registry()

dpg.configure_app(docking=True, docking_space=True)
dpg.create_viewport(title='Custom Title', width=1280, height=840)
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
        dpg.add_menu_item(label="Use Classic theme")
        dpg.add_menu_item(label="Use Dark theme")
        dpg.add_menu_item(label="Use Light theme")
        dpg.add_menu_item(label="Use Gruvbox theme")
        dpg.add_menu_item(label="Use Green theme")  

with dpg.theme() as global_theme:

    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_CellPadding, 8, 2)

dpg.bind_theme(global_theme)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
