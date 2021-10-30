/* eslint-disable react-hooks/exhaustive-deps */
import 'antd/dist/antd.css';
import React, {useState} from 'react';
import { Table, Input, Button, Space } from 'antd';
import { SearchOutlined } from '@ant-design/icons';
import './TourDeatilsForm.css';

const TourDetailsForm = ({tourDetails, location}) => {
    let details = [];
    let hotel = "";
    let journey = [];

    tourDetails.forEach(detail => {
      detail.journey.forEach((item) => {
        journey.push(`${new Date(item.start_date).getHours()}h - ${new Date(item.end_date).getHours()}h: ${item.content}.`);
        if(item.location.type === "Hotel") {
          hotel = item.location.name;
        };
      });

      let formatDetail  = {
        id: detail.id,
        name: detail.name,
        startDate: detail.start_date,
        endDate: detail.end_date,
        journey: journey.join(' || '),
        hotel,
        location: location.location
      };
      details.push(formatDetail);
    });
    
    const [searchText, setSearchText] = useState("");
    const [searchedColumn, setSearchedColumn] = useState("");

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
            width: '20%',
            editable: true,
            ...getColumnSearchProps('journey'),
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
        </div>
    )
}

export default TourDetailsForm;
