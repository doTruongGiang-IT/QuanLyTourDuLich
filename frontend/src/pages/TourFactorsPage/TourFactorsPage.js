import React, {useState} from 'react'
import TourCharacteristic from '../../components/TourCharacteristic/TourCharacteristic';
import TourLocation from '../../components/TourLocation/TourLocation';
import TourPrice from '../../components/TourPrice/TourPrice';
import TourType from '../../components/TourType/TourType';
import './TourFactorsPage.css';

const TourFactorPage = () => {
    const[isVisible, setIsVisible] = useState(false);

    const handleVisible = () => {
        setIsVisible(!isVisible);
    };

    return (
        <div className="tourFactorsPage">
            <div className="tourItem">
                <TourCharacteristic />
                <TourType />
            </div>
            {
                !isVisible ?
                <p id="showMore" onClick={handleVisible}>Show more...</p> : 
                (
                    <>
                        <div id="moreItem">
                            <div className="tourItem">
                                <TourPrice />
                            </div>
                            <div className="tourItem">
                                <TourLocation />
                            </div>
                        </div>
                        <p id="showMore" onClick={handleVisible}>Show less...</p>
                    </>
                )
            }
        </div>

    )
}

export default TourFactorPage;
