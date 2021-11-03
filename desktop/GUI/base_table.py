import dearpygui.dearpygui as dpg


def sort_callback(sender, sort_specs):
    if sort_specs is None: return

    rows = dpg.get_item_children(sender, 1)

    sortable_list = []
    for row in rows:
        first_cell = dpg.get_item_children(row, 1)[0]
        sortable_list.append([row, dpg.get_value(first_cell)])

    def _sorter(e):
        return e[1]

    sortable_list.sort(key=_sorter, reverse=sort_specs[0][1] < 0)

    new_order = [] 
    for pair in sortable_list:
        new_order.append(pair[0])

    dpg.reorder_items(sender, 1, new_order)

def init_table(
    header, 
    data, 
    parent, 
    width_columns = None, 
    is_action = False, 
    modified_callback=None, 
    delete_callback=None, 
    view_callback=None
):
    table = dpg.add_table(
        header_row=True, 
        borders_innerH=True, 
        borders_outerH=True,
        borders_innerV=True, 
        borders_outerV=True, 
        row_background=True,
        resizable=True,
        sortable=True,
        callback=sort_callback,
        parent=parent)

    for idx, column in enumerate(header):
        width = width_columns[idx] if width_columns else 0
        dpg.add_table_column(label=column, width=width, parent=table)

    if is_action is True:
        dpg.add_table_column(label="Action", parent=table)
        
    for row in data:
        table_row = dpg.add_table_row(parent=table)
        for d in row:
            dpg.add_text(d, parent=table_row)
        
        if is_action is True:
            action_group = dpg.add_group(horizontal=True, parent=table_row)
            dpg.add_button(label='M', parent=action_group, callback=modified_callback, user_data=row[0])
            dpg.add_button(label='D', parent=action_group, callback=delete_callback, user_data=row[0])
            dpg.add_button(label='V', parent=action_group, callback=view_callback, user_data=row[0])
            dpg.add_image_button
            
    return table