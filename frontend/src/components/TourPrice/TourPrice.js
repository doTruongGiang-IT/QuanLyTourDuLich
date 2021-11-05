import React, {useState} from 'react';
import '../GuestsForm/GuestsForm.css';
import { Table, Input, Button, Space, Popconfirm, Form, notification, DatePicker, InputNumber } from 'antd';
import { SearchOutlined, DeleteOutlined, EditOutlined } from '@ant-design/icons';
import EditableCell from '../EditableCell/EditableCell';

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

const { RangePicker } = DatePicker;

const TourPrice = () => {
    const [searchText, setSearchText] = useState("");
    const [searchedColumn, setSearchedColumn] = useState("");
    const [form] = Form.useForm();
    const [editData, setEditData] = useState([]);
    const [editingKey, setEditingKey] = useState('');
    const [selectedRowKeys, setSelectedKeys] = useState([]);
    const [api, contextHolder] = notification.useNotification();
    const Context = React.createContext();

    const onFinish = (values) => {
        // submit(values);
        form.resetFields();
        console.log(values);
    };
    
      const onReset = () => {
        form.resetFields();
    };

    const onSelectChange = (selectedRowKeys) => {
        setSelectedKeys(selectedRowKeys);
    };

    const rowSelection = {
        selectedRowKeys,
        onChange: onSelectChange,
        selections: [
          Table.SELECTION_ALL,
          Table.SELECTION_INVERT,
          Table.SELECTION_NONE,
          {
            key: 'odd',
            text: 'Select Odd Row',
            onSelect: changableRowKeys => {
                let newSelectedRowKeys = [];
                newSelectedRowKeys = changableRowKeys.filter((key, index) => {
                    if (index % 2 !== 0) {
                        return false;
                    };
                    return true;
                });
                setSelectedKeys(newSelectedRowKeys);
            },
          },
          {
            key: 'even',
            text: 'Select Even Row',
            onSelect: changableRowKeys => {
                let newSelectedRowKeys = [];
                newSelectedRowKeys = changableRowKeys.filter((key, index) => {
                    if (index % 2 !== 0) {
                        return true;
                    };
                    return false;
                });
                setSelectedKeys(newSelectedRowKeys);
            },
          },
          {
            key: 'delete',
            text: 'Delete Selected Rows',
            onSelect: () => {
                if(selectedRowKeys.length > 0) {
                    selectedRowKeys.forEach(async (selectedRowKey) => await handleDelete(selectedRowKey-1));
                };
                setSelectedKeys([]);
            },
          },
        ],
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

    const handleDelete = (id) => {
        // setDataInfo(data.filter((item) => item.key !== key));
        // remove(id);
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

    // const saveEdit = async (id) => {
    //     try {
    //       const row = await form.validateFields();
    //       const newData = [...tourList];
    //       const index = newData.findIndex((item) => id === item.id);
    
    //       if (index > -1) {
    //         const item = newData[index];
    //         newData.splice(index, 1, { ...item, ...row });
    //         setEditData(newData);
    //         // update(newData[index]);
    //         setEditingKey('');
    //         openNotification("Update");
    //       } else {
    //         newData.push(row);
    //         setEditData(newData);
    //         setEditingKey('');
    //       }
    //     } catch (errInfo) {
    //       console.log('Validate Failed:', errInfo);
    //     }
    // };

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

    // tourList = quickSort(tourList);

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
            sorter: {
              compare: (a, b) => new Date(a.startDate) - new Date(b.startDate),
            //   multiple: tourDetails.length
            },
            sortDirections: ['descend', 'ascend'],
        },
        {
            title: 'Price',
            dataIndex: 'price',
            key: 'price',
            width: '15%',
            editable: true,
            ...getColumnSearchProps('price'),
        },
        {
            title: 'Start Date',
            dataIndex: 'start_date',
            key: 'start_date',
            width: '20%',
            editable: true,
            ...getColumnSearchProps('start_date'),
        },
        {
            title: 'End Date',
            dataIndex: 'end_date',
            key: 'end_date',
            width: '20%',
            editable: true,
            ...getColumnSearchProps('end_date'),
        },
        {
            title: 'Actions',
            dataIndex: 'actions',
            key: 'actions',
            width: '15%',
            render: (_, record) => {
                const editable = isEditing(record);
                return editable ? (
                    <Space>
                        <Button
                            // onClick={() => saveEdit(record.id)}
                            type="primary"
                            size="small"
                            style={{ width: 60 }}
                        >
                            Save
                        </Button>
                        <Popconfirm title="Sure to cancel?" onConfirm={cancel}>
                            <Button
                                type="primary"
                                size="small"
                                style={{ width: 60 }}
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
                                size="small"
                                style={{ width: 40 }}
                                danger
                            />
                        </Popconfirm>
                        <Button
                            disabled={editingKey !== ''} 
                            onClick={() => edit(record)}
                            type="primary"
                            icon={<EditOutlined />}
                            size="small"
                            style={{ width: 40 }}
                        />
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
            inputType: record.key === 'price' ? 'number' : 'text',
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
        <div className="guestsForm">
            <h2>Tour Price list</h2>
            {contextHolder}
            <div className="guestContent">
                <div className="guestList">
                    <Form form={form} component={false}>
                        <Table components={{
                            body: {
                                cell: EditableCell,
                            },
                        }} 
                        rowSelection={rowSelection}
                        bordered columns={mergedColumns} dataSource={[]} pagination={{defaultPageSize: 20}} scroll={{ y: 500}} />
                    </Form>
                </div>
                <div className="guestAddForm">
                    <h2>ADD FORM</h2>
                    <Form {...layout} form={form} name="control-hooks" onFinish={onFinish}>
                        <Form.Item
                            name="name"
                            label="Name"
                            rules={[
                                {
                                    required: true,
                                },
                            ]}
                        >
                            <Input />
                        </Form.Item>
                        <Form.Item
                            name="price"
                            label="Price"
                            rules={[
                                {
                                    required: true,
                                },
                            ]}
                        >
                            <InputNumber style={{ width: 185 }} min="0" />
                        </Form.Item>
                        <Form.Item
                            name="date"
                            label="Date"
                            rules={[
                                {
                                    required: true,
                                },
                            ]}
                        >    
                            <RangePicker />
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

export default TourPrice;
