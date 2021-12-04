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
    selectTypeFactor,
    getTypesFactor,
    updateTypesFactor,
    deleteTypesFactor,
    createTypesFactor,
} from '../../features/tourFactor/tourFactorSlice';

const TourFactorPage = () => {
    const [isVisible, setIsVisible] = useState(false);
    const dispatch = useDispatch();
    const characteristicsFactor = useSelector(selectCharacteristicFactor);
    const typesFactor = useSelector(selectTypeFactor);
    const [charFactor, setCharFactor] = useState(characteristicsFactor);
    const [typeFactor, setTypeFactor] = useState(typesFactor);

    useEffect(() => {
        dispatch(getCharacteristicsFactor());
        dispatch(getTypesFactor());
    }, [dispatch, charFactor, typeFactor]);

    const handleVisible = () => {
        setIsVisible(!isVisible);
    };

    const handleUpdateChar = async (charUpdate) => {
        delete charUpdate.key;
        await dispatch(updateCharacteristicsFactor(charUpdate));
        characteristicsFactor.forEach(char => {
            if(char.id === charUpdate.id) {
                char = {...char, ...charUpdate};
            };
        });
        setCharFactor(characteristicsFactor);
    };

    const handleDeleteChar = async (id) => {
        await dispatch(deleteCharacteristicsFactor(id));
        setCharFactor(characteristicsFactor.filter(char => char.id !== id));
    };

    const handleSubmitChar = async (newChar) => {
        await dispatch(createCharacteristicsFactor(newChar));
        setCharFactor(characteristicsFactor.map(() => ([...characteristicsFactor, newChar])));
    };

    const handleUpdateType = async (typeUpdate) => {
        delete typeUpdate.key;
        await dispatch(updateTypesFactor(typeUpdate));
        typesFactor.forEach(type => {
            if(type.id === typeUpdate.id) {
                type = {...type, ...typeUpdate};
            };
        });
        setTypeFactor(typesFactor);
    };

    const handleDeleteType = async (id) => {
        await dispatch(deleteTypesFactor(id));
        setTypeFactor(typesFactor.filter(type => type.id !== id));
    };

    const handleSubmitType = async (newType) => {
        await dispatch(createTypesFactor(newType));
        setTypeFactor(typesFactor.map(() => ([...typesFactor, newType])));
    };

    return (
        <div className="tourFactorsPage">
            <div className="tourItem">
                <TourCharacteristic 
                    characteristicsFactor={characteristicsFactor} 
                    update={handleUpdateChar} remove={handleDeleteChar}
                    submit={handleSubmitChar}
                />
                <TourType 
                    typeFactor={typesFactor} update={handleUpdateType} 
                    remove={handleDeleteType} submit={handleSubmitType}
                />
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