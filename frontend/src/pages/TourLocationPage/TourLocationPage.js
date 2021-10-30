import React, {useEffect} from 'react';
import TourLocationForm from '../../components/TourLocationForm/TourLocationForm';
import { useParams } from 'react-router';
import { selectTourDetails, getTourDetails} from '../../features/tour/tourSlice';
import { useSelector, useDispatch } from 'react-redux';

const TourLocationPage = () => {
    let {id} = useParams();
    const dispatch = useDispatch();
    const tourDetails = useSelector(selectTourDetails);

    useEffect(() => {
        dispatch(getTourDetails(id));
    }, [dispatch, id]);

    return (
        <div>
            <TourLocationForm locations={tourDetails} />
        </div>
    )
}

export default TourLocationPage;
