import dearpygui.dearpygui as dpg
from .base_data import MENU

def init_window():
    with dpg.window(tag="menu_window", label="Menu", pos=[0, 0], width=400, height=800):
        for collapsing_header, header_data in MENU.items():
            with dpg.collapsing_header(tag=collapsing_header, label=header_data['name']):
                for item_data in header_data['data']:
                    dpg.add_button(tag=item_data[0], label=item_data[1], width=380, indent=20, callback=item_data[2])
        
    with dpg.window(tag="content_window", label="Content", pos=[400, 0], width=800, height=800):
        pass
    
def init_font():
    with dpg.font_registry() as main_font_registry:
        regular_font = dpg.add_font('GUI/font/static/RobotoMono-Medium.ttf', 16)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Vietnamese, parent=regular_font)
        dpg.bind_font(regular_font)