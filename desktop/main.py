import threading

import dearpygui.dearpygui as dpg

from Base.lazy_loading import async_lazy_loading
from GUI.base_window import init_font, init_window

dpg.create_context()
        
init_font()
init_window()

lazy_loading_thread = threading.Thread(target=async_lazy_loading, args=(), daemon=True)
lazy_loading_thread.start()
            
dpg.show_style_editor()
dpg.show_imgui_demo()
# dpg.show_debug()
# dpg.show_item_registry()

dpg.configure_app(docking=True, docking_space=True)
dpg.create_viewport(title='Custom Title', width=1280, height=840)
# with dpg.viewport_menu_bar():
#     with dpg.menu(label="Window"):
#         dpg.add_menu_item(label="Show About")
#         dpg.add_menu_item(label="Show Metrics")
#         dpg.add_menu_item(label="Show Documentation")
#         dpg.add_menu_item(label="Show Debug")
#         dpg.add_menu_item(label="Show Style Editor")
#     with dpg.menu(label="Tools"):
#         dpg.add_menu_item(label="Show About")
#         dpg.add_menu_item(label="Show Metrics")
#         dpg.add_menu_item(label="Show Documentation")
#         dpg.add_menu_item(label="Show Debug")
#         dpg.add_menu_item(label="Show Style Editor")
#     with dpg.menu(label="Theme"):
#         dpg.add_menu_item(label="Show About")
#         dpg.add_menu_item(label="Show Metrics")
#         dpg.add_menu_item(label="Show Documentation")
#         dpg.add_menu_item(label="Show Debug")
#         dpg.add_menu_item(label="Show Style Editor")  

with dpg.theme() as global_theme:

    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_CellPadding, 8, 2)

dpg.bind_theme(global_theme)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
