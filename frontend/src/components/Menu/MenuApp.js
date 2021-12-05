import React, {useState} from 'react';
import { Menu } from 'antd';
import { HomeFilled } from '@ant-design/icons';
import { useHistory } from 'react-router';

const { SubMenu } = Menu;

const MenuApp = () => {
    const history = useHistory();
    const [currentKey, setCurrentKey] = useState("");

    const handleClick = e => {
        history.push(`/${e.key}`);
        setCurrentKey(e.key);
    };

    return (
        <Menu onClick={handleClick} selectedKeys={[currentKey]} mode="horizontal" style={{backgroundColor: "whitesmoke", padding: "0 30px"}}>
            <Menu.Item key="" icon={<HomeFilled />}>
                HOME
            </Menu.Item>
            <Menu.Item key="tour_factors">
                TOUR FACTORS
            </Menu.Item>
            <Menu.Item key="customer">
                CUSTOMER
            </Menu.Item>
        </Menu>
    )
}

export default MenuApp;
