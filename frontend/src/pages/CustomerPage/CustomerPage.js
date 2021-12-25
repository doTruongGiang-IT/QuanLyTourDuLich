import React, {useEffect, useState} from 'react';
import CustomerListForm from '../../components/CustomerListForm/CustomerListForm';
import {useSelector, useDispatch} from 'react-redux';
import { getAllCustomer, selectCustomerList, updateCustomer, deleteCustomer, getCustomer, selectCustomer } from '../../features/customer/customerSlice';

const CustomerPage = () => {
    const dispatch = useDispatch();
    const customers = useSelector(selectCustomerList);
    const customer = useSelector(selectCustomer);
    const [customerListState, setCustomerListState] = useState(customers);

    useEffect(() => {
        dispatch(getAllCustomer());
    }, [dispatch, customerListState]);

    const handleDelete = async (id) => {
        await dispatch(deleteCustomer(id));
        setCustomerListState(customers.filter(customer => customer.id !== id));
    };

    const saveEdit = async (editCustomer) => {
        await dispatch(updateCustomer(editCustomer));
        customers.forEach(customer => {
            if(customer.id === editCustomer.id) {
                customer = {...customer, ...editCustomer};
            };
        });
        setCustomerListState(customers);
    };

    const handleDetails = (id) => {
        dispatch(getCustomer(id));
    };

    return (
        <CustomerListForm customers={customers} remove={handleDelete} update={saveEdit} />
    )
}

export default CustomerPage;
