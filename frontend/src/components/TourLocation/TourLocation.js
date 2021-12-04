import React, {useState} from 'react';
import './TourLocation.css';
import { Table, Input, Button, Space, Popconfirm, Form, notification } from 'antd';
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

const TourLocation = ({locationsFactor, update, remove, submit}) => {
    const [searchText, setSearchText] = useState("");
    const [searchedColumn, setSearchedColumn] = useState("");
    const [form] = Form.useForm();
    const [editData, setEditData] = useState([]);
    const [editingKey, setEditingKey] = useState('');
    const [selectedRowKeys, setSelectedKeys] = useState([]);
    const [api, contextHolder] = notification.useNotification();
    const Context = React.createContext();

    let locateFactorList = locationsFactor ? locationsFactor.map((locate, index) => {
        return {key: index, ...locate};
    }) : [];

    const onFinish = (values) => {
        submit(values);
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
          const newData = [...locateFactorList];
          const index = newData.findIndex((item) => id === item.id);
    
          if (index > -1) {
            const item = newData[index];
            newData.splice(index, 1, { ...item, ...row });
            setEditData(newData);
            update(newData[index]);
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

    locateFactorList = quickSort(locateFactorList);

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
            width: '25%',
            editable: true,
            ...getColumnSearchProps('name'),
            sorter: {
              compare: (a, b) => new Date(a.startDate) - new Date(b.startDate),
            //   multiple: tourDetails.length
            },
            sortDirections: ['descend', 'ascend'],
        },
        {
            title: 'Type Location',
            dataIndex: 'type',
            key: 'type',
            width: '20%',
            editable: true,
            ...getColumnSearchProps('type'),
        },
        {
            title: 'Level',
            dataIndex: 'level',
            key: 'level',
            width: '20%',
            editable: true,
            ...getColumnSearchProps('level'),
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
                            onClick={() => saveEdit(record.id)}
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
                                style={{ width: 60 }}
                                danger
                            />
                        </Popconfirm>
                        <Button
                            disabled={editingKey !== ''} 
                            onClick={() => edit(record)}
                            type="primary"
                            icon={<EditOutlined />}
                            size="small"
                            style={{ width: 60 }}
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
        <div className="locationsForm">
            <h2>Tour Location list</h2>
            {contextHolder}
            <div className="locationContent">
                <div className="locationList">
                    <Form form={form} component={false}>
                        <Table components={{
                            body: {
                                cell: EditableCell,
                            },
                        }} 
                        bordered columns={mergedColumns} dataSource={locateFactorList} pagination={{defaultPageSize: 10}} scroll={{ y: 300}} />
                    </Form>
                </div>
                <div className="locationAddForm">
                    <h2>ADD FORM</h2>
                    <Form {...layout} form={form} name="control-hooks" onFinish={onFinish}>
                        <Form.Item
                            className="tourLocationFactorItem"
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
                            className="tourLocationFactorItem"
                            name="type"
                            label="Type"
                            rules={[
                                {
                                    required: true,
                                },
                            ]}
                        >
                            <Input />
                        </Form.Item>
                        <Form.Item
                            className="tourLocationFactorItem"
                            name="level"
                            label="Level"
                            rules={[
                                {
                                    required: true,
                                },
                            ]}
                        >    
                            <Input />
                        </Form.Item>
                        <Form.Item {...tailLayout} className="tourLocationFactorItem">
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

export default TourLocation;
