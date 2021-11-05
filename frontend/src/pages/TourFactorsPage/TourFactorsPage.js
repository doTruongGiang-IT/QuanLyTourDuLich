import React from 'react'
import TourCharacteristic from '../../components/TourCharacteristic/TourCharacteristic';
import TourPrice from '../../components/TourPrice/TourPrice';
import TourType from '../../components/TourType/TourType';
import './TourFactorsPage.css';

const TourFactorPage = () => {
    return (
        <div className="tourFactorsPage">
            <div className="tourItem">
                <TourCharacteristic />
                <TourType />
            </div>
            <div className="tourItem">
                <TourPrice />
            </div>
        </div>

    )
}

export default TourFactorPage;
