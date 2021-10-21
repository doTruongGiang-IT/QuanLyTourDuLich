import React, {useEffect} from 'react';
import TourListForm from '../../components/TourListForm/TourListForm';
import {useSelector, useDispatch} from 'react-redux';
import { selectTourList, getTourList, editTour, deleteTour } from '../../features/tour/tourSlice';

const TourListPage = () => {
    const dispatch = useDispatch();
    const tours = useSelector(selectTourList);

    const handleDelete = (key) => {
        dispatch(deleteTour(key));
    };

    const saveEdit = (updateTour) => {
        dispatch(editTour(updateTour));
    };

    return (
        <TourListForm remove={handleDelete} update={saveEdit} />
    )
}

export default TourListPage;
