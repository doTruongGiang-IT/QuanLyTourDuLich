import React, {useEffect} from 'react';
import { Input, Form, InputNumber, Select } from 'antd';
import { useDispatch, useSelector } from 'react-redux';
import { selectCostTypes, getCostTypes } from '../../features/groupCost/groupCostSlice';
const { Option } = Select;
const EditableCellForPriceList = ({
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
    const types = useSelector(selectCostTypes);

    useEffect(() => {
        dispatch(getCostTypes());
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
                    (title === "Price") ?
                    <InputNumber style={{width: "150px"}} min="0" /> :
                    (
                        title === "Cost Type" ?
                        <Select>
                            {
                                types ?
                                types.map((type, index) => {
                                    return <Option key={index} value={type.id}>{type.name}</Option>
                                }) : null
                            }
                        </Select>:
                        <Input />
                    )
                    
                }
                </Form.Item>
            ) : (
                children
            )}
        </td>
    )
}

export default EditableCellForPriceList;
