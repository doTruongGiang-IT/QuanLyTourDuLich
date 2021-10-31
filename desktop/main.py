import dearpygui.dearpygui as dpg
from GUI.base_window import init_window, init_font

dpg.create_context()
        
init_font()
init_window()
            
            
dpg.show_style_editor()
dpg.show_imgui_demo()
# dpg.show_debug()
dpg.show_implot_demo()

dpg.configure_app(docking=True, docking_space=True)
dpg.create_viewport(title='Custom Title', width=1215, height=840)
# with dpg.viewport_menu_bar():
#     with dpg.menu(label="Tools"):
#         dpg.add_menu_item(label="Show About")
#         dpg.add_menu_item(label="Show Metrics")
#         dpg.add_menu_item(label="Show Documentation")
#         dpg.add_menu_item(label="Show Debug")
#         dpg.add_menu_item(label="Show Style Editor")
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()