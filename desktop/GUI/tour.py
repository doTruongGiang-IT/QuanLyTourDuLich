import dearpygui.dearpygui as dpg
from base_window import init_window, init_font

dpg.create_context()
        
init_font()
init_window()
            
            
dpg.show_style_editor()
dpg.show_imgui_demo()
# dpg.show_debug()
dpg.show_item_registry()

dpg.configure_app(docking=True, docking_space=True)
dpg.create_viewport(title='Custom Title', width=1215, height=840)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()