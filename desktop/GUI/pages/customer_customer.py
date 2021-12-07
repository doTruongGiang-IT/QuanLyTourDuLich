import dearpygui.dearpygui as dpg
from BUS.customer import CustomerBUS
from DTO.customer import Customer
from ..base_table import init_table

class CustomerCustomerGUI:
    group_content_window = None

    @classmethod
    def content_render(cls, data):
        dpg.delete_item(cls.group_content_window, children_only=True)
        dpg.add_text(default_value=data, parent=cls.group_content_window)
        
        top_group = dpg.add_group(horizontal=True, parent=cls.group_content_window)
        dpg.add_button(label="Add new customer", callback=cls.create_window, parent=top_group)
        dpg.add_input_text(label="Search", parent=top_group)
        dpg.add_combo(label="Columns", items=['column1', 'column2', 'column3'], parent=top_group)
        
        header = ['id', 'name', 'id number', "address", "gender", "phone number"]
        type_columns = [int, str, str, str, str, str]
        data = []
        customer_bus = CustomerBUS()
        tour_data = customer_bus.objects

        for d in tour_data:
            data.append([
                d.id,
                d.name,
                d.id_number,
                d.address,
                d.gender,
                d.phone_number
            ])
        
        table = init_table(
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
                print(data)
                request_data[item['field']] = data
            else:
                is_valid = False
                dpg.configure_item(user_data['status'], default_value=f'Status: {item["name"]} is invalid', color=[255, 92, 88])               
                break
            
        if is_valid:
            dpg.configure_item(user_data['status'], default_value=f'Status: OK', color=[128, 237, 153]) 
            print(request_data)
            
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
                print(data)
                request_data[item['field']] = data
            else:
                is_valid = False
                dpg.configure_item(user_data['status'], default_value=f'Status: {item["name"]} is invalid', color=[255, 92, 88])               
                break
            
        if is_valid:
            dpg.configure_item(user_data['status'], default_value=f'Status: OK', color=[128, 237, 153]) 
            print(request_data)
            
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
        print(customer)
    

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