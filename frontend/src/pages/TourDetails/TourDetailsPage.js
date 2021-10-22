import React, {useEffect} from 'react';
import TourDetailsForm from '../../components/TourDeatailsForm/TourDetailsForm';
import { useParams } from 'react-router';
import { selectTourDetails, getTourDetails } from '../../features/tour/tourSlice';
import { useSelector, useDispatch } from 'react-redux';

const TourDetailsPage = () => {
    let {id} = useParams();
    const dispatch = useDispatch();
    const tourDetails = useSelector(selectTourDetails);

    useEffect(() => {
        dispatch(getTourDetails(id));
    }, [dispatch, id]);

    return (
        <TourDetailsForm tourDetails={tourDetails} />
    )
}

export default TourDetailsPage;
