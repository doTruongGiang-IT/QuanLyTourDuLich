import dearpygui.dearpygui as dpg

from datetime import date, datetime

from ..base_table import init_table
from BUS.statistics import StatsCostRevenueGroupBUS
from DAO.group import GroupDAO
from BUS.tour import TourBUS
from BUS.group import GroupCostBUS

class StatsCostGroupGUI:
    group_content_window = None
    table = None
    btn_start_date = None
    btn_end_date = None
    txt_cost_general = None

    start_date = None
    end_date = None
    tour_id = None

    @classmethod
    def content_render(cls, data):
        dpg.delete_item(cls.group_content_window, children_only=True)
        cls.table = None
        cls.btn_start_date = None
        cls.btn_end_date = None
        cls.txt_cost_general = None
        # cls.txt_revenue_general = None

        cls.start_date = "...-...-..."
        cls.end_date = "...-...-..."
        cls.tour_id = None

        tours = [f'{t.id} | {t.name}' for t in TourBUS().objects]

        high_top_group = dpg.add_group(horizontal=True, parent=cls.group_content_window)
        dpg.add_text(default_value=data, parent=high_top_group)
        tour_combo = dpg.add_combo(label="Tour", items=tours, parent=high_top_group, callback=cls.choice_tour_combo)
        
        top_group = dpg.add_group(horizontal=True, parent=cls.group_content_window)
        dpg.add_text("Start date:", parent=top_group)
        if cls.start_date is None:
            cls.btn_start_date = dpg.add_button(label="...-...-...", parent=top_group, callback=cls.window_date_picker)
        else:
            cls.btn_start_date = dpg.add_button(label=cls.start_date, parent=top_group, callback=cls.window_date_picker)
        dpg.add_text("End date:", parent=top_group)
        if cls.end_date is None:
            cls.btn_end_date = dpg.add_button(label="...-...-...", parent=top_group, callback=cls.window_date_picker)
        else:
            cls.btn_end_date = dpg.add_button(label=cls.end_date, parent=top_group, callback=cls.window_date_picker)
        dpg.set_item_user_data(cls.btn_start_date, "start_date")
        dpg.set_item_user_data(cls.btn_end_date, "end_date")
        dpg.add_button(label="Clear", parent=top_group, callback=cls.clear_callback)
    
    @classmethod
    def choice_tour_combo(cls, sender, app_data):
        cls.tour_id = int(app_data.split('|')[0])
        header = ['id', 'name', "cost"]
        type_columns = [int, str, float]
        data = []
        stats_cost_rev_group_bus = StatsCostRevenueGroupBUS()
        stats_cost_rev_group_data = stats_cost_rev_group_bus.read(cls.tour_id)
        general_cost = 0

        for d in stats_cost_rev_group_data:
            general_cost += d.cost
            data.append([
                d.id,
                d.name,
                d.cost
            ])
        
        if cls.table is not None:
            dpg.delete_item(cls.table)
            cls.table = None
        if cls.txt_cost_general is not None:
            dpg.delete_item(cls.txt_cost_general)
            cls.txt_cost_general = None
        
        cls.table = cls.init_table(
            header=header,
            data=data,
            parent=cls.group_content_window,
            type_columns=type_columns,
            is_action=False,
            modified_callback=None,
            delete_callback=None,
            view_callback=None
        )
        cls.txt_cost_general = dpg.add_input_text(label='General cost', default_value=general_cost, parent=cls.group_content_window, enabled=False)

    @classmethod
    def window_date_picker(cls, sender, app_data, user_date):
        window = dpg.add_window(label="Date picker", width=400, autosize=True, pos=[500, 200])
        date_picker = dpg.add_date_picker(parent=window)
        group = dpg.add_group(horizontal=True, parent=window)
        btn_ok = dpg.add_button(label="Ok", parent=group, callback=cls.date_picker_callback)
        dpg.set_item_user_data(btn_ok, {
            'window': window,
            'type_date': user_date,
            'date': date_picker
        })
        dpg.add_button(label="Close", parent=group, callback=lambda :dpg.delete_item(window))
    
    @classmethod
    def clear_callback(cls, sender, app_data, user_data):
        cls.start_date = "...-...-..."
        cls.end_date = "...-...-..."

        dpg.set_item_label(cls.btn_start_date, "...-...-...")
        dpg.set_item_label(cls.btn_end_date, "...-...-...")

        header = ['id', 'name', 'cost']
        type_columns = [int, str, float]

        general_cost = 0

        data = []

        if cls.tour_id is not None:
            stats_cost_rev_group_bus = StatsCostRevenueGroupBUS()
            stats_cost_rev_group_data = stats_cost_rev_group_bus.read(cls.tour_id)
            for d in stats_cost_rev_group_data:
                general_cost += d.cost
                data.append([
                    d.id,
                    d.name,
                    d.cost
            ])

        if cls.table is not None:
            dpg.delete_item(cls.table)
            cls.table = None
        if cls.txt_cost_general is not None:
            dpg.delete_item(cls.txt_cost_general)
            cls.txt_cost_general = None

        cls.table= cls.init_table(
            header=header,
            data=data,
            parent=cls.group_content_window,
            type_columns=type_columns,
            is_action=False,
            modified_callback=None,
            delete_callback=None,
            view_callback=None
        )
        cls.txt_cost_general = dpg.add_input_text(label='General cost', default_value=general_cost, parent=cls.group_content_window, enabled=False)
    
    @classmethod
    def date_picker_callback(cls, sender, app_data, user_data):
        date = dpg.get_value(user_data['date'])
        date = datetime(date['year']+1900, date['month']+1, date['month_day'])
        date_string = date.strftime("%Y-%m-%d")
        if(user_data['type_date'] == 'start_date'):
            dpg.set_item_label(cls.btn_start_date, date_string)
            cls.start_date = date
        else:
             dpg.set_item_label(cls.btn_end_date, date_string)
             cls.end_date = date

        data = []
        general_cost = 0

        group_dao = GroupDAO()

        if cls.tour_id is not None:
            if (cls.start_date != "...-...-..." and cls.end_date == "...-...-..."):
                stats_cost_rev_group_bus = StatsCostRevenueGroupBUS()
                stats_cost_rev_group_data = stats_cost_rev_group_bus.read(cls.tour_id)
                for scrg in stats_cost_rev_group_data:
                    _, group = group_dao.read_detail(scrg.id)
                    print (f"{group} | abc")
                    if(group.journey[-1].end_date >= cls.start_date):
                        general_cost += scrg.cost
                        data.append([
                            scrg.id,
                            scrg.name,
                            scrg.cost
                        ])
            if (cls.start_date == "...-...-..." and cls.end_date != "...-...-..."):
                stats_cost_rev_group_bus = StatsCostRevenueGroupBUS()
                stats_cost_rev_group_data = stats_cost_rev_group_bus.read(cls.tour_id)
                for scrg in stats_cost_rev_group_data:
                    _, group = group_dao.read_detail(scrg.id)
                    print (f"{group} | abc")
                    if(group.journey[-1].end_date <= cls.end_date):
                        general_cost += scrg.cost
                        data.append([
                            scrg.id,
                            scrg.name,
                            scrg.cost
                        ])
            if (cls.start_date != "...-...-..." and cls.end_date != "...-...-..."):
                stats_cost_rev_group_bus = StatsCostRevenueGroupBUS()
                stats_cost_rev_group_data = stats_cost_rev_group_bus.read(cls.tour_id)
                for scrg in stats_cost_rev_group_data:
                    _, group = group_dao.read_detail(scrg.id)
                    print (f"{group} | abc")
                    if(group.journey[-1].end_date >= cls.start_date and group.journey[-1].end_date <= cls.end_date):
                        general_cost += scrg.cost
                        data.append([
                            scrg.id,
                            scrg.name,
                            scrg.cost
                        ])

        header = ['id', 'name', 'cost']
        type_columns = [int, str, float]

        if cls.table is not None:
            dpg.delete_item(cls.table)
            cls.table = None
        if cls.txt_cost_general is not None:
            dpg.delete_item(cls.txt_cost_general)
            cls.txt_cost_general = None

        cls.table = cls.init_table(
            header=header,
            data=data,
            parent=cls.group_content_window,
            type_columns=type_columns,
            is_action=False,
            modified_callback=None,
            delete_callback=None,
            view_callback=None
        )
        cls.txt_cost_general = dpg.add_input_text(label='General cost', default_value=general_cost, parent=cls.group_content_window, enabled=False)

        dpg.delete_item(user_data['window'])

    @classmethod
    def sort_callback(cls, sender, sort_specs, user_data):
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
    
    @classmethod
    def init_table(
        cls,
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
            callback=None,
            parent=parent)

        type_column_map = {}
        
        for ind, column in enumerate(header):
            col = dpg.add_table_column(label=column, width_fixed=False, parent=table)
            if type_columns:
                type_column_map[col] = (ind, type_columns[ind])
        dpg.add_table_column(width_fixed=False, parent=table)

        if is_action is True:
            dpg.add_table_column(label="Action", parent=table, no_sort=True)
            
        for row in data:
            table_row = dpg.add_table_row(parent=table)
            with dpg.theme() as item_theme:
                with dpg.theme_component(dpg.mvAll):
                    dpg.add_theme_color(dpg.mvThemeCol_Text, [102, 255, 51])
            dpg.bind_item_theme(table_row, item_theme)     
            for d in row:
                txt_row = dpg.add_text(d, parent=table_row)
                dpg.bind_item_theme(txt_row, item_theme) 
            group_cost_bus = GroupCostBUS()
            group_costs = [g for g in group_cost_bus.objects if g.group.id == row[0]]
            header_cost_row = dpg.add_table_row(parent=table)
            dpg.add_text("Group cost", parent=header_cost_row)
            dpg.add_text("id", parent=header_cost_row)
            dpg.add_text("name", parent=header_cost_row)
            dpg.add_text("price", parent=header_cost_row)
            for gc in group_costs:
                table_row_cost = dpg.add_table_row(parent=table)
                dpg.add_text("", parent=table_row_cost)
                dpg.add_text(gc.id, parent=table_row_cost)
                dpg.add_text(gc.name, parent=table_row_cost)
                dpg.add_text(gc.price, parent=table_row_cost)
                
        dpg.configure_item(table, user_data=type_column_map)    
        
        return table