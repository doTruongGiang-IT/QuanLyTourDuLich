import React, {useEffect, useState} from 'react';
import TourListForm from '../../components/TourListForm/TourListForm';
import {useSelector, useDispatch} from 'react-redux';
import { selectTourList, selectTourEdit, getTourList, editTour, deleteTour, selectTourCharacteristic, selectTourType, getTourCharacteristic, getTourType } from '../../features/tour/tourSlice';

const TourListPage = () => {
    const dispatch = useDispatch();
    const tours = useSelector(selectTourList);
    const characteristics = useSelector(selectTourCharacteristic);
    const types = useSelector(selectTourType);
    const tourEdit = useSelector(selectTourEdit);
    const [tourList, setTourList] = useState(tours.results);

    useEffect(() => {
        dispatch(getTourList());
    }, [dispatch, tourList]);

    const handleDelete = (id) => {
        dispatch(deleteTour(id));
        setTourList(tours.results.forEach(tour => tour.id !== id));
    };

    const formatEditTour = (updateTour) => {
        delete updateTour.key;
        delete updateTour.price;
        delete updateTour.location;
        delete updateTour.price_name;
        dispatch(getTourCharacteristic());
        dispatch(getTourType());
        characteristics.forEach(characteristic => {
            if(characteristic.name === updateTour.characteristic) {
                updateTour.characteristic = characteristic.id;
            };
        });
        types.forEach(type => {
            if(type.name === updateTour.type) {
                updateTour.type = type.id;
            };
        });
    };

    const saveEdit = (updateTour) => {
        formatEditTour(updateTour);
        dispatch(editTour(updateTour));
        tours.results.forEach(tour => {
            if(tour.id === updateTour.id) {
                tour = {...tour, ...updateTour};
            };
        });
        setTourList(tours.results);
    };

    return (
        <TourListForm tours={tours.results} remove={handleDelete} update={saveEdit} tourEdit={tourEdit} />
    )
}

export default TourListPage;
