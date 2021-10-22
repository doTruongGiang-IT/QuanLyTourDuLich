/* eslint-disable react-hooks/exhaustive-deps */
import 'antd/dist/antd.css';
import React, {useState} from 'react';
import { Table, Input, Button, Space } from 'antd';
import { SearchOutlined } from '@ant-design/icons';
import './TourDeatilsForm.css';

const TourDetailsForm = () => {
    let data = [
        {
            key: '1',
            id: 0,
            startDate: '12/10/1998',
            endDate: '25/10/1998',
            journey: 'journey',
            hotel: 'hotel',
            location: 'location'
        },
        {
            key: '2',
            id: 1,
            startDate: '11/05/2000',
            endDate: '18/05/2000',
            journey: 'journey',
            hotel: 'hotel',
            location: 'location'
        },
        {
            key: '3',
            id: 2,
            startDate: '06/09/2013',
            endDate: '16/09/2013',
            journey: 'journey',
            hotel: 'hotel',
            location: 'location'
        },
        {
            key: '4',
            id: 3,
            startDate: '23/11/2018',
            endDate: '28/11/2018',
            journey: 'journey',
            hotel: 'hotel',
            location: 'location'
        },
        {
            key: '5',
            id: 4,
            startDate: '13/03/1999',
            endDate: '18/03/1999',
            journey: 'journey',
            hotel: 'hotel',
            location: 'location'
        }
    ];

    const [searchText, setSearchText] = useState("");
    const [searchedColumn, setSearchedColumn] = useState("");
    const [dataInfo, setDataInfo] = useState(data);

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
          sorter: (a, b) => new Date(a.startDate) - new Date(b.startDate),
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
            <Table bordered columns={columns} dataSource={dataInfo} />
        </div>
    )
}

export default TourDetailsForm;
