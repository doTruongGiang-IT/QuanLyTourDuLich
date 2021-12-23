import React, {useState, useEffect} from 'react';
import GroupCost from '../../components/GroupCost/GroupCost';
import '../TourFactorsPage/TourFactorsPage.css';
import { useSelector, useDispatch } from 'react-redux';
import { selectCostList, getCostList, selectCostTypes, getCostTypes, createCost, updateCost, deleteCost } from '../../features/groupCost/groupCostSlice';

const GroupCostPage = () => {
    const dispatch = useDispatch();
    const costTypes = useSelector(selectCostTypes);
    const costList = useSelector(selectCostList);
    const [typeState, setTypeState] = useState(costTypes);
    const [costState, setCostState] = useState(costList);

    useEffect(() =>{
        dispatch(getCostTypes());
        dispatch(getCostList());
    }, [dispatch, typeState, costState]);

    const formatCost = (cost) => {
        let result = {...cost};
        if(typeof cost.type === "string") {
            costTypes.forEach(type => {
                if(type.name === cost.type) {
                    result.type = type.id;
                };
            });
        };
        return result;
    };

    const handleSubmitCost = async (cost) => {
        await dispatch(createCost(cost));
        setCostState(costList.map(() => ([...costList, cost])));
    };

    const handleUpdateCost = async (costUpdate) => {
        delete costUpdate.key;
        let format = formatCost(costUpdate);
        await dispatch(updateCost(format));
        costList.forEach(cost => {
            if(cost.id === format.id) {
                cost = {...cost, ...format};
            };
        });
        setCostState(costList);
    };

    const handleDeleteCost = async (id) => {
        await dispatch(deleteCost(id));
        setCostState(costList.filter(cost => cost.id !== id));
    };

    return (
        <div className="tourFactorsPage">
            <div className="tourItem">
                <GroupCost types={costTypes} costList={costList} submit={handleSubmitCost} update={handleUpdateCost} remove={handleDeleteCost} />
            </div>
        </div>
    )
}

export default GroupCostPage;
