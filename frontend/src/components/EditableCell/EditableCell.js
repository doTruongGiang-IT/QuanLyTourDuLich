import React from 'react';
import { Input, InputNumber, Form } from 'antd';

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
    const inputNode = inputType === 'number' ? <InputNumber /> : <Input />;

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
                {inputNode}
                </Form.Item>
            ) : (
                children
            )}
        </td>
    )
}

export default EditableCell;
