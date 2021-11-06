import React, {useState, useEffect} from 'react'
import TourCharacteristic from '../../components/TourCharacteristic/TourCharacteristic';
import TourLocation from '../../components/TourLocation/TourLocation';
import TourPrice from '../../components/TourPrice/TourPrice';
import TourType from '../../components/TourType/TourType';
import './TourFactorsPage.css';
import { useSelector, useDispatch } from 'react-redux';
import { 
    selectCharacteristicFactor, 
    getCharacteristicsFactor,
    updateCharacteristicsFactor,
    deleteCharacteristicsFactor,
    createCharacteristicsFactor,
} from '../../features/tourFactor/tourFactorSlice';

const TourFactorPage = () => {
    const [isVisible, setIsVisible] = useState(false);
    const dispatch = useDispatch();
    const characteristicsFactor = useSelector(selectCharacteristicFactor);
    const [factor, setFactor] = useState(characteristicsFactor);

    useEffect(() => {
        dispatch(getCharacteristicsFactor());
    }, [dispatch, factor]);

    const handleVisible = () => {
        setIsVisible(!isVisible);
    };

    const saveEdit = async (charUpdate) => {
        delete charUpdate.key;
        await dispatch(updateCharacteristicsFactor(charUpdate));
        characteristicsFactor.forEach(char => {
            if(char.id === charUpdate.id) {
                char = {...char, ...charUpdate};
            };
        });
        setFactor(characteristicsFactor);
    };

    const handleDelete = async (id) => {
        await dispatch(deleteCharacteristicsFactor(id));
        setFactor(characteristicsFactor.filter(char => char.id !== id));
    };

    const handleSubmit = async (newChar) => {
        await dispatch(createCharacteristicsFactor(newChar));
        setFactor(characteristicsFactor.map(() => ([...characteristicsFactor, newChar])));
    };

    return (
        <div className="tourFactorsPage">
            <div className="tourItem">
                <TourCharacteristic 
                    characteristicsFactor={characteristicsFactor} 
                    update={saveEdit} remove={handleDelete}
                    submit={handleSubmit}
                />
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