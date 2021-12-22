import React, {useEffect, useState} from 'react';
import GuestsForm from '../../components/GuestsForm/GuestsForm';
import {useSelector, useDispatch} from 'react-redux';
import { useParams } from 'react-router';
import { getAllCustomer, selectCustomerList, getCustomerByGroup, selectCustomerGroup, addCustomerToGroup, deleteCustomerFromGroup } from '../../features/customer/customerSlice';

const GuestsPage = () => {
    let {id} = useParams();
    const dispatch = useDispatch();
    const customerGroup = useSelector(selectCustomerGroup);
    const customers = useSelector(selectCustomerList);
    const [customerGroupState, setCustomerGroupState] = useState(customerGroup);

    useEffect(() => {
        dispatch(getCustomerByGroup(Number.parseInt(id)));
        dispatch(getAllCustomer());
    }, [dispatch, customerGroupState, id]);

    const handleDeleteCus = async (value) => {
        await dispatch(deleteCustomerFromGroup(value));
        setCustomerGroupState(customerGroup.filter(cus => cus.id !== id));
    };

    const handleSubmitCus = async (newCus) => {
        await dispatch(addCustomerToGroup(newCus));
        setCustomerGroupState(customerGroup.map(() => ([...customerGroup, newCus])));
    };
    
    return (
        <div>
            <GuestsForm customers={customers} customerGroup={customerGroup} remove={handleDeleteCus} submit={handleSubmitCus} />
        </div>
    )
}

export default GuestsPage;
