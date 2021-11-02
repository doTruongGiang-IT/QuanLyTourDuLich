import dearpygui.dearpygui as dpg
from .base_data import MENU

def init_window():
    with dpg.window(tag="menu_window", label="Menu", pos=[0, 0], width=400, height=800):
        for collapsing_header, header_data in MENU.items():
            with dpg.collapsing_header(tag=collapsing_header, label=header_data['name']):
                for item_data in header_data['data']:
                    dpg.add_button(tag=item_data[0], label=item_data[1], width=380, indent=20, callback=item_data[2])
        
    with dpg.window(tag="content_window", label="Content", pos=[400, 0], width=865, height=800):
        pass
    
def init_font():
    with dpg.font_registry() as main_font_registry:
        roboto_mono_regular_font = dpg.add_font('GUI/font/roboto_mono/RobotoMono-Medium.ttf', 16)
        lora_regular_font = dpg.add_font('GUI/font/lora/Lora-Medium.ttf', 16)
        firacode_regular_font = dpg.add_font('GUI/font/firacode/FiraCode-SemiBold.ttf', 15)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Vietnamese, parent=roboto_mono_regular_font)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Vietnamese, parent=lora_regular_font)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Vietnamese, parent=firacode_regular_font)
        dpg.bind_font(roboto_mono_regular_font)