import React, {useEffect} from 'react';
import { Input, Form, Select } from 'antd';
import { Option } from 'rc-select';
import { selectTourCharacteristic, selectTourType, getTourCharacteristic, getTourType } from '../../features/tour/tourSlice';
import { useDispatch, useSelector } from 'react-redux';

const EditableCell = ({
    editing,
    dataIndex,
    title,
    inputType,
    record,
    index,
    children,
    ...restProps
}) => {
    
    const dispatch = useDispatch();
    const characteristics = useSelector(selectTourCharacteristic);
    const types = useSelector(selectTourType);

    useEffect(() => {
        dispatch(getTourCharacteristic());
        dispatch(getTourType());
    }, [dispatch]);

    return (
        <td {...restProps}>
            {editing ? (
                <Form.Item
                name={dataIndex}
                style={{
                    margin: 0,
                }}
                rules={[
                    {
                    required: true,
                    message: `Please Input ${title}!`,
                    },
                ]}
                >
                {
                    title === "Name" ?
                    <Input /> :
                    <Select placeholder="Please select one" allowClear>
                        {
                            title === "Characteristic" ?
                            characteristics.map(characteristic => {
                                return <Option key={characteristic.id} value={characteristic.id}>{characteristic.name}</Option>
                            }):
                            types.map(type => {
                                return <Option key={type.id} value={type.id}>{type.name}</Option>
                            })
                        }
                    </Select>
                }
                </Form.Item>
            ) : (
                children
            )}
        </td>
    )
}

export default EditableCell;
