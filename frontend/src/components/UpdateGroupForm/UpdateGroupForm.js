/* eslint-disable default-case */
import React, {useEffect, useState} from 'react';
import { Form, Input, Button, Space, DatePicker } from 'antd';
import '../AddGroupForm/AddGroupForm.css';
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

const UpdateGroupForm = ({submit, group}) => {
    const [name, setName] = useState("");
    const [startDate, setStartDate] = useState(new Date());
    const [endDate, setEndDate] = useState(new Date());
    const [form] = Form.useForm();
    let count = 0;
    let start = ""; 
    let end = "";

    useEffect(() => {
        setName(group.name);
        setStartDate(group.start_date);
        setEndDate(group.end_date);
    }, [group.name, group.start_date, group.end_date]);

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
            <h2>EDIT GROUP FORM</h2>
            <Form {...layout} form={form} name="control-hooks" onFinish={onFinish}>
                <Form.Item
                    name="name"
                    label="Name"
                    initialValue={`${name}`}
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
                    initialValue={[moment(startDate, 'YYYY-MM-DD'), moment(endDate, 'YYYY-MM-DD')]}
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

export default UpdateGroupForm;
