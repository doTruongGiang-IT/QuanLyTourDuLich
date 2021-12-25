import dearpygui.dearpygui as dpg
from BUS.customer import CustomerBUS, GroupCustomerBUS
from DTO.customer import Customer
from BUS.group import GroupBUS
from DAO.customer import GroupCustomerDAO
from ..base_table import init_table
import re

class CustomerCustomerGUI:
    group_content_window = None
    table = None

    @classmethod
    def content_render(cls, data, choice_default=None):
        dpg.delete_item(cls.group_content_window, children_only=True)
        #dpg.add_text(default_value=data, parent=cls.group_content_window)
        cls.table = None

        if choice_default is None:
            choice_default = 'All'

        groups = ['All']
        groups += [f'{g.id} | {g.name}' for g in GroupBUS().objects]

        high_top_group = dpg.add_group(horizontal=True, parent=cls.group_content_window)
        dpg.add_text(default_value=data, parent=high_top_group)
        group_combo = dpg.add_combo(label="Group", items=groups, parent=high_top_group, default_value=choice_default, callback=cls.choice_group_combo)
        
        top_group = dpg.add_group(horizontal=True, parent=cls.group_content_window)
        dpg.add_button(label="Add new customer", callback=cls.create_window, parent=top_group)
        #dpg.add_button(label="Add a customer to a group", parent=top_group)
        search_text = dpg.add_input_text(label="Search", parent=top_group, on_enter=True)
        column_search = dpg.add_combo(label="Columns", items=['all', 'name', 'id number', 'address', 'gender', 'phone number'], parent=top_group, default_value='all')
        dpg.set_item_user_data(search_text, {
            'group': group_combo,
            'column': column_search
        })
        dpg.set_item_callback(search_text, cls.search_callback)

        cls.choice_group_combo(group_combo, choice_default)


    @classmethod
    def choice_group_combo(cls, sender, app_data):
        header = ['id', 'name', 'id number', "address", "gender", "phone number"]
        type_columns = [int, str, str, str, str, str]

        if app_data == 'All':
            data = []
            customer_bus = CustomerBUS()
            customer_data = customer_bus.objects
            for c in customer_data:
                data.append([
                    c.id,
                    c.name,
                    c.id_number,
                    c.address,
                    c.gender,
                    c.phone_number
                ])

            if cls.table is not None:
                dpg.delete_item(cls.table)
                cls.table = None

            cls.table = init_table(
                header=header,
                data=data,
                parent=cls.group_content_window,
                type_columns=type_columns,
                is_action=True,
                modified_callback=cls.modified_window,
                delete_callback=cls.delete_window,
                view_callback=cls.view_window
            )
        else:
            group_id = int(app_data.split('|')[0])

            data = []
            group_customer_bus = GroupCustomerBUS()
            group_customer_data = group_customer_bus.read(group_id)
            for gc in group_customer_data:
                customer_bus = CustomerBUS()
                customer = [c for c in customer_bus.objects if c.id == gc.customer][0]
                data.append([
                    customer.id,
                    customer.name,
                    customer.id_number,
                    customer.address,
                    customer.gender,
                    customer.phone_number
                ])
            
            if cls.table is not None:
                    dpg.delete_item(cls.table)
                    cls.table = None

            cls.table = init_table(
                    header=header,
                    data=data,
                    parent=cls.group_content_window,
                    type_columns=type_columns,
                    is_action=True,
                    modified_callback=cls.modified_window,
                    delete_callback=cls.delete_window,
                    view_callback=cls.view_window
            )

    @classmethod
    def create_window(cls):
        window = dpg.add_window(label="Add new customer", width=400, autosize=True, pos=[500, 200])

        customer_name = dpg.add_input_text(label="Name ", parent=window)
        customer_id_number = dpg.add_input_text(label="ID number ", parent=window)
        customer_address = dpg.add_input_text(label="Address ", parent=window)
        datas = ["Male", "Female", "Other"]
        customer_gender = dpg.add_combo(label="Gender ", items=datas, parent=window)
        customer_phone_number = dpg.add_input_text(label="Phone number ", parent=window)
        
        group = dpg.add_group(horizontal=True, parent=window)
        button = dpg.add_button(label="Add new tour", callback=cls.create_window_callback, parent=group)
        status = dpg.add_text(default_value="Status", parent=group)
        dpg.set_item_user_data(
            button, 
            {
                'window': window,
                'status': status, 
                'items': [
                    {
                        'field': 'name',
                        'name': 'Customer name',
                        'item': customer_name,
                    },
                    {
                        'field': 'id_number',
                        'name': 'ID number',
                        'item': customer_id_number,
                    },
                    {
                        'field': 'address',
                        'name': 'Address',
                        'item': customer_address,
                    },
                    {
                        'field': 'gender',
                        'name': 'Gender',
                        'item': customer_gender,
                    },
                    {
                        'field': 'phone_number',
                        'name': 'Phone number',
                        'item': customer_phone_number,
                    }
                ]
            }
        )

    @classmethod
    def create_window_callback(cls, sender, app_data, user_data):
        is_valid = True
        request_data = {}
        
        for item in user_data['items']:
            data = dpg.get_value(item['item'])
            if data != "": 
                request_data[item['field']] = data
                if item['field'] == 'id_number':
                    pattern_id_number = re.compile('^([0-9]{9}|[0-9]{12})+$')
                    if pattern_id_number.match(data) is None:
                        is_valid = False
                        dpg.configure_item(user_data['status'], default_value=f'Status: {item["name"]} is not id number', color=[255, 92, 88])

                if item['field'] == 'phone_number':
                    pattern_id_number = re.compile('^([0-9]{10}|[0-9]{11})+$')
                    if pattern_id_number.match(data) is None:
                        is_valid = False
                        dpg.configure_item(user_data['status'], default_value=f'Status: {item["name"]} is not phone number', color=[255, 92, 88])
            else:
                is_valid = False
                dpg.configure_item(user_data['status'], default_value=f'Status: {item["name"]} is invalid', color=[255, 92, 88])               
                break
            
        if is_valid:
            dpg.configure_item(user_data['status'], default_value=f'Status: OK', color=[128, 237, 153]) 
            
            customer_obj = Customer(
                id=0,
                name=request_data['name'],
                id_number=request_data['id_number'],
                address=request_data['address'],
                gender=request_data['gender'],
                phone_number=request_data['phone_number']
            ) 
            customer_bus = CustomerBUS()
            error = customer_bus.create(customer_obj)
            
            if error.status is True:
                dpg.configure_item(user_data['status'], default_value=f'Status: {error.message}', color=[255, 92, 88])
            else:
                dpg.delete_item(user_data['window'])
                cls.content_render("customer")

    @classmethod
    def modified_window(cls, sender, app_data, user_data):
        customers = CustomerBUS().objects
        
        customer = [c for c in customers if c.id == user_data][0]
        
        window = dpg.add_window(label="Modified the customer", width=400, autosize=True, pos=[500, 200])
        customer_id = dpg.add_text(default_value=f"id: {customer.id}", parent=window)
        customer_name = dpg.add_input_text(label="Name ", default_value=customer.name, parent=window)
        customer_id_number = dpg.add_input_text(label="ID number ", default_value=customer.id_number, parent=window)
        customer_address = dpg.add_input_text(label="Address ", default_value=customer.address, parent=window)
        datas = ["Male", "Female", "Other"]
        customer_gender = dpg.add_combo(label="Gender ", items=datas, default_value=customer.gender, parent=window)
        customer_phone_number = dpg.add_input_text(label="Phone number ", default_value=customer.phone_number, parent=window)
        
        group = dpg.add_group(horizontal=True, parent=window)
        button = dpg.add_button(label="Save the tour", callback=cls.modified_window_callback, parent=group)
        status = dpg.add_text(default_value="Status", parent=group)
        dpg.set_item_user_data(
            button, 
            {
                'window': window,
                'status': status,
                'id': customer.id,
                'items': [
                    {
                        'field': 'name',
                        'name': 'Customer name',
                        'item': customer_name,
                    },
                    {
                        'field': 'id_number',
                        'name': 'ID number',
                        'item': customer_id_number,
                    },
                    {
                        'field': 'address',
                        'name': 'Address',
                        'item': customer_address,
                    },
                    {
                        'field': 'gender',
                        'name': 'Gender',
                        'item': customer_gender,
                    },
                    {
                        'field': 'phone_number',
                        'name': 'Phone number',
                        'item': customer_phone_number,
                    }
                ]
            }
        )

    @classmethod
    def modified_window_callback(cls, sender, app_data, user_data):
        is_valid = True
        request_data = {}
        
        for item in user_data['items']:
            data = dpg.get_value(item['item'])
            if data != "": 
                request_data[item['field']] = data
                if item['field'] == 'id_number':
                    pattern_id_number = re.compile('^([0-9]{9}|[0-9]{12})+$')
                    if pattern_id_number.match(data) is None:
                        is_valid = False
                        dpg.configure_item(user_data['status'], default_value=f'Status: {item["name"]} is not id number', color=[255, 92, 88])

                if item['field'] == 'phone_number':
                    pattern_id_number = re.compile('^([0-9]{10}|[0-9]{11})+$')
                    if pattern_id_number.match(data) is None:
                        is_valid = False
                        dpg.configure_item(user_data['status'], default_value=f'Status: {item["name"]} is not phone number', color=[255, 92, 88])
            else:
                is_valid = False
                dpg.configure_item(user_data['status'], default_value=f'Status: {item["name"]} is invalid', color=[255, 92, 88])               
                break
            
        if is_valid:
            dpg.configure_item(user_data['status'], default_value=f'Status: OK', color=[128, 237, 153]) 
            
            customer_obj = Customer(
                id=user_data['id'],
                name=request_data['name'],
                id_number=request_data['id_number'],
                address=request_data['address'],
                gender=request_data['gender'],
                phone_number=request_data['phone_number']
            ) 
            customer_bus = CustomerBUS()
            error = customer_bus.update(customer_obj)
            
            if error.status is True:
                dpg.configure_item(user_data['status'], default_value=f'Status: {error.message}', color=[255, 92, 88])
            else:
                dpg.delete_item(user_data['window'])
                cls.content_render("customer")
        
        customers = CustomerBUS().objects
        customer = [c for c in customers if c.id == user_data['id']][0]
    

    @classmethod
    def delete_window(cls, sender, app_data, user_data):
        customer_id = user_data
        window = dpg.add_window(label="Modified the tour", width=400, autosize=True, pos=[500, 200])

        question = dpg.add_text(default_value=f"Do you want to delete the customer (id: {customer_id})?", parent=window)
        status = dpg.add_text(default_value="Status", parent=window)
        
        group = dpg.add_group(horizontal=True, parent=window)
        
        user_data = {
            'customer_id': customer_id,
            'status': status,
            'window': window
        }
        button_yes = dpg.add_button(label="Yes", callback=cls.delete_window_callback, user_data=user_data, parent=group)
        button_no = dpg.add_button(label="Cancel", callback=lambda :dpg.delete_item(window), parent=group)

    @classmethod
    def delete_window_callback(cls, sender, app_data, user_data):
        error = CustomerBUS().delete(user_data['customer_id'])
        if error.status is True:
            dpg.configure_item(user_data['status'], default_value=f'Status: {error.message}', color=[255, 92, 88])
        else:
            dpg.configure_item(user_data['status'], default_value=f'Status: OK', color=[128, 237, 153])
            dpg.delete_item(user_data['window'])
            cls.content_render('customer')

    @classmethod
    def view_window(cls, sender, app_data, user_data):
        customer = [g for g in CustomerBUS().objects if g.id == user_data][0]
        
        window = dpg.add_window(label="Modified the tour", width=400, autosize=True, pos=[500, 200])
        dpg.add_text(default_value=f"id: {customer.id}", parent=window)
        dpg.add_text(default_value=f"Name: {customer.name}", parent=window)
        dpg.add_text(default_value=f"ID number: {customer.id_number}", parent=window)
        dpg.add_text(default_value=f"Address: {customer.address}", parent=window)
        dpg.add_text(default_value=f"Gender: {customer.gender}", parent=window)
        dpg.add_text(default_value=f"Phone number: {customer.phone_number}", parent=window)

        dpg.add_button(label="Close", callback=lambda :dpg.delete_item(window), parent=window)

    @classmethod
    def search_callback(cls,sender, app_data, user_data):
        customer_bus = CustomerBUS()
        customer = []
        if dpg.get_value(user_data['group']) != 'All':
            group_id = int(dpg.get_value(user_data['group']).split('|')[0])
            group_customer_bus = GroupCustomerBUS()
            group_customer_data = group_customer_bus.read(group_id)
            for gc in group_customer_data:
                customer.append([ c for c in customer_bus.objects if c.id == gc.customer][0])
        if dpg.get_value(user_data['group']) == 'All':
            customer = customer_bus.objects
        header = ['id', 'name', 'id number', "address", "gender", "phone number"]
        type_columns = [int, str, str, str, str, str]
        data = []
        column_search = dpg.get_value(user_data['column'])
        if (column_search == 'all'):
            for c in customer:
                multi_strings = f"{c.id} | {c.name} | {c.id_number} | {c.address} | {c.gender} | {c.phone_number}"
                search = re.search(app_data, multi_strings)
                if (search):
                    data.append([
                        c.id,
                        c.name,
                        c.id_number,
                        c.address,
                        c.gender,
                        c.phone_number
                    ])
        if (column_search == 'name'):
            for c in customer:
                search = re.search(app_data, c.name)
                if (search):
                    data.append([
                        c.id,
                        c.name,
                        c.id_number,
                        c.address,
                        c.gender,
                        c.phone_number
                    ])
        if (column_search == 'id number'):
            for c in customer:
                search = re.search(app_data, c.id_number)
                if (search):
                    data.append([
                        c.id,
                        c.name,
                        c.id_number,
                        c.address,
                        c.gender,
                        c.phone_number
                    ])
        if (column_search == 'address'):
            for c in customer:
                search = re.search(app_data, c.address)
                if (search):
                    data.append([
                        c.id,
                        c.name,
                        c.id_number,
                        c.address,
                        c.gender,
                        c.phone_number
                    ])
        if (column_search == 'gender'):
            for c in customer:
                search = re.search(app_data, c.gender)
                if (search):
                    data.append([
                        c.id,
                        c.name,
                        c.id_number,
                        c.address,
                        c.gender,
                        c.phone_number
                    ])
        if (column_search == 'phone number'):
            for c in customer:
                search = re.search(app_data, c.phone_number)
                if (search):
                    data.append([
                        c.id,
                        c.name,
                        c.id_number,
                        c.address,
                        c.gender,
                        c.phone_number
                    ])
        
        dpg.delete_item(cls.table)
        cls.table= init_table(
                header=header,
                data=data,
                parent=cls.group_content_window,
                type_columns=type_columns,
                is_action=True,
                modified_callback=cls.modified_window,
                delete_callback=cls.delete_window,
                view_callback=cls.view_window
            )