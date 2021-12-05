import React, {useState} from 'react';
import '../GuestsForm/GuestsForm.css';
import { Table, Input, Button, Space, Popconfirm, Form, notification, DatePicker, InputNumber } from 'antd';
import { SearchOutlined, DeleteOutlined, EditOutlined } from '@ant-design/icons';
import moment from 'moment';
import EditableCellForPriceList from '../EditableCellForPriceList/EditableCellForPriceList';

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

const TourPrice = ({priceFactor, submit, update, remove}) => {
    const [searchText, setSearchText] = useState("");
    const [searchedColumn, setSearchedColumn] = useState("");
    const [form] = Form.useForm();
    const [editData, setEditData] = useState([]);
    const [editingKey, setEditingKey] = useState('');
    const [api, contextHolder] = notification.useNotification();
    const Context = React.createContext();
    let count = 0;
    let start = new Date(); 
    let end = new Date();

    let priceFactorList = priceFactor ? priceFactor.map((price, index) => {
        return {key: index, id: price.id, name: price.name, price: price.price.toLocaleString('it-IT', {style : 'currency', currency : 'VND'}), start_date: price.start_date, end_date: price.end_date};
    }) : [];
    
    const handleDate = (date) => {
        if(count === 0) {
            start = date;
            count++;
        }else {
            end = date;
        };
    };

    const onFinish = (values) => {
        submit({name: values.name, price: values.price, start_date: start, end_date: end});
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

    const formatData = (editPrice) => {
        delete editPrice.date;
        delete editPrice.key;
        if(typeof editPrice.price === "string") {
            editPrice.price = editPrice.price.slice(0, editPrice.price.length-4);
            editPrice.price = editPrice.price.replaceAll('.', '');  
            editPrice.price = Number.parseInt(editPrice.price);
        };
        return editPrice;
    };

    const saveEdit = async (id) => {
        try {
          const row = await form.validateFields();
          const newData = [...priceFactorList];
          const index = newData.findIndex((item) => id === item.id);
    
          if (index > -1) {
            const item = newData[index];
            newData.splice(index, 1, { ...item, ...row });
            setEditData(newData);
            const editPrice = formatData(newData[index]);
            update(editPrice);
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

    priceFactorList = quickSort(priceFactorList);

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
                                cell: EditableCellForPriceList,
                            },
                        }} 
                        bordered columns={mergedColumns} dataSource={priceFactorList} pagination={{defaultPageSize: 10}} scroll={{ y: 230}} />
                    </Form>
                </div>
                <div className="guestAddForm">
                    <h2>ADD FORM</h2>
                    <Form {...layout} form={form} name="control-hooks" onFinish={onFinish}>
                        <Form.Item
                            name="name"
                            label="Name"
                            initialValue=""
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
                            initialValue=""
                            rules={[
                                {
                                    required: true,
                                },
                            ]}
                        >
                            <InputNumber style={{ width: 165 }} min="0" />
                        </Form.Item>
                        <Form.Item
                            name="date"
                            label="Date"
                            initialValue={[moment(start, 'YYYY-MM-DD'), moment(end, 'YYYY-MM-DD')]}
                            rules={[
                                {
                                    required: true,
                                },
                            ]}
                        >    
                            <RangePicker format="YYYY-MM-DD" value={[moment('', 'YYYY-MM-DD'), moment('', 'YYYY-MM-DD')]} onBlur={e => handleDate(e.target.value)} />
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
