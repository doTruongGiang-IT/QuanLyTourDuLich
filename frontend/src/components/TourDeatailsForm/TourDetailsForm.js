/* eslint-disable no-unused-expressions */
/* eslint-disable react-hooks/exhaustive-deps */
import 'antd/dist/antd.css';
import React, {useState} from 'react';
import { Table, Input, Button, Space, Modal, Popconfirm, notification, Form, DatePicker } from 'antd';
import { Link } from 'react-router-dom';
import { SearchOutlined, BookOutlined, TeamOutlined, ClockCircleOutlined, DeleteOutlined, EditOutlined } from '@ant-design/icons';
import './TourDeatilsForm.css';
import { useHistory, useParams } from 'react-router';
import EditableCell from '../EditableCell/EditableCell';
import { useDispatch } from 'react-redux';
import { updateGroup } from '../../features/group/groupSlice';
import moment from 'moment';

const TourDetailsForm = ({tourDetails, location, listLocation, remove, update, submit, removeJourney}) => {
    let details = [];
    let hotel = "";
    let journeys = [];
    let nameLocation = "";
    let containers = [];
    let days = [];
    const { RangePicker } = DatePicker;

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
    const [modalInputDisable, setModalInputDisable] = useState(true);
    const [modalInput, setModalInput] = useState("");
    const [modalDate, setModalDate] = useState("");
    const [isEditJourney, setIsEditJourney] = useState(false);
    const [contentJourney, setContentJourney] = useState('');
    let locationId = 0;

    const quickSort = (values) => {
      if (values.length <= 1) {
          return values
      };

      var lessThanPivot = [];
      var greaterThanPivot = [];
      var pivot = values[0];
      for (var i = 1; i < values.length; i++) {
          if (new Date(values[i].start_date) <= new Date(pivot.start_date)) {
              lessThanPivot.push(values[i]);
          } else {
              greaterThanPivot.push(values[i]);
          }
      }
      return quickSort(lessThanPivot).concat(pivot, quickSort(greaterThanPivot));
    };
    // console.log(journey.containers);

    tourDetails.forEach(detail => {
      let journeySort = quickSort(detail.journey);
      if(detail.journey.length > 0) {
        journeySort.forEach((item) => {
          let day = `${new Date(item.start_date).getUTCDate()}-${new Date(item.start_date).getUTCMonth()}-${new Date(item.start_date).getUTCFullYear()}`;
          let content = `${new Date(item.start_date).getUTCHours()}h:${new Date(item.start_date).getUTCMinutes()} - ${new Date(item.end_date).getUTCHours()}h:${new Date(item.end_date).getUTCMinutes()}: ${item.content}.`;
          containers.push({id: detail.id, content_id: item.id, day, content});
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
          locationId = locationItem.id;
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

    journeys.forEach(journey => {
      let temp = [];
      journey.containers.filter(container => {
        if(container.id === journey.id) {
          temp.push(container);
        };
        journey.containers = temp;  
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

    const handleOk = () => {
      setModalInputDisable(false);
    };

    const handleSubmit = () => {
      const journey = {group: isRowActive, content: modalInput, start_date: modalDate[0], end_date: modalDate[1], location: locationId};
      // console.log(journey);
      submit(journey);
      setModalInput("");
      setModalDate("");
      setModalInputDisable(true);
    };

    const onChange = (value, dateString) => {
      // console.log('Selected Time: ', value);
      // console.log('Formatted Selected Time: ', dateString);
      setModalDate(dateString);
    };

    const disabledDate = (current) => {
      // Can not select days before today and today
      let start = "";
      let end = "";
      tourDetails.forEach(detail => {
        if(detail.id === isRowActive) {
          start = detail.start_date;
          end = detail.end_date;
        };
      });
      return (current && current < moment(start).startOf("day")) || (current && current > moment(end).endOf("day"));
    };

    // const handleUpdateJourney = (content) => {
    //   // updateJourney(content)
    //   setIsEditJourney(true);
    //   let contents = content.content.split(': ');
    //   console.log(contents[1]);
    //   let times = contents[0].split(' - ');
    //   console.log(times[0])
    //   console.log(times[1])
    //   console.log(content.day)
    //   setModalInput(contents[1]);
    // };

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
            <Modal title="Journey for this group" visible={isModalVisible} onCancel={handleCancel} footer={[
              <Space>
                <RangePicker defaultValue="" disabledDate={disabledDate} showTime onChange={onChange} disabled={modalInputDisable} />
                <Input value={modalInput} disabled={modalInputDisable} onChange={e => setModalInput(e.target.value)} />
                {
                  (!isEditJourney && modalInputDisable) ?
                  <Button key="submit" type="primary" onClick={handleOk}>
                    Create
                  </Button> :
                  <Button key="submit" type="primary" onClick={handleSubmit}>
                    Submit
                  </Button>
                }
              </Space>
            ]}>
              {
                journeys.map(journey => {
                  return <div key={journey.id}>
                    {
                      days.map((day, index) => {
                        return <div key={index}>
                                  {(journey.id === isRowActive) ? <strong>DAY: {day}</strong> : ""}
                                  {
                                    journey.id === isRowActive ? journey.containers.map((content, index) => {
                                      return content.day === day ? 
                                              <div className="contentJourney" key={index}>
                                                <p><ClockCircleOutlined /> {content.content}</p>
                                                <Button type="primary" size="small" danger onClick={() => removeJourney(content)}><DeleteOutlined /></Button>
                                              </div> : ""
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
