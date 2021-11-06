import { configureStore } from '@reduxjs/toolkit';
import tourReducer from '../features/tour/tourSlice';
import tourFactorReducer from '../features/tourFactor/tourFactorSlice';

export const store = configureStore({
  reducer: {
    tour: tourReducer,
    factors: tourFactorReducer
  },
});
