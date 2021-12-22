/* eslint-disable default-case */
import React, {useState} from 'react';
import { Form, Input, Button, Space, DatePicker } from 'antd';
import './AddGroupForm.css';
import moment from 'moment';

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

const { RangePicker } = DatePicker;

const AddGroupForm = ({submit}) => {
    const [form] = Form.useForm();
    let count = 0;
    let start = ""; 
    let end = "";

    const onFinish = (values) => {
        submit(values, start, end);
        form.resetFields();
    };
    
      const onReset = () => {
        form.resetFields();
    };

    const handleDate = (date) => {
        if(count === 0) {
            start = date;
            count++;
        }else {
            end = date;
        };
    };

    return (
        <div className="addGroupForm">
            <h2>CREATE GROUP FORM</h2>
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
                    name="date"
                    label="Date"
                    rules={[
                        {
                            required: true,
                        },
                    ]}
                >    
                    <RangePicker format="YYYY-MM-DD" value={[moment('', 'YYYY-MM-DD'), moment('', 'YYYY-MM-DD')]} onBlur={e => handleDate(e.target.value)} />
                </Form.Item>
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

export default AddGroupForm;
