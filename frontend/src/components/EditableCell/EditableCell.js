import React, {useEffect} from 'react';
import { Input, Form, Select, InputNumber } from 'antd';
import { Option } from 'rc-select';
import { selectTourCharacteristic, selectTourType, getTourCharacteristic, getTourType, getTourPrice, selectTourPrice } from '../../features/tour/tourSlice';
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
    const prices = useSelector(selectTourPrice);

    useEffect(() => {
        dispatch(getTourCharacteristic());
        dispatch(getTourType());
        dispatch(getTourPrice());
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
                    (title !== "ID Type" && title !== "Gender" && title !== "Price") ?
                    <Input /> :
                    <Select placeholder="Please select one" allowClear>
                        {
                            title === "ID Type" ?
                            types.map(type => {
                                return <Option key={type.id} value={type.id}>{type.name}</Option>
                            }) :
                            (
                                title === "Gender" ?
                                <>
                                    <Option value="Male">Male</Option>
                                    <Option value="Female">Female</Option>
                                </> : (
                                    prices.map(price => {
                                        return <Option key={price.id} value={price.id}>{price.price.toLocaleString('it-IT', {style : 'currency', currency : 'VND'})}</Option>
                                    })
                                )
                            )
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

// title === "Characteristic" ?
//                             characteristics.map(characteristic => {
//                                 return <Option key={characteristic.id} value={characteristic.id}>{characteristic.name}</Option>
//                             }):
//                             (
                                
//                             ) 

export default EditableCell;
