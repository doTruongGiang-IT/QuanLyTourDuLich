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

def init_table(header, data, parent):
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

    for column in header:
        dpg.add_table_column(label=column, parent=table)

    for row in data:
        table_row = dpg.add_table_row(parent=table)
        for d in row:
            dpg.add_text(d, parent=table_row)
            
    return table