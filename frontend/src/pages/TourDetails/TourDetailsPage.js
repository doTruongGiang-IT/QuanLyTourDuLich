import React, {useEffect} from 'react';
import TourDetailsForm from '../../components/TourDeatailsForm/TourDetailsForm';
import { useParams } from 'react-router';
import { selectTourDetails, getTourDetails, getTourLocation, selectTourLocation } from '../../features/tour/tourSlice';
import { useSelector, useDispatch } from 'react-redux';

const TourDetailsPage = () => {
    let {id} = useParams();
    const dispatch = useDispatch();
    const tourDetails = useSelector(selectTourDetails);
    const tourLocation = useSelector(selectTourLocation);

    useEffect(() => {
        dispatch(getTourDetails(id));
        dispatch(getTourLocation(id));
    }, [dispatch, id]);

    return (
        <TourDetailsForm tourDetails={tourDetails} location={tourLocation} />
    )
}

export default TourDetailsPage;
