/* eslint-disable react-hooks/exhaustive-deps */
import 'antd/dist/antd.css';
import React, {useState} from 'react';
import { Table, Input, Button, Space, Popconfirm, Form, notification, Modal} from 'antd';
import { SearchOutlined, DeleteOutlined, EditOutlined, EyeOutlined, BookOutlined } from '@ant-design/icons';
import EditableCell from '../EditableCell/EditableCell';
import "./TourListForm.css";
import { Link } from 'react-router-dom';
import { useHistory } from 'react-router';

const TourListForm = ({remove, update, tours, setDetails, tourDetails}) => {
    let formatLocations = [];
    let tourList = tours ? tours.map((tour) => {
        return {key: tour.id + 1, id: tour.id, name: tour.name, description: tour.description, price: tour.price.toLocaleString('it-IT', {style : 'currency', currency : 'VND'}), type: tour.type};
    }) : [];

    let locations = tourDetails.length > 0 ? tourDetails[0].journey.map(location => {
        if(location.location.type !== "Hotel") {
            return location.location.name;
        };
    }) : [];

    locations.forEach(location => {
        if(location !== undefined && !formatLocations.includes(location)) {
            formatLocations.push(location);
        }
    });

    const [searchText, setSearchText] = useState("");
    const [searchedColumn, setSearchedColumn] = useState("");
    const [form] = Form.useForm();
    const [editData, setEditData] = useState([]);
    const [editingKey, setEditingKey] = useState('');
    const [selectedRowKeys, setSelectedKeys] = useState([]);
    const [tourLocations, setTourLocations] = useState("");
    const [api, contextHolder] = notification.useNotification();
    const Context = React.createContext();
    const history = useHistory();
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [isRowActive, setIsRowActive] = useState(0);

    const showModal = async (id) => {
        await setDetails(id);
        setIsRowActive(id);
        setIsModalVisible(true);
    };

    const handleCancel = () => {
        setIsModalVisible(false);
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
          const newData = [...tourList];
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

    tourList = quickSort(tourList);

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
            title: 'Characteristic',
            dataIndex: 'description',
            key: 'description',
            width: '30%',
            editable: true,
            ...getColumnSearchProps('description'),
        },
        {
            title: 'Price',
            dataIndex: 'price',
            key: 'price',
            width: '10%',
            editable: true,
            ...getColumnSearchProps('price'),
        },
        {
            title: 'ID Type',
            dataIndex: 'type',
            key: 'type',
            width: '15%',
            editable: true,
            ...getColumnSearchProps('type'),
        },
        {
            title: 'Actions',
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
                        <Button
                            disabled={editingKey !== ''} 
                            onClick={() => history.push(`/details/${record.id}`)}
                            type="primary"
                            icon={<EyeOutlined />}
                            size="small"
                            style={{ width: 40 }}
                        />
                        <Button
                            onClick={() => showModal(record.id)}
                            type="primary"
                            icon={<BookOutlined />}
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
        <div className="tourListForm">
            {contextHolder}
            <Link id="addTour" to="/add">Add Tour</Link>
            <Form form={form} component={false}>
                <Table components={{
                    body: {
                        cell: EditableCell,
                    },
                }} 
                // onRow={(record, rowIndex) => {
                //     return {
                //         onClick: event => history.push(`/?tour_id=${record.id}`),
                //     };
                // }}
                rowSelection={rowSelection}
                bordered columns={mergedColumns} dataSource={tourList} pagination={{defaultPageSize: 20}} scroll={{ y: 500, x: "max-content" }} />
            </Form>
            <Modal title="Locations for this tour" visible={isModalVisible} onCancel={handleCancel} footer={[]}>
              {
                formatLocations.map((location, index) => {
                    return <p key={index}>{index + 1}: {location}</p>;
                })
              }
            </Modal>
        </div>
    )
}

export default TourListForm;
