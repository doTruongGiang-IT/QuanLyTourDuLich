import React, {useEffect, useState} from 'react';
import TourDetailsForm from '../../components/TourDeatailsForm/TourDetailsForm';
import { useParams } from 'react-router';
import { selectTourDetails, getTourDetails, getTourLocation, selectTourLocation, selectListLocation, getListLocation } from '../../features/tour/tourSlice';
import { useSelector, useDispatch } from 'react-redux';
import { deleteGroup, updateGroup } from '../../features/group/groupSlice';

const TourDetailsPage = () => {
    let {id} = useParams();
    const dispatch = useDispatch();
    const tourDetails = useSelector(selectTourDetails);
    const tourLocation = useSelector(selectTourLocation);
    const listLocation = useSelector(selectListLocation);
    const [groups, setgroups] = useState(tourDetails);

    useEffect(() => {
        dispatch(getTourDetails(id));
        dispatch(getTourLocation(id));
        dispatch(getListLocation());
    }, [dispatch, id, groups]);

    // useEffect(() => {
    //     dispatch(getTourDetails(id));
    // }, [tourDetails, dispatch, id]);

    const handleDelete = async (id) => {
        await dispatch(deleteGroup(id));
        setgroups(tourDetails.filter(tour => tour.id !== id));
    };

    const handleUpdate = async (groupEdit) => {
        // console.log(groupEdit);
        await dispatch(updateGroup(groupEdit));
        tourDetails.forEach(tour => {
            if(tour.id === groupEdit.id) {
                tour = {...tour, ...groupEdit};
            };
        });
        setgroups(tourDetails);
    };

    return (
        <TourDetailsForm tourDetails={tourDetails} location={tourLocation} listLocation={listLocation} remove={handleDelete} update={handleUpdate} />
    )
}

export default TourDetailsPage;
