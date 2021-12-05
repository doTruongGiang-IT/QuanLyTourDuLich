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
    selectLocationFactor,
    getLocationsFactor,
    updateLocationsFactor,
    deleteLocationsFactor,
    createLocationsFactor,
    selectPriceFactor,
    getPricesFactor,
    createPriceFactor,
    updatePriceFactor,
    deletePriceFactor
} from '../../features/tourFactor/tourFactorSlice';

const TourFactorPage = () => {
    const [isVisible, setIsVisible] = useState(false);
    const dispatch = useDispatch();
    const characteristicsFactor = useSelector(selectCharacteristicFactor);
    const typesFactor = useSelector(selectTypeFactor);
    const locationsFactor = useSelector(selectLocationFactor);
    const pricesFactor = useSelector(selectPriceFactor);
    const [charFactor, setCharFactor] = useState(characteristicsFactor);
    const [typeFactor, setTypeFactor] = useState(typesFactor);
    const [locateFactor, setLocateFactor] = useState(locationsFactor);
    const [priceFactor, setPriceFactor] = useState(pricesFactor);

    useEffect(() => {
        dispatch(getCharacteristicsFactor());
        dispatch(getTypesFactor());
        dispatch(getLocationsFactor());
        dispatch(getPricesFactor());
    }, [dispatch, charFactor, typeFactor, locateFactor, priceFactor]);

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

    const handleUpdateLocate = async (locateUpdate) => {
        delete locateUpdate.key;
        await dispatch(updateLocationsFactor(locateUpdate));
        locationsFactor.forEach(locate => {
            if(locate.id === locateUpdate.id) {
                locate = {...locate, ...locateUpdate};
            };
        });
        setLocateFactor(locationsFactor);
    };

    const handleDeleteLocate = async (id) => {
        await dispatch(deleteLocationsFactor(id));
        setLocateFactor(locationsFactor.filter(locate => locate.id !== id));
    };

    const handleSubmitLocate = async (newLocate) => {
        await dispatch(createLocationsFactor(newLocate));
        setLocateFactor(locationsFactor.map(() => ([...locationsFactor, newLocate])));
    };

    const handleUpdatePrice = async (priceUpdate) => {
        await dispatch(updatePriceFactor(priceUpdate));
        pricesFactor.forEach(price => {
            if(price.id === priceUpdate.id) {
                price = {...price, ...priceUpdate};
            };
        });
        setPriceFactor(pricesFactor);
    };

    const handleDeletePrice = async (id) => {
        await dispatch(deletePriceFactor(id));
        setPriceFactor(pricesFactor.filter(price => price.id !== id));
    };

    const handleSubmitPrice = async (newPrice) => {
        await dispatch(createPriceFactor(newPrice));
        setPriceFactor(pricesFactor.map(() => ([...pricesFactor, newPrice])));
    };

    return (
        <div className="tourFactorsPage">
            <div className="tourItem">
                <TourPrice priceFactor={pricesFactor} submit={handleSubmitPrice} update={handleUpdatePrice} remove={handleDeletePrice} />
            </div>
            {
                !isVisible ?
                <p id="showMore" onClick={handleVisible}>Show more...</p> : 
                (
                    <>
                        <div id="moreItem">
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
                            <div className="tourItem">
                                <TourLocation 
                                    locationsFactor={locationsFactor} update={handleUpdateLocate}
                                    remove={handleDeleteLocate} submit={handleSubmitLocate} 
                                />
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