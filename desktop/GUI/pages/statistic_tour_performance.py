import dearpygui.dearpygui as dpg

from datetime import date, datetime
from ..base_table import init_table
from BUS.statistics import StatsCostRevenueTourBUS
from BUS.tour import TourPriceBUS
from BUS.group import GroupBUS

class StatsTourPerfGUI:
    group_content_window = None
    table = None
    btn_start_date = None
    btn_end_date = None
    txt_num_group = None
    txt_revenue_general = None

    start_date = None
    end_date = None

    @classmethod
    def content_render(cls, data):
        dpg.delete_item(cls.group_content_window, children_only=True)
        dpg.add_text(default_value=data, parent=cls.group_content_window)
        cls.table = None
        cls.btn_start_date = None
        cls.btn_end_date = None
        cls.txt_num_group = None
        cls.txt_revenue_general = None

        cls.start_date = "...-...-..."
        cls.end_date = "...-...-..."
        
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

        header = ['id', 'name', 'revenue', 'number of groups']
        type_columns = [int, str, float, int]
        stats_cost_rev_tour_bus = StatsCostRevenueTourBUS()
        stats_cost_rev_tour_data = stats_cost_rev_tour_bus.objects
        group_bus = GroupBUS()

        if cls.table is not None:
            dpg.delete_item(cls.table)
            cls.table = None
        
        general_num_group = 0
        general_revenue = 0

        data = []
        for d in stats_cost_rev_tour_data:
            general_revenue += d.revenue
            group = [g for g in group_bus.objects if g.tour == d.id]
            number = len(group)
            general_num_group += number
            data.append([
                d.id,
                d.name,
                d.revenue,
                number
            ])

        cls.table= init_table(
            header=header,
            data=data,
            parent=cls.group_content_window,
            type_columns=type_columns,
            is_action=None,
            modified_callback=None,
            delete_callback=None,
            view_callback=None
        )
        cls.txt_num_group = dpg.add_input_text(label='General group', default_value=general_num_group, parent=cls.group_content_window, enabled=False)
        cls.txt_revenue_general = dpg.add_input_text(label='General revenue', default_value=general_revenue, parent=cls.group_content_window, enabled=False)

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

        header = ['id', 'name', 'revenue', 'number of groups']
        type_columns = [int, str, float, int]
        stats_cost_rev_tour_bus = StatsCostRevenueTourBUS()
        stats_cost_rev_tour_data = stats_cost_rev_tour_bus.objects
        group_bus = GroupBUS()


        general_num_group = 0
        general_revenue = 0

        data = []
        for d in stats_cost_rev_tour_data:
            general_revenue += d.revenue
            group = [g for g in group_bus.objects if g.tour == d.id]
            number = len(group)
            general_num_group += number
            data.append([
                d.id,
                d.name,
                d.revenue,
                number
            ])

        if cls.table is not None:
            dpg.delete_item(cls.table)
            cls.table = None
        if cls.txt_revenue_general is not None:
            dpg.delete_item(cls.txt_revenue_general)
            cls.txt_revenue_general = None
        if cls.txt_num_group is not None:
            dpg.delete_item(cls.txt_num_group)
            cls.txt_num_group = None

        cls.table= init_table(
            header=header,
            data=data,
            parent=cls.group_content_window,
            type_columns=type_columns,
            is_action=False,
            modified_callback=None,
            delete_callback=None,
            view_callback=None
        )
        cls.txt_num_group = dpg.add_input_text(label='General group', default_value=general_num_group, parent=cls.group_content_window, enabled=False)
        cls.txt_revenue_general = dpg.add_input_text(label='General revenue', default_value=general_revenue, parent=cls.group_content_window, enabled=False)

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
        general_num_group = 0
        general_revenue = 0
        tour_price_bus = TourPriceBUS()
        group_bus = GroupBUS()
        if (cls.start_date != "...-...-..." and cls.end_date == "...-...-..."):
            tour_price = [tp for tp in tour_price_bus.objects if tp.end_date >= cls.start_date]
            stats_cost_revenue_tour_bus = StatsCostRevenueTourBUS()
            for tp in tour_price:
                stats_cost_revenue_tour = [scvt for scvt in stats_cost_revenue_tour_bus.objects if scvt.price.id == tp.id]
                for d in stats_cost_revenue_tour:
                    general_revenue += d.revenue
                    group = [g for g in group_bus.objects if g.tour == d.id]
                    number = len(group)
                    general_num_group += number
                    data.append([
                        d.id,
                        d.name,
                        d.revenue,
                        number
                    ])
        if (cls.start_date == "...-...-..." and cls.end_date != "...-...-..."):
            tour_price = [tp for tp in tour_price_bus.objects if tp.end_date <= cls.end_date]
            stats_cost_revenue_tour_bus = StatsCostRevenueTourBUS()
            for tp in tour_price:
                stats_cost_revenue_tour = [scvt for scvt in stats_cost_revenue_tour_bus.objects if scvt.price.id == tp.id]
                for d in stats_cost_revenue_tour:
                    general_revenue += d.revenue
                    group = [g for g in group_bus.objects if g.tour == d.id]
                    number = len(group)
                    general_num_group += number
                    data.append([
                        d.id,
                        d.name,
                        d.revenue,
                        number
                    ])
        if (cls.start_date != "...-...-..." and cls.end_date != "...-...-..."):
            tour_price = [tp for tp in tour_price_bus.objects if tp.end_date >= cls.start_date and tp.end_date <= cls.end_date]
            stats_cost_revenue_tour_bus = StatsCostRevenueTourBUS()
            for tp in tour_price:
                stats_cost_revenue_tour = [scvt for scvt in stats_cost_revenue_tour_bus.objects if scvt.price.id == tp.id]
                for d in stats_cost_revenue_tour:
                    general_revenue += d.revenue
                    group = [g for g in group_bus.objects if g.tour == d.id]
                    number = len(group)
                    general_num_group += number
                    data.append([
                        d.id,
                        d.name,
                        d.revenue,
                        number
                    ])

        header = ['id', 'name', 'revenue', 'number of groups']
        type_columns = [int, str, float, int]

        if cls.table is not None:
            dpg.delete_item(cls.table)
            cls.table = None
        if cls.txt_num_group is not None:
            dpg.delete_item(cls.txt_num_group)
            cls.txt_num_group = None
        if cls.txt_revenue_general is not None:
            dpg.delete_item(cls.txt_revenue_general)
            cls.txt_revenue_general = None

        cls.table= init_table(
            header=header,
            data=data,
            parent=cls.group_content_window,
            type_columns=type_columns,
            is_action=None,
            modified_callback=None,
            delete_callback=None,
            view_callback=None
        )
        cls.txt_num_group = dpg.add_input_text(label='General group', default_value=general_num_group, parent=cls.group_content_window, enabled=False)
        cls.txt_revenue_general = dpg.add_input_text(label='General revenue', default_value=general_revenue, parent=cls.group_content_window, enabled=False)

        dpg.delete_item(user_data['window'])