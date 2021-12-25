import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()

def sort_callback(sender, sort_specs):

    # sort_specs scenarios:
    #   1. no sorting -> sort_specs == None
    #   2. single sorting -> sort_specs == [[column_id, direction]]
    #   3. multi sorting -> sort_specs == [[column_id, direction], [column_id, direction], ...]
    #
    # notes:
    #   1. direction is ascending if == 1
    #   2. direction is ascending if == -1

    # no sorting case
    if sort_specs is None: return

    rows = dpg.get_item_children(sender, 1)

    # create a list that can be sorted based on first cell
    # value, keeping track of row and value used to sort
    sortable_list = []
    for row in rows:
        first_cell = dpg.get_item_children(row, 1)[0]
        sortable_list.append([row, dpg.get_value(first_cell)])

    def _sorter(e):
        return e[1]

    sortable_list.sort(key=_sorter, reverse=sort_specs[0][1] < 0)

    # create list of just sorted row ids
    new_order = []
    for pair in sortable_list:
        new_order.append(pair[0])

    dpg.reorder_items(sender, 1, new_order)

with dpg.window(label="Tutorial", width=500):

    with dpg.table(header_row=True, borders_innerH=True, borders_outerH=True,
                   borders_innerV=True, borders_outerV=True, row_background=True,
                   sortable=True, callback=sort_callback):

        dpg.add_table_column(label="One")
        dpg.add_table_column(label="Two", no_sort=True)

        for i in range(25):
            with dpg.table_row():
                dpg.add_input_int(label=" ", step=0, default_value=i)
                dpg.add_text(f"Cell {i}, 1")

# main loop
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()