import dearpygui.dearpygui as dpg
from BUS.statistics import StatsToursOfStaffBUS
from BUS.group import GroupBUS
from BUS.staff import GroupStaffBUS
import re
import datetime

class StatsToursOfStaffGUI:
    group_content_window = None
    table = None

    @classmethod
    def content_render(cls, data, choice_default=None):
        # dpg.delete_item(cls.group_content_window, children_only=True)
        # dpg.add_text(default_value=data, parent=cls.group_content_window)
        
        top_group = dpg.add_group(horizontal=True, parent=cls.group_content_window)
        # dpg.add_button(label="Add new tour", callback=cls.create_window, parent=top_group)
        dpg.add_input_text(label="Search", parent=top_group)
        dpg.add_combo(label="Columns", items=['column1', 'column2', 'column3'], parent=top_group)
        

        header = ['id', 'name', 'number_of_tours']
        type_columns = [int, str, str]
        data = []
        tours_of_staff_bus = StatsToursOfStaffBUS()
        tour_of_staff_data = tours_of_staff_bus.objects
        
        for d in tour_of_staff_data:
            data.append([
                d.id,
                d.name,
                d.number_of_tours
            ])
        
        table = cls.init_table(
            header=header,
            data=data,
            parent=cls.group_content_window,
            type_columns=type_columns,
            is_action=True,
            modified_callback=None,
            delete_callback=None,
            view_callback=cls.view_window
        )


    # @classmethod
    # def choice_group_combo(cls, sender, app_data):
    #     header = ['id', 'name', 'id number', "address", "gender", "phone number"]
    #     type_columns = [int, str, str, str, str, str]

    #     if app_data == 'All':
    #         data = []
    #         customer_bus = CustomerBUS()
    #         customer_data = customer_bus.objects
    #         for c in customer_data:
    #             data.append([
    #                 c.id,
    #                 c.name,
    #                 c.id_number,
    #                 c.address,
    #                 c.gender,
    #                 c.phone_number
    #             ])

    #         if cls.table is not None:
    #             dpg.delete_item(cls.table)
    #             cls.table = None

    #         cls.table = init_table(
    #             header=header,
    #             data=data,
    #             parent=cls.group_content_window,
    #             type_columns=type_columns,
    #             is_action=True,
    #             modified_callback=cls.modified_window,
    #             delete_callback=cls.delete_window,
    #             view_callback=cls.view_window
    #         )
    #     else:
    #         group_id = int(app_data.split('|')[0])
    #         print (group_id)

    #         data = []
    #         group_customer_bus = GroupCustomerBUS()
    #         # print (group_customer_bus.objects(group_id))
    #         group_customer_data = group_customer_bus.read(group_id)
    #         for gc in group_customer_data:
    #             customer_bus = CustomerBUS()
    #             customer = [c for c in customer_bus.objects if c.id == gc.customer][0]
    #             data.append([
    #                 customer.id,
    #                 customer.name,
    #                 customer.id_number,
    #                 customer.address,
    #                 customer.gender,
    #                 customer.phone_number
    #             ])
            
    #         if cls.table is not None:
    #                 dpg.delete_item(cls.table)
    #                 cls.table = None

    #         cls.table = init_table(
    #                 header=header,
    #                 data=data,
    #                 parent=cls.group_content_window,
    #                 type_columns=type_columns,
    #                 is_action=True,
    #                 modified_callback=cls.modified_window,
    #                 delete_callback=cls.delete_window,
    #                 view_callback=cls.view_window
    #         )

    # @classmethod
    # def create_window(cls):
    #     window = dpg.add_window(label="Add new customer", width=400, autosize=True, pos=[500, 200])

    #     customer_name = dpg.add_input_text(label="Name ", parent=window)
    #     customer_id_number = dpg.add_input_text(label="ID number ", parent=window)
    #     customer_address = dpg.add_input_text(label="Address ", parent=window)
    #     datas = ["Male", "Female", "Other"]
    #     customer_gender = dpg.add_combo(label="Gender ", items=datas, parent=window)
    #     customer_phone_number = dpg.add_input_text(label="Phone number ", parent=window)
        
    #     group = dpg.add_group(horizontal=True, parent=window)
    #     button = dpg.add_button(label="Add new tour", callback=cls.create_window_callback, parent=group)
    #     status = dpg.add_text(default_value="Status", parent=group)
    #     dpg.set_item_user_data(
    #         button, 
    #         {
    #             'window': window,
    #             'status': status, 
    #             'items': [
    #                 {
    #                     'field': 'name',
    #                     'name': 'Customer name',
    #                     'item': customer_name,
    #                 },
    #                 {
    #                     'field': 'id_number',
    #                     'name': 'ID number',
    #                     'item': customer_id_number,
    #                 },
    #                 {
    #                     'field': 'address',
    #                     'name': 'Address',
    #                     'item': customer_address,
    #                 },
    #                 {
    #                     'field': 'gender',
    #                     'name': 'Gender',
    #                     'item': customer_gender,
    #                 },
    #                 {
    #                     'field': 'phone_number',
    #                     'name': 'Phone number',
    #                     'item': customer_phone_number,
    #                 }
    #             ]
    #         }
    #     )

    # @classmethod
    # def create_window_callback(cls, sender, app_data, user_data):
    #     is_valid = True
    #     request_data = {}
        
    #     for item in user_data['items']:
    #         data = dpg.get_value(item['item'])
    #         if data != "": 
    #             request_data[item['field']] = data
    #             if item['field'] == 'id_number':
    #                 pattern_id_number = re.compile('^([0-9]{9}|[0-9]{12})+$')
    #                 if pattern_id_number.match(data) is None:
    #                     is_valid = False
    #                     dpg.configure_item(user_data['status'], default_value=f'Status: {item["name"]} is not id number', color=[255, 92, 88])

    #             if item['field'] == 'phone_number':
    #                 pattern_id_number = re.compile('^([0-9]{10}|[0-9]{11})+$')
    #                 if pattern_id_number.match(data) is None:
    #                     is_valid = False
    #                     dpg.configure_item(user_data['status'], default_value=f'Status: {item["name"]} is not phone number', color=[255, 92, 88])
    #         else:
    #             is_valid = False
    #             dpg.configure_item(user_data['status'], default_value=f'Status: {item["name"]} is invalid', color=[255, 92, 88])               
    #             break
            
    #     if is_valid:
    #         dpg.configure_item(user_data['status'], default_value=f'Status: OK', color=[128, 237, 153]) 
    #         print(request_data)
            
    #         customer_obj = Customer(
    #             id=0,
    #             name=request_data['name'],
    #             id_number=request_data['id_number'],
    #             address=request_data['address'],
    #             gender=request_data['gender'],
    #             phone_number=request_data['phone_number']
    #         ) 
    #         customer_bus = CustomerBUS()
    #         error = customer_bus.create(customer_obj)
            
    #         if error.status is True:
    #             dpg.configure_item(user_data['status'], default_value=f'Status: {error.message}', color=[255, 92, 88])
    #         else:
    #             dpg.delete_item(user_data['window'])
    #             cls.content_render("customer")

    # @classmethod
    # def modified_window(cls, sender, app_data, user_data):
    #     customers = CustomerBUS().objects
        
    #     customer = [c for c in customers if c.id == user_data][0]
        
    #     window = dpg.add_window(label="Modified the customer", width=400, autosize=True, pos=[500, 200])
    #     customer_id = dpg.add_text(default_value=f"id: {customer.id}", parent=window)
    #     customer_name = dpg.add_input_text(label="Name ", default_value=customer.name, parent=window)
    #     customer_id_number = dpg.add_input_text(label="ID number ", default_value=customer.id_number, parent=window)
    #     customer_address = dpg.add_input_text(label="Address ", default_value=customer.address, parent=window)
    #     datas = ["Male", "Female", "Other"]
    #     customer_gender = dpg.add_combo(label="Gender ", items=datas, default_value=customer.gender, parent=window)
    #     customer_phone_number = dpg.add_input_text(label="Phone number ", default_value=customer.phone_number, parent=window)
        
    #     group = dpg.add_group(horizontal=True, parent=window)
    #     button = dpg.add_button(label="Save the tour", callback=cls.modified_window_callback, parent=group)
    #     status = dpg.add_text(default_value="Status", parent=group)
    #     dpg.set_item_user_data(
    #         button, 
    #         {
    #             'window': window,
    #             'status': status,
    #             'id': customer.id,
    #             'items': [
    #                 {
    #                     'field': 'name',
    #                     'name': 'Customer name',
    #                     'item': customer_name,
    #                 },
    #                 {
    #                     'field': 'id_number',
    #                     'name': 'ID number',
    #                     'item': customer_id_number,
    #                 },
    #                 {
    #                     'field': 'address',
    #                     'name': 'Address',
    #                     'item': customer_address,
    #                 },
    #                 {
    #                     'field': 'gender',
    #                     'name': 'Gender',
    #                     'item': customer_gender,
    #                 },
    #                 {
    #                     'field': 'phone_number',
    #                     'name': 'Phone number',
    #                     'item': customer_phone_number,
    #                 }
    #             ]
    #         }
    #     )

    # @classmethod
    # def modified_window_callback(cls, sender, app_data, user_data):
    #     is_valid = True
    #     request_data = {}
        
    #     for item in user_data['items']:
    #         data = dpg.get_value(item['item'])
    #         if data != "": 
    #             print(data)
    #             request_data[item['field']] = data
    #             if item['field'] == 'id_number':
    #                 pattern_id_number = re.compile('^([0-9]{9}|[0-9]{12})+$')
    #                 if pattern_id_number.match(data) is None:
    #                     is_valid = False
    #                     dpg.configure_item(user_data['status'], default_value=f'Status: {item["name"]} is not id number', color=[255, 92, 88])

    #             if item['field'] == 'phone_number':
    #                 pattern_id_number = re.compile('^([0-9]{10}|[0-9]{11})+$')
    #                 if pattern_id_number.match(data) is None:
    #                     is_valid = False
    #                     dpg.configure_item(user_data['status'], default_value=f'Status: {item["name"]} is not phone number', color=[255, 92, 88])
    #         else:
    #             is_valid = False
    #             dpg.configure_item(user_data['status'], default_value=f'Status: {item["name"]} is invalid', color=[255, 92, 88])               
    #             break
            
    #     if is_valid:
    #         dpg.configure_item(user_data['status'], default_value=f'Status: OK', color=[128, 237, 153]) 
    #         print(request_data)
            
    #         customer_obj = Customer(
    #             id=user_data['id'],
    #             name=request_data['name'],
    #             id_number=request_data['id_number'],
    #             address=request_data['address'],
    #             gender=request_data['gender'],
    #             phone_number=request_data['phone_number']
    #         ) 
    #         customer_bus = CustomerBUS()
    #         error = customer_bus.update(customer_obj)
            
    #         if error.status is True:
    #             dpg.configure_item(user_data['status'], default_value=f'Status: {error.message}', color=[255, 92, 88])
    #         else:
    #             dpg.delete_item(user_data['window'])
    #             cls.content_render("customer")
        
    #     customers = CustomerBUS().objects
    #     customer = [c for c in customers if c.id == user_data['id']][0]
    #     print(customer)
    

    # @classmethod
    # def delete_window(cls, sender, app_data, user_data):
    #     customer_id = user_data
    #     window = dpg.add_window(label="Modified the tour", width=400, autosize=True, pos=[500, 200])

    #     question = dpg.add_text(default_value=f"Do you want to delete the customer (id: {customer_id})?", parent=window)
    #     status = dpg.add_text(default_value="Status", parent=window)
        
    #     group = dpg.add_group(horizontal=True, parent=window)
        
    #     user_data = {
    #         'customer_id': customer_id,
    #         'status': status,
    #         'window': window
    #     }
    #     button_yes = dpg.add_button(label="Yes", callback=cls.delete_window_callback, user_data=user_data, parent=group)
    #     button_no = dpg.add_button(label="Cancel", callback=lambda :dpg.delete_item(window), parent=group)

    # @classmethod
    # def delete_window_callback(cls, sender, app_data, user_data):
    #     error = CustomerBUS().delete(user_data['customer_id'])
    #     if error.status is True:
    #         dpg.configure_item(user_data['status'], default_value=f'Status: {error.message}', color=[255, 92, 88])
    #     else:
    #         dpg.configure_item(user_data['status'], default_value=f'Status: OK', color=[128, 237, 153])
    #         dpg.delete_item(user_data['window'])
    #         cls.content_render('customer')

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
        # dpg.add_table_column(width_fixed=False, parent=table)

        if is_action is True:
            dpg.add_table_column(label="Action", parent=table, no_sort=True)
        
        for row in data:
            table_row = dpg.add_table_row(parent=table)
            for d in row:
                if type(d) == list:
                    data = []
                    for j in d:
                        content = f"{str(j.start_date.strftime('%Y-%m-%d'))} | {str(j.start_date.strftime('%Hh%M'))}-{str(j.end_date.strftime('%Hh%M'))} : {j.content}"
                        data.append(content)
                    dpg.add_combo(items=data, parent=table_row, no_preview=True)
                else:
                    dpg.add_text(d, parent=table_row)
            
            if is_action is True:
                action_group = dpg.add_group(horizontal=True, parent=table_row)
                # modified_button= dpg.add_button(label='M', parent=action_group, callback=modified_callback, user_data=row[0])
                # delete_button = dpg.add_button(label='D', parent=action_group, callback=delete_callback, user_data=row[0])
                view_button = dpg.add_button(label='V', parent=action_group, callback=view_callback, user_data=row[0])
                # tooltip_modified_button = dpg.add_tooltip(parent=modified_button)
                # tooltip_delete_button = dpg.add_tooltip(parent=delete_button)
                tooltip_view_button = dpg.add_tooltip(parent=view_button)
                # dpg.add_text("Modified", parent=tooltip_modified_button)
                # dpg.add_text("Delete", parent=tooltip_delete_button)
                dpg.add_text("View Staff's Tours", parent=tooltip_view_button)
                dpg.add_selectable(parent=action_group, span_columns=True)
            

        dpg.configure_item(table, user_data=type_column_map)    
        
        return table

    @classmethod
    def view_window(cls, sender, app_data, user_data):
        staff_group = [sg for sg in StatsToursOfStaffBUS().objects if sg.id == user_data][0]
        group = GroupBUS()
        group_data = group.objects
        group_staff = GroupStaffBUS()
        # group_staff_data = group_staff.objects
        group_list = []
        staff_group_list = []
        header = ['id', 'name', 'start_date','end_date']
        datetime_type = lambda d: datetime.strptime(d, '%Y-%m-%d')
        type_columns = [int, str, datetime_type,datetime_type]
        window = dpg.add_window(label="Staff_groups", width=400, autosize=True, pos=[500, 200])
        
        for d in group_data:
            group_data_list = [ gdl for gdl in group_staff.read(d.id)]
            for gl in group_data_list:
                if gl.staff.id == user_data:
                    staff_group_list.append([
                        d.id,
                        d.name,
                        d.start_date,
                        d.end_date
                    ])

        table = cls.init_table(
            header=header,
            data=staff_group_list,
            parent=window,
            type_columns=type_columns,
            is_action=False,
            modified_callback=None,
            delete_callback=None,
            view_callback=None
        )
            
            
        

        dpg.add_button(label="Close", callback=lambda :dpg.delete_item(window), parent=window)