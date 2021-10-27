import React, {useEffect} from 'react';
import AddForm from '../../components/AddForm/AddForm';
import { addTour, 
    selectTourCharacteristic, 
    selectListLocation, 
    selectTourType, 
    selectTourPrice, 
    getTourCharacteristic,
    getListLocation,
    getTourPrice,
    getTourType
 } from '../../features/tour/tourSlice';
import { useDispatch, useSelector } from 'react-redux';
import { useHistory } from 'react-router';

const AddTourPage = () => {
    const dispatch = useDispatch();
    const history = useHistory();
    const characteristics = useSelector(selectTourCharacteristic);
    const locations = useSelector(selectListLocation);
    const types = useSelector(selectTourType);
    const prices = useSelector(selectTourPrice);

    useEffect(() => {
        dispatch(getTourCharacteristic());
        dispatch(getListLocation());
        dispatch(getTourType());
        dispatch(getTourPrice());
    }, [dispatch]);

    const handleSubmit = async (values) => {
        await dispatch(addTour(values));
        history.push("/");
    };

    return (
        <AddForm submit={handleSubmit} characteristics={characteristics} locations={locations} types={types} prices={prices} />  
    )
}

export default AddTourPage;
