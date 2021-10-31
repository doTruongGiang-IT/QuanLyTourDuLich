import React from 'react';
import GuestsForm from '../../components/GuestsForm/GuestsForm';
import {useSelector, useDispatch} from 'react-redux';

const GuestsPage = () => {
    const dispatch = useDispatch();
    
    return (
        <div>
            <GuestsForm />
        </div>
    )
}

export default GuestsPage;
