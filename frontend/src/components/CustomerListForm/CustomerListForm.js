import React, {useState} from 'react';
import './CustomerListForm.css';
import 'antd/dist/antd.css';
import { Table, Input, Button, Space, Popconfirm, Form, notification, Modal} from 'antd';
import { SearchOutlined, DeleteOutlined, EditOutlined, EyeOutlined, BookOutlined } from '@ant-design/icons';
import EditableCell from '../EditableCell/EditableCell';
import { Link } from 'react-router-dom';
import { useHistory } from 'react-router';

const CustomerListForm = ({remove, update, customers}) => {
    const [searchText, setSearchText] = useState("");
    const [searchedColumn, setSearchedColumn] = useState("");
    const [form] = Form.useForm();
    const [editData, setEditData] = useState([]);
    const [editingKey, setEditingKey] = useState('');
    const [tourLocations, setTourLocations] = useState("");
    const [api, contextHolder] = notification.useNotification();
    const Context = React.createContext();
    const history = useHistory();
    let customerList = customers ? customers.map((customer) => {
        return {key: customer.id + 1, ...customer};
    }) : [];

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

    const handleDelete = (id) => {
        // setDataInfo(data.filter((item) => item.key !== key));
        remove(id);
        openNotification("Deleted");
    };

    const isEditing = (record) => record.key === editingKey;

    const edit = (record) => {
        form.setFieldsValue({
        ...record,
        });
        setEditingKey(record.key);
    };

    const cancel = () => {
        setEditingKey('');
    };

    const saveEdit = async (id) => {
        try {
          const row = await form.validateFields();
          const newData = [...customerList];
          const index = newData.findIndex((item) => id === item.id);
    
          if (index > -1) {
            const item = newData[index];
            newData.splice(index, 1, { ...item, ...row });
            setEditData(newData);
            update(newData[index]);
            // setDataInfo(newData);
            setEditingKey('');
            openNotification("Update");
          } else {
            newData.push(row);
            setEditData(newData);
            setEditingKey('');
          }
        } catch (errInfo) {
          console.log('Validate Failed:', errInfo);
        }
    };

    const quickSort = (values) => {
        if (values.length <= 1) {
            return values
        };

        var lessThanPivot = [];
        var greaterThanPivot = [];
        var pivot = values[0];
        for (var i = 1; i < values.length; i++) {
            if (values[i].id <= pivot.id) {
                lessThanPivot.push(values[i]);
            } else {
                greaterThanPivot.push(values[i]);
            }
        }
        return quickSort(lessThanPivot).concat(pivot, quickSort(greaterThanPivot));
    };

    customerList = quickSort(customerList);

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
            editable: true,
            ...getColumnSearchProps('name'),
            sorter: (a, b) => a.name.length - b.name.length,
            sortDirections: ['descend', 'ascend'],
        },
        {
            title: 'Identify',
            dataIndex: 'id_number',
            key: 'id_number',
            width: '10%',
            editable: true,
            ...getColumnSearchProps('id_number'),
        },
        {
            title: 'Address',
            dataIndex: 'address',
            key: 'address',
            width: '30%',
            editable: true,
            ...getColumnSearchProps('address'),
        },
        {
            title: 'Gender',
            dataIndex: 'gender',
            key: 'gender',
            width: '10%',
            editable: true,
            ...getColumnSearchProps('gender'),
        },
        {
            title: 'Phone',
            dataIndex: 'phone_number',
            key: 'phone_number',
            width: '10%',
            editable: true,
            ...getColumnSearchProps('phone_number'),
        },
        {
            title: 'Actions',
            width: '10%',
            render: (_, record) => {
                const editable = isEditing(record);
                return editable ? (
                    <Space>
                        <Button
                            onClick={() => saveEdit(record.id)}
                            type="primary"
                            size="medium"
                            style={{ width: 70 }}
                        >
                            Save
                        </Button>
                        <Popconfirm title="Sure to cancel?" onConfirm={cancel}>
                            <Button
                                type="primary"
                                size="medium"
                                style={{ width: 70 }}
                                danger
                            >
                                Cancel
                            </Button>
                        </Popconfirm>
                    </Space> 
                ) : (
                    <Space>
                        <Popconfirm title="Sure to delete?" onConfirm={() => handleDelete(record.id)}>
                            <Button
                                type="primary"
                                icon={<DeleteOutlined />}
                                size="medium"
                                style={{ width: 70 }}
                                danger
                            />
                        </Popconfirm>
                        <Button
                            disabled={editingKey !== ''} 
                            onClick={() => edit(record)}
                            type="primary"
                            icon={<EditOutlined />}
                            size="medium"
                            style={{ width: 70 }}
                        />
                        {/* <Button
                            disabled={editingKey !== ''} 
                            // onClick={() => history.push(`/details/${record.id}`)}
                            type="primary"
                            icon={<EyeOutlined />}
                            size="small"
                            style={{ width: 50 }}
                        /> */}
                    </Space>   
                )
            },
        },
    ];

    const mergedColumns = columns.map((col) => {
        if (!col.editable) {
          return col;
        }
    
        return {
          ...col,
          onCell: (record) => ({
            record,
            inputType: 'text',
            dataIndex: col.dataIndex,
            title: col.title,
            editing: isEditing(record),
          }),
        };
    });

    const openNotification = placement => {
        api.info({
            message: `Notification`,
            description: <Context.Consumer>{() => `${placement} Success!`}</Context.Consumer>,
        });
    };

    return (
        <div className="customerListForm">
            {contextHolder}
            <Link id="addTour" to="/create_customer">Create Customer</Link>
            <Form form={form} component={false}>
                <Table components={{
                    body: {
                        cell: EditableCell,
                    },
                }} 
                bordered columns={mergedColumns} dataSource={customerList} pagination={{defaultPageSize: 20}} scroll={{x: "max-content" }} />
            </Form>
        </div>
    )
}

export default CustomerListForm;
