/* eslint-disable default-case */
import React from 'react';
import { Form, Input, Button, Select, Space } from 'antd';
import './AddForm.css';

const { Option } = Select;
const layout = {
  labelCol: {
    span: 5,
  },
  wrapperCol: {
    span: 16,
  },
};

const tailLayout = {
  wrapperCol: {
    offset: 5,
    span: 16,
  },
};

const AddForm = ({submit, locations, types, prices, characteristics}) => {
    const [form] = Form.useForm();

    const onFinish = (values) => {
        submit(values);
        form.resetFields();
    };
    
      const onReset = () => {
        form.resetFields();
    };

    return (
        <div className="addForm">
            <h2>ADD FORM</h2>
            <Form {...layout} form={form} name="control-hooks" onFinish={onFinish}>
                <Form.Item
                    name="name"
                    label="Name"
                    rules={[
                        {
                            required: true,
                        },
                    ]}
                >
                    <Input />
                </Form.Item>
                <Form.Item
                    name="characteristic"
                    label="Characteristic"
                    rules={[
                        {
                            required: true,
                        },
                    ]}
                >
                    <Select placeholder="Select tour characteristic" allowClear>
                        {
                            characteristics.map(characteristic => {
                                return <Option key={characteristic.id} value={characteristic.id}>{characteristic.name}</Option>
                            })
                        }
                    </Select>
                </Form.Item>
                <Form.Item
                    name="type"
                    label="Type"
                    rules={[
                        {
                            required: true,
                        },
                    ]}
                >
                    <Select placeholder="Select tour type" allowClear>
                        {
                            types.map(type => {
                                return <Option key={type.id} value={type.id}>{type.name}</Option>
                            })
                        }
                    </Select>
                </Form.Item>
                <Form.Item
                    name="price"
                    label="Price"
                    rules={[
                        {
                            required: true,
                        },
                    ]}
                >
                    <Select placeholder="Select tour price" allowClear>
                        {
                            prices.map(price => {
                                return <Option key={price.id} value={price.id}>{price.price}</Option>
                            })
                        }
                    </Select>
                </Form.Item>
                <Form.Item
                    name="location"
                    label="Location"
                    rules={[
                        {
                            required: true,
                        },
                    ]}
                >
                    <Select placeholder="Select tour location" allowClear>
                        {
                            locations.map(location => {
                                if(location.type === "Tourist Area" || location.type === "Tourist")
                                    return <Option key={location.id} value={location.id}>{location.name}</Option>
                            })
                        }
                    </Select>
                </Form.Item>
                {/* <Form.Item
                    noStyle
                    shouldUpdate={(prevValues, currentValues) => prevValues.gender !== currentValues.gender}
                >
                    {({ getFieldValue }) =>
                    getFieldValue('gender') === 'other' ? (
                        <Form.Item
                        name="customizeGender"
                        label="Customize Gender"
                        rules={[
                            {
                            required: true,
                            },
                        ]}
                        >
                        <Input />
                        </Form.Item>
                    ) : null
                    }
                </Form.Item> */}
                <Form.Item {...tailLayout}>
                    <Space>
                        <Button type="primary" htmlType="submit">
                            Submit
                        </Button>
                        <Button htmlType="button" onClick={onReset}>
                            Reset
                        </Button>
                    </Space>
                </Form.Item>
            </Form>
        </div>
    )
}

export default AddForm;
