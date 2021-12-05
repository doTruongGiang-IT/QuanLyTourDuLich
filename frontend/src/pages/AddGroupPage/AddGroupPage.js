import React from 'react';
import AddGroupForm from '../../components/AddGroupForm/AddGroupForm';
import { useDispatch } from 'react-redux';
import { useHistory, useParams } from 'react-router';
import { createGroup } from '../../features/group/groupSlice';

const AddGroupPage = () => {
    const {id} = useParams();
    const dispatch = useDispatch();
    const history = useHistory();

    const handleSubmit = async (values, sdate, edate) => {
        const group = {name: values.name, tour: Number.parseInt(id), start_date: sdate, end_date: edate};
        await dispatch(createGroup(group));
        history.push(`/details/${id}`);
    };

    return (
        <AddGroupForm submit={handleSubmit} />
    )
}

export default AddGroupPage;
