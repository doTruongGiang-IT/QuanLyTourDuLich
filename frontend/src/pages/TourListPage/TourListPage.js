import React, {useEffect, useState} from 'react';
import TourListForm from '../../components/TourListForm/TourListForm';
import {useSelector, useDispatch} from 'react-redux';
import { selectTourList,
    selectTourDetails,
    getTourDetails,
    getTourList, 
    editTour, 
    deleteTour, 
    selectTourCharacteristic, 
    selectTourType, 
    getTourCharacteristic, 
    getTourType 
} from '../../features/tour/tourSlice';

const TourListPage = () => {
    const dispatch = useDispatch();
    const tours = useSelector(selectTourList);
    const characteristics = useSelector(selectTourCharacteristic);
    const types = useSelector(selectTourType);
    const details = useSelector(selectTourDetails);
    const [tourList, setTourList] = useState(tours);

    useEffect(() => {
        dispatch(getTourList());
    }, [dispatch, tourList]);

    const handleDelete = async (id) => {
        await dispatch(deleteTour(id));
        setTourList(tours.filter(tour => tour.id !== id));
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

    const saveEdit = async (updateTour) => {
        await formatEditTour(updateTour);
        await dispatch(editTour(updateTour));
        tours.forEach(tour => {
            if(tour.id === updateTour.id) {
                tour = {...tour, ...updateTour};
            };
        });
        setTourList(tours);
    };

    const handleDetails = (id) => {
        dispatch(getTourDetails(id));
    };

    return (
        <TourListForm tours={tours} remove={handleDelete} update={saveEdit} setDetails={handleDetails} tourDetails={details} />
    )
}

export default TourListPage;
