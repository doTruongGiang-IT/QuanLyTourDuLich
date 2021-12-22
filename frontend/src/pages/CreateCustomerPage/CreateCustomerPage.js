import React from 'react';
import { createCustomer } from '../../features/customer/customerSlice';
import { useDispatch } from 'react-redux';
import { useHistory } from 'react-router';
import CreateCustomerForm from '../../components/CreateCustomerForm/CreateCustomerForm';

const CreateCustomerPage = () => {
    const dispatch = useDispatch();
    const history = useHistory();

    const handleSubmit = async (values) => {
        // console.log(values);
        await dispatch(createCustomer(values));
        history.push("/customer");
    };

    return (
        <CreateCustomerForm submit={handleSubmit} />
    )
}

export default CreateCustomerPage;
