import React, {useState} from 'react';
import '../TourCharacteristic/TourCharacteristic.css';
import { Table, Input, Button, Space, Popconfirm, Form, notification, Select} from 'antd';
import { SearchOutlined, DeleteOutlined, EditOutlined } from '@ant-design/icons';
import EditableCell from '../EditableCell/EditableCell';

const layout = {
    labelCol: {
      span: 8,
    },
    wrapperCol: {
      span: 14,
    },
};
  
  const tailLayout = {
    wrapperCol: {
      offset: 3,
      span: 14,
    },
};

const TourType = ({typeFactor, update, remove, submit}) => {
    const [searchText, setSearchText] = useState("");
    const [searchedColumn, setSearchedColumn] = useState("");
    const [form] = Form.useForm();
    const [editData, setEditData] = useState([]);
    const [editingKey, setEditingKey] = useState('');
    const [selectedRowKeys, setSelectedKeys] = useState([]);
    const [api, contextHolder] = notification.useNotification();
    const Context = React.createContext();

    let typeFactorList = typeFactor ? typeFactor.map((type, index) => {
        return {key: index, ...type};
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
          const newData = [...typeFactorList];
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

    typeFactorList = quickSort(typeFactorList);

    const columns = [
        {
            title: 'ID',
            dataIndex: 'id',
            key: 'id',
            width: '15%',
            ...getColumnSearchProps('id'),
        },
        {
            title: 'Name',
            dataIndex: 'name',
            key: 'name',
            // width: '20%',
            editable: true,
            ...getColumnSearchProps('name'),
            sorter: {
              compare: (a, b) => new Date(a.startDate) - new Date(b.startDate),
            //   multiple: tourDetails.length
            },
            sortDirections: ['descend', 'ascend'],
        },
        {
            title: 'Actions',
            dataIndex: 'actions',
            key: 'actions',
            width: '25%',
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
        <div className="typeForm">
            <h2>Tour Type list</h2>
            {contextHolder}
            <div className="characteristicContent">
                <div className="characteristicList">
                    <Form form={form} component={false}>
                        <Table components={{
                            body: {
                                cell: EditableCell,
                            },
                        }} 
                        bordered columns={mergedColumns} dataSource={typeFactorList} pagination={{defaultPageSize: 20}} scroll={{ y: 200 }} />
                    </Form>
                </div>
                <div className="characteristicAddForm">
                    <h2>ADD FORM</h2>
                    <Form {...layout} form={form} name="control-hooks" onFinish={onFinish}>
                        <Form.Item
                            className="tourCharacteristicFactorItem"
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
                        <Form.Item {...tailLayout} className="tourCharacteristicFactorItem">
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

export default TourType;
