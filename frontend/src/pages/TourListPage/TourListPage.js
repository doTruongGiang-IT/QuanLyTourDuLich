import React, {useEffect, useState} from 'react';
import TourListForm from '../../components/TourListForm/TourListForm';
import {useSelector, useDispatch} from 'react-redux';
import { selectTourList,
    selectTourDetails,
    getTourDetails,
    getTourList, 
    editTour, 
    deleteTour, 
    selectTourPrice, 
    selectTourType, 
    getTourPrice, 
    getTourType 
} from '../../features/tour/tourSlice';

const TourListPage = () => {
    const dispatch = useDispatch();
    const tours = useSelector(selectTourList);
    const prices = useSelector(selectTourPrice);
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
        delete updateTour.location;
        delete updateTour.price_name;
        // delete updateTour.characteristic;
        dispatch(getTourPrice());
        dispatch(getTourType());
        if(typeof updateTour.price === "string") {
            updateTour.price = updateTour.price.slice(0, updateTour.price.length-4);
            updateTour.price = updateTour.price.replaceAll('.', '');  
        };
        prices.forEach(price => {
            if(price.price === Number.parseInt(updateTour.price)) {
                updateTour.price = price.id;
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
        // console.log(updateTour);
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
