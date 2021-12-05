import React from 'react';
import { Input, Form, InputNumber } from 'antd';

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
                    (title !== "Price") ?
                    <Input /> :
                    <InputNumber style={{width: "150px"}} min="0" />
                }
                </Form.Item>
            ) : (
                children
            )}
        </td>
    )
}

export default EditableCellForPriceList;
