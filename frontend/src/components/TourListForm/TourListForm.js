/* eslint-disable react-hooks/exhaustive-deps */
import 'antd/dist/antd.css';
import React, {useState} from 'react';
import { Table, Input, Button, Space, Popconfirm, Form, notification} from 'antd';
import { SearchOutlined, DeleteOutlined, EditOutlined } from '@ant-design/icons';
import EditableCell from '../EditableCell/EditableCell';
import "./TourListForm.css";
import { Link } from 'react-router-dom';
import { useHistory } from 'react-router';

const TourListForm = ({remove, update}) => {
    let data = [
        {
            key: '1',
            id: 0,
            name: 'John Brown',
            characteristic: 'Expensive',
            type: 1
        },
        {
            key: '2',
            id: 1,
            name: 'John Brown',
            characteristic: 'Expensive',
            type: 1
        },
        {
            key: '3',
            id: 2,
            name: 'John Brown',
            characteristic: 'Expensive',
            type: 1
        },
        {
            key: '4',
            id: 3,
            name: 'John Brown',
            characteristic: 'Expensive',
            type: 1
        },
        {
            key: '5',
            id: 4,
            name: 'John Brown',
            characteristic: 'Expensive',
            type: 1
        },
        {
            key: '6',
            id: 5,
            name: 'John Brown',
            characteristic: 'Expensive',
            type: 1
        },
        {
            key: '7',
            id: 6,
            name: 'John Brown',
            characteristic: 'Expensive',
            type: 1
        },
        {
            key: '8',
            id: 7,
            name: 'John Brown',
            characteristic: 'Expensive',
            type: 1
        },
        {
            key: '9',
            id: 8,
            name: 'John Brown',
            characteristic: 'Expensive',
            type: 1
        },
        {
            key: '10',
            id: 9,
            name: 'John Brown',
            characteristic: 'Expensive',
            type: 1
        },
        {
            key: '11',
            id: 10,
            name: 'John Brown',
            characteristic: 'Expensive',
            type: 1
        },
        {
            key: '12',
            id: 11,
            name: 'John Brown',
            characteristic: 'Expensive',
            type: 1
        },
    ];
    
    const [searchText, setSearchText] = useState("");
    const [searchedColumn, setSearchedColumn] = useState("");
    const [dataInfo, setDataInfo] = useState(data);
    const [form] = Form.useForm();
    const [editData, setEditData] = useState([]);
    const [editingKey, setEditingKey] = useState('');
    const [api, contextHolder] = notification.useNotification();
    const Context = React.createContext();
    const history = useHistory();

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

    const handleDelete = (key) => {
        // setDataInfo(data.filter((item) => item.key !== key));
        remove(key);
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

    const saveEdit = async (key) => {
        try {
          const row = await form.validateFields();
          const newData = [...dataInfo];
          const index = newData.findIndex((item) => key === item.key);
    
          if (index > -1) {
            const item = newData[index];
            newData.splice(index, 1, { ...item, ...row });
            // setEditData(newData);
            update(newData[index]);
            setDataInfo(newData);
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

    const columns = [
        {
          title: 'ID',
          dataIndex: 'id',
          key: 'id',
          width: '10%',
          editable: true,
          ...getColumnSearchProps('id'),
        },
        {
          title: 'Name',
          dataIndex: 'name',
          key: 'name',
          width: '30%',
          editable: true,
          ...getColumnSearchProps('name'),
          sorter: (a, b) => a.name.length - b.name.length,
          sortDirections: ['descend', 'ascend'],
        },
        {
            title: 'Characteristic',
            dataIndex: 'characteristic',
            key: 'characteristic',
            editable: true,
            ...getColumnSearchProps('characteristic'),
        },
        {
            title: 'ID Type',
            dataIndex: 'type',
            key: 'type',
            width: '10%',
            editable: true,
            ...getColumnSearchProps('type'),
        },
        {
            title: 'Actions',
            width: '10%',
            render: (_, record) => {
                const editable = isEditing(record);
                return editable ? (
                    <Space>
                        <Button
                            onClick={() => saveEdit(record.key)}
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
                        <Popconfirm title="Sure to delete?" onConfirm={() => handleDelete(record.key)}>
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
            inputType: col.dataIndex === 'type' ? 'number' : 'text',
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
        <div className="tourListForm">
            {contextHolder}
            <Link id="addTour" to="/add">Add Tour</Link>
            <Form form={form} component={false}>
                <Table components={{
                    body: {
                        cell: EditableCell,
                    },
                }} onRow={(record, rowIndex) => {
                    return {
                        onClick: event => history.push(`/details/${record.id}`),
                    };
                }} bordered columns={mergedColumns} dataSource={dataInfo} />
            </Form>
        </div>
    )
}

export default TourListForm;
