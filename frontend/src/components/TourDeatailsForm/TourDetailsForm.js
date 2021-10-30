/* eslint-disable no-unused-expressions */
/* eslint-disable react-hooks/exhaustive-deps */
import 'antd/dist/antd.css';
import React, {useState} from 'react';
import { Table, Input, Button, Space, Modal } from 'antd';
import { SearchOutlined, BookOutlined } from '@ant-design/icons';
import './TourDeatilsForm.css';

const TourDetailsForm = ({tourDetails, location, listLocation}) => {
    let details = [];
    let hotel = "";
    let journeys = [];
    let nameLocation = "";
    let contents = [];

    tourDetails.forEach(detail => {
      if(detail.journey.length > 0) {
        detail.journey.forEach((item) => {
          contents.push(`${new Date(item.start_date).getHours()}h - ${new Date(item.end_date).getHours()}h: ${item.content}.`);
          if(item.location.type === "Hotel") {
            hotel = item.location.name;
          };
        });
        journeys.push({id: detail.id, contents});
      }else {
        journeys.push({id: detail.id, contents: []});
      };

      listLocation.forEach(locationItem => {
        if(locationItem.id === location.location) {
          nameLocation = locationItem.name;
        };
      });

      let formatDetail  = {
        id: detail.id,
        name: detail.name,
        startDate: detail.start_date,
        endDate: detail.end_date,
        // journey: detail.journey.length > 0 ? journey.join(' || ') : "",
        hotel,
        location: nameLocation
      };
      details.push(formatDetail);
      details = details.map((detail) => {
        return {key: detail.id + 1, ...detail};
      });
    });
    
    const [searchText, setSearchText] = useState("");
    const [searchedColumn, setSearchedColumn] = useState("");
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [isRowActive, setIsRowActive] = useState(0);

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

    const columns = [
        {
            title: 'ID Tourist Group',
            dataIndex: 'id',
            key: 'id',
            width: '10%',
            editable: true,
            ...getColumnSearchProps('id'),
        },
        {
            title: 'StartDate',
            dataIndex: 'startDate',
            key: 'startDate',
            width: '20%',
            editable: true,
            ...getColumnSearchProps('startDate'),
            sorter: {
              compare: (a, b) => new Date(a.startDate) - new Date(b.startDate),
              multiple: tourDetails.length
            },
            ellipsis: true,
            sortDirections: ['descend', 'ascend'],
        },
        {
            title: 'EndDate',
            dataIndex: 'endDate',
            key: 'endDate',
            width: '20%',
            editable: true,
            ...getColumnSearchProps('endDate'),
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
            editable: true,
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
            width: '10%',
            editable: true,
            ...getColumnSearchProps('hotel'),
        },
        {
            title: 'Location',
            dataIndex: 'location',
            key: 'location',
            width: '20%',
            editable: true,
            ...getColumnSearchProps('location'),
        },
    ];

    return (
        <div className="tourDetailsForm">
            <h2>Details for this tour</h2>
            <Table bordered columns={columns} dataSource={details} />
            <Modal title="Journey for this group" visible={isModalVisible} onCancel={handleCancel} footer={[]}>
              {
                journeys.map(journey => {
                  return <p key={journey.id}>
                    {
                      journey.id === isRowActive ? journey.contents.map((content, index) => {
                        return <p key={index}>{content}</p>
                      }) : ""
                    }
                  </p>
                })
              }
            </Modal>
        </div>
    )
}

export default TourDetailsForm;
