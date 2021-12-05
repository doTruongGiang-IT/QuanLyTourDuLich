import { configureStore } from '@reduxjs/toolkit';
import tourReducer from '../features/tour/tourSlice';
import groupReducer from '../features/group/groupSlice';
import tourFactorReducer from '../features/tourFactor/tourFactorSlice';

export const store = configureStore({
  reducer: {
    tour: tourReducer,
    factors: tourFactorReducer,
    group: groupReducer,
  },
});
