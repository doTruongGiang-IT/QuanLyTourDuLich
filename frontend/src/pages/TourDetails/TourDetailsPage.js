import React, {useEffect} from 'react';
import TourDetailsForm from '../../components/TourDeatailsForm/TourDetailsForm';
import { useParams } from 'react-router';
import { selectTourDetails, getTourDetails, getTourLocation, selectTourLocation, selectListLocation, getListLocation } from '../../features/tour/tourSlice';
import { useSelector, useDispatch } from 'react-redux';

const TourDetailsPage = () => {
    let {id} = useParams();
    const dispatch = useDispatch();
    const tourDetails = useSelector(selectTourDetails);
    const tourLocation = useSelector(selectTourLocation);
    const listLocation = useSelector(selectListLocation);

    useEffect(() => {
        dispatch(getTourDetails(id));
        dispatch(getTourLocation(id));
        dispatch(getListLocation());
    }, [dispatch, id]);

    return (
        <TourDetailsForm tourDetails={tourDetails} location={tourLocation} listLocation={listLocation} />
    )
}

export default TourDetailsPage;
