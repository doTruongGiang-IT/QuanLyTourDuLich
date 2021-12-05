import React, {useState} from 'react';
import './GuestsForm.css';
import { useParams } from 'react-router';
import { Table, Input, Button, Space, Popconfirm, Form, notification, Select} from 'antd';
import { SearchOutlined, DeleteOutlined } from '@ant-design/icons';
import EditableCell from '../EditableCell/EditableCell';

const { Option } = Select;
const layout = {
  labelCol: {
    span: 7,
  },
  wrapperCol: {
    span: 14,
  },
};

const tailLayout = {
  wrapperCol: {
    offset: 7,
    span: 14,
  },
};

const GuestsForm = ({customerGroup, remove, submit, customers}) => {
    let {id} = useParams();
    const customerlist = useState([]);
    const [searchText, setSearchText] = useState("");
    const [searchedColumn, setSearchedColumn] = useState("");
    const [form] = Form.useForm();
    const [api, contextHolder] = notification.useNotification();
    const Context = React.createContext();
    let temp = [];

    for(let i = 0; i < customers.length; i++) {
        for(let j = 0; j < customerGroup.length; j++) {
            if(customers[i].id === customerGroup[j].customer) {
                temp.push(customers[i]);
            };
        };
    };

    temp = temp.map((cus, index) => {
        return {key: index, ...cus};
    });

    const onFinish = (values) => {
        submit({group: Number.parseInt(id), customer: values.customer});
        form.resetFields();
    };
    
      const onReset = () => {
        form.resetFields();
    };

    const getColumnSearchProps = dataIndex => ({
        filterDropdown: ({ setSelectedKeys, selectedKeys, confirm, clearFilters }) => (
          <div style={{ padding: 8 }}>
            <Input
              placeholder={`Search ${dataIndex}`}
              value={selectedKeys[0]}
              onChange={e => setSelectedKeys(e.target.value ? [e.target.value] : [])}
              onPressEnter={() => handleSearch(selectedKeys, confirm, dataIndex)}
              style={{ marginBottom: 8, display: 'block' }}
            />
            <Space>
              <Button
                type="primary"
                onClick={() => handleSearch(selectedKeys, confirm, dataIndex)}
                icon={<SearchOutlined />}
                size="small"
                style={{ width: 90 }}
              >
                Search
              </Button>
              <Button onClick={() => handleReset(clearFilters)} size="small" style={{ width: 90 }}>
                Reset
              </Button>
              <Button
                type="link"
                size="small"
                onClick={() => {
                  confirm({ closeDropdown: false });
                  setSearchText(selectedKeys[0]);
                  setSearchedColumn(dataIndex);
                }}
              >
                Filter
              </Button>
            </Space>
          </div>
        ),
        filterIcon: filtered => <SearchOutlined style={{ color: filtered ? '#1890ff' : undefined }} />,
        onFilter: (value, record) =>
          record[dataIndex]
            ? record[dataIndex].toString().toLowerCase().includes(value.toLowerCase())
            : '',
        render: text => text,
    });

    const handleSearch = (selectedKeys, confirm, dataIndex) => {
        confirm();
        setSearchText(selectedKeys[0]);
        setSearchedColumn(dataIndex);
    };
    
    const handleReset = clearFilters => {
        clearFilters();
        setSearchText({ searchText: '' });
    };

    const handleDelete = (value) => {
        // setDataInfo(data.filter((item) => item.key !== key));
        remove(value);
        openNotification("Deleted");
    };

    const columns = [
        {
            title: 'ID',
            dataIndex: 'id',
            key: 'id',
            width: '10%',
            ...getColumnSearchProps('id'),
        },
        {
            title: 'Name',
            dataIndex: 'name',
            key: 'name',
            width: '20%',
            ...getColumnSearchProps('name'),
            sorter: {
              compare: (a, b) => new Date(a.startDate) - new Date(b.startDate),
            //   multiple: tourDetails.length
            },
            sortDirections: ['descend', 'ascend'],
        },
        {
            title: 'Identify',
            dataIndex: 'id_number',
            key: 'id_number',
            width: '10%',
            ...getColumnSearchProps('id_number'),
        },
        {
            title: 'Address',
            dataIndex: 'address',
            key: 'address',
            width: '30%',
            ...getColumnSearchProps('address'),
        },
        {
            title: 'Gender',
            dataIndex: 'gender',
            key: 'gender',
            width: '10%',
            ...getColumnSearchProps('gender'),
        },
        {
            title: 'Phone',
            dataIndex: 'phone_number',
            key: 'phone_number',
            width: '10%',
            ...getColumnSearchProps('phone_number'),
        },
        {
            title: 'Actions',
            dataIndex: 'actions',
            key: 'actions',
            width: '10%',
            render: (_, record) => {
                return (
                    <Popconfirm title="Sure to delete?" onConfirm={() => handleDelete({group_id: Number.parseInt(id), customer_id: record.id})}>
                        <Button
                            type="primary"
                            icon={<DeleteOutlined />}
                            size="medium"
                            style={{ width: 90 }}
                            danger
                        />
                    </Popconfirm>
                )
            },
        },
    ];

    const openNotification = placement => {
        api.info({
            message: `Notification`,
            description: <Context.Consumer>{() => `${placement} Success!`}</Context.Consumer>,
        });
    };


    return (
        <div className="guestsForm">
            <h2>Guest list for group {id}</h2>
            {contextHolder}
            <div className="guestContent">
                <div className="guestList">
                    <Form form={form} component={false}>
                        <Table components={{
                            body: {
                                cell: EditableCell,
                            },
                        }} 
                        bordered columns={columns} dataSource={temp} pagination={{defaultPageSize: 20}} scroll={{ y: 500}} />
                    </Form>
                </div>
                <div className="guestAddForm">
                    <h2>ADD FORM</h2>
                    <Form {...layout} form={form} name="control-hooks" onFinish={onFinish}>
                        <Form.Item
                            name="customer"
                            label="Customer"
                            rules={[
                                {
                                    required: true,
                                },
                            ]}
                        >
                            <Select placeholder="Select customer" allowClear>
                                {
                                    customers ?
                                    customers.map((customer, index) => {
                                        return <Option key={index} value={customer.id}>{customer.name}</Option>
                                    }) : null
                                }
                            </Select>
                        </Form.Item>
                        <Form.Item {...tailLayout}>
                            <Space>
                                <Button type="primary" htmlType="submit">
                                    Submit
                                </Button>
                                <Button htmlType="button" onClick={onReset}>
                                    Reset
                                </Button>
                            </Space>
                        </Form.Item>
                    </Form>
                </div>
            </div>
        </div>
    )
}

export default GuestsForm;
