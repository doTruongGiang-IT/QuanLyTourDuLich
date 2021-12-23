import { configureStore } from '@reduxjs/toolkit';
import tourReducer from '../features/tour/tourSlice';
import groupReducer from '../features/group/groupSlice';
import tourFactorReducer from '../features/tourFactor/tourFactorSlice';
import groupCostReducer from '../features/groupCost/groupCostSlice';
import statsReducer from '../features/stats/statsSlice';
import customerReducer from '../features/customer/customerSlice';

export const store = configureStore({
  reducer: {
    tour: tourReducer,
    factors: tourFactorReducer,
    group: groupReducer,
    customer: customerReducer,
    stats: statsReducer,
    groupCost: groupCostReducer,
  },
});
