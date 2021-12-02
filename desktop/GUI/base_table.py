from typing import List
import dearpygui.dearpygui as dpg

from DTO.group import GroupJourney


def sort_callback(sender, sort_specs, user_data):
    if sort_specs is None: return
    
    type_columns = user_data
    rows = dpg.get_item_children(sender, 1)
    ind = type_columns[sort_specs[0][0]][0]
    data_type = type_columns[sort_specs[0][0]][1]

    sortable_list = []
    for row in rows:
        ind_cell = dpg.get_item_children(row, 1)[ind]
        sortable_list.append([row, dpg.get_value(ind_cell)])

    def _sorter(e):
        return data_type(e[1])
    
    sortable_list.sort(key=_sorter, reverse=sort_specs[0][1] < 0)

    new_order = [] 
    for pair in sortable_list:
        new_order.append(pair[0])

    dpg.reorder_items(sender, 1, new_order)

def init_table(
    header, 
    data, 
    parent, 
    type_columns=None,
    is_action=False, 
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
        hideable=True,
        precise_widths=True,
        no_host_extendX=True,
        callback=sort_callback,
        parent=parent)

    type_column_map = {}
    
    for ind, column in enumerate(header):
        col = dpg.add_table_column(label=column, width_fixed=True, parent=table)
        if type_columns:
            type_column_map[col] = (ind, type_columns[ind])

    if is_action is True:
        dpg.add_table_column(label="Action", parent=table, no_sort=True)
        
    for row in data:
        table_row = dpg.add_table_row(parent=table)
        for d in row:
            if type(d) == list:
                data = []
                for j in d:
                    content = str(j.start_date.hour) + "h" + str(j.start_date.minute) + "-" + str(j.end_date.hour) + "h" + str(j.start_date.minute) + " : " + j.content
                    data.append(content)
                dpg.add_combo(items=data, parent=table_row, no_preview=True)
            else:
                dpg.add_text(d, parent=table_row)
        
        if is_action is True:
            action_group = dpg.add_group(horizontal=True, parent=table_row)
            modified_button= dpg.add_button(label='M', parent=action_group, callback=modified_callback, user_data=row[0])
            delete_button = dpg.add_button(label='D', parent=action_group, callback=delete_callback, user_data=row[0])
            view_button = dpg.add_button(label='V', parent=action_group, callback=view_callback, user_data=row[0])
            tooltip_modified_button = dpg.add_tooltip(parent=modified_button)
            tooltip_delete_button = dpg.add_tooltip(parent=delete_button)
            tooltip_view_button = dpg.add_tooltip(parent=view_button)
            dpg.add_text("Modified", parent=tooltip_modified_button)
            dpg.add_text("Delete", parent=tooltip_delete_button)
            dpg.add_text("View", parent=tooltip_view_button)
            dpg.add_selectable(parent=action_group, span_columns=True)
            
    dpg.configure_item(table, user_data=type_column_map)    
    
    return table
