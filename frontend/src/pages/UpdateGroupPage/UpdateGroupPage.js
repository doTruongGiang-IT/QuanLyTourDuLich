import React, {useEffect} from 'react';
import UpdateGroupForm from '../../components/UpdateGroupForm/UpdateGroupForm';
import { useDispatch, useSelector } from 'react-redux';
import { useHistory, useParams } from 'react-router';
import { updateGroup, selectGroup, getGroup } from '../../features/group/groupSlice';

const UpdateGroupPage = () => {
    const {id} = useParams();
    const dispatch = useDispatch();
    const group = useSelector(selectGroup);
    const history = useHistory();

    useEffect(() => {
        dispatch(getGroup(Number.parseInt(id)));
    }, [dispatch, id]);

    const handleSubmit = async (values, sdate, edate) => {
        const group = {name: values.name, id: Number.parseInt(id), start_date: sdate, end_date: edate};
        await dispatch(updateGroup(group));
        history.goBack();
    };

    return (
        <UpdateGroupForm group={group} submit={handleSubmit} />
    )
};

export default UpdateGroupPage;
