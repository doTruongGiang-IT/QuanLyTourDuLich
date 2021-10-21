import React from 'react';
import AddForm from '../../components/AddForm/AddForm';
import { addTour } from '../../features/tour/tourSlice';
import { useDispatch } from 'react-redux';
import { useHistory } from 'react-router';

const AddTourPage = () => {
    const dispatch = useDispatch();
    const history = useHistory();

    const handleSubmit = (values) => {
        dispatch(addTour(values));
        history.push("/");
    };

    return (
        <AddForm submit={handleSubmit} />  
    )
}

export default AddTourPage;
