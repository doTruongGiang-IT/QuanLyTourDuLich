/* eslint-disable no-unused-expressions */
/* eslint-disable react-hooks/exhaustive-deps */
import 'antd/dist/antd.css';
import React, {useState} from 'react';
import { Table, Input, Button, Space, Modal, Popconfirm, notification, Form } from 'antd';
import { Link } from 'react-router-dom';
import { SearchOutlined, BookOutlined, TeamOutlined, ClockCircleOutlined, DeleteOutlined, EditOutlined } from '@ant-design/icons';
import './TourDeatilsForm.css';
import { useHistory, useParams } from 'react-router';
import EditableCell from '../EditableCell/EditableCell';
import { useDispatch } from 'react-redux';
import { updateGroup } from '../../features/group/groupSlice';

const TourDetailsForm = ({tourDetails, location, listLocation, remove, update}) => {
    let details = [];
    let hotel = "";
    let journeys = [];
    let nameLocation = "";
    let containers = [];
    let days = [];

    const dispatch = useDispatch();
    const [searchText, setSearchText] = useState("");
    const [searchedColumn, setSearchedColumn] = useState("");
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [isRowActive, setIsRowActive] = useState(0);
    const history = useHistory();
    const [api, contextHolder] = notification.useNotification();
    const Context = React.createContext();
    let {id} = useParams();
    const [editData, setEditData] = useState([]);
    const [editingKey, setEditingKey] = useState('');
    const [form] = Form.useForm();

    tourDetails.forEach(detail => {
      if(detail.journey.length > 0) {
        detail.journey.forEach((item) => {
          let day = `${new Date(item.start_date).getUTCDate()}-${new Date(item.start_date).getUTCMonth()}-${new Date(item.start_date).getUTCFullYear()}`;
          let content = `${new Date(item.start_date).getUTCHours()}h:${new Date(item.start_date).getUTCMinutes()} - ${new Date(item.end_date).getUTCHours()}h:${new Date(item.end_date).getUTCMinutes()}: ${item.content}.`;
          containers.push({day, content});
          if(!days.includes(day)) {
            days.push(day);
          };
          
          if(item.location.type === "Hotel") {
            hotel = item.location.name;
          };
        });
        journeys.push({id: detail.id, containers});
      }else {
        journeys.push({id: detail.id, containers: []});
      };

      listLocation.forEach(locationItem => {
        if(locationItem.id === location.location) {
          nameLocation = locationItem.name;
        };
      });

      let formatDetail  = {
        id: detail.id,
        name: detail.name,
        start_date: detail.start_date,
        end_date: detail.end_date,
        // journey: detail.journey.length > 0 ? journey.join(' || ') : "",
        hotel,
        location: nameLocation
      };
      details.push(formatDetail);
      details = details.map((detail) => {
        return {key: detail.id + 1, ...detail};
      });
    });

    const showModal = (id) => {
      setIsRowActive(id);
      setIsModalVisible(true);
    };

    const handleCancel = () => {
      setIsModalVisible(false);
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
          const newData = [...tourDetails];
          const index = newData.findIndex((item) => id === item.id);
    
          if (index > -1) {
            const item = newData[index];
            newData.splice(index, 1, { ...item, ...row });
            setEditData(newData);
            update(newData[index]);
            // console.log(newData[index]);
            // dispatch(updateGroup(newData[index]));
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

    const columns = [
        {
            title: 'ID Tourist Group',
            dataIndex: 'id',
            key: 'id',
            width: '10%',
            ...getColumnSearchProps('id'),
        },
        {
            title: 'Group Name',
            dataIndex: 'name',
            key: 'name',
            width: '15%',
            editable: true,
            ...getColumnSearchProps('name'),
        },
        {
            title: 'StartDate',
            dataIndex: 'start_date',
            key: 'start_date',
            width: '10%',
            editable: true,
            ...getColumnSearchProps('start_date'),
            sorter: {
              compare: (a, b) => new Date(a.startDate) - new Date(b.startDate),
              multiple: tourDetails.length
            },
            ellipsis: true,
            sortDirections: ['descend', 'ascend'],
        },
        {
            title: 'EndDate',
            dataIndex: 'end_date',
            key: 'end_date',
            width: '10%',
            editable: true,
            ...getColumnSearchProps('end_date'),
            sorter: {
              compare: (a, b) => new Date(a.startDate) - new Date(b.startDate),
              multiple: tourDetails.length
            },
            ellipsis: true,
            sortDirections: ['descend', 'ascend'],
        },
        {
            title: 'Journey',
            dataIndex: 'journey',
            key: 'journey',
            width: '10%',
            render: (_, record) => {
              return(
                <Button
                    onClick={() => showModal(record.id)}
                    type="primary"
                    icon={<BookOutlined />}
                    size="medium"
                    style={{ width: 100 }}
                />
              )
            }
        },
        {
            title: 'Hotel',
            dataIndex: 'hotel',
            key: 'hotel',
            width: '15%',
            ...getColumnSearchProps('hotel'),
        },
        {
            title: 'Location',
            dataIndex: 'location',
            key: 'location',
            width: '10%',
            ...getColumnSearchProps('location'),
        },
        {
            title: 'Actions',
            dataIndex: 'actions',
            key: 'actions',
            // width: '10%',
            render: (_, record) => {
              const editable = isEditing(record);
              return editable ? (
                <Space>
                    <Button
                        onClick={() => saveEdit(record.id)}
                        type="primary"
                        size="medium"
                        style={{ width: 100 }}
                    >
                        Save
                    </Button>
                    <Popconfirm title="Sure to cancel?" onConfirm={cancel}>
                        <Button
                            type="primary"
                            size="medium"
                            style={{ width: 100 }}
                            danger
                        >
                            Cancel
                        </Button>
                    </Popconfirm>
                </Space> 
            ) : (
                <Space>
                    <Button
                      onClick={() => history.push(`/guests/${record.id}`)}
                      type="primary"
                      icon={<TeamOutlined />}
                      size="medium"
                      style={{ width: 80 }}
                    />
                    <Popconfirm title="Sure to delete?" onConfirm={() => handleDelete(record.id)}>
                      <Button
                          type="primary"
                          icon={<DeleteOutlined />}
                          size="medium"
                          style={{ width: 80 }}
                          danger
                      />
                    </Popconfirm>
                    <Button
                        // onClick={() => history.push(`/update/groupTour/${record.id}`)}
                        onClick={() => edit(record)}
                        type="primary"
                        icon={<EditOutlined />}
                        size="medium"
                        style={{ width: 80 }}
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
        <div className="tourDetailsForm">
            {contextHolder}
            <Link id="addTour" to={`/add/groupTour/${id}`}>Add Group</Link>
            <h2>Details for this tour</h2>
            <Form form={form} component={false}>
              <Table 
                components={{
                    body: {
                        cell: EditableCell,
                    },
                }} 
                bordered columns={mergedColumns} dataSource={details} 
              />
            </Form>
            <Modal title="Journey for this group" visible={isModalVisible} onCancel={handleCancel} footer={[]}>
              {
                journeys.map(journey => {
                  return <div key={journey.id}>
                    {
                      days.map((day, index) => {
                        return <div key={index}>
                                  {(journey.id === isRowActive && journey.containers.length > 0) ? <strong>DAY: {day}</strong> : ""}
                                  {
                                    journey.id === isRowActive ? journey.containers.map((content, index) => {
                                      return content.day === day ? <div key={index}><p><ClockCircleOutlined /> {content.content}</p></div> : ""
                                    }) : ""
                                  }
                              </div>
                      })
                    }
                  </div>
                })
              }
            </Modal>
        </div>
    )
}

export default TourDetailsForm;
