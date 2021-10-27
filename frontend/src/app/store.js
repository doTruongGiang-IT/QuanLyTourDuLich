import { configureStore } from '@reduxjs/toolkit';
import counterReducer from '../features/counter/counterSlice';
import tourReducer from '../features/tour/tourSlice';

export const store = configureStore({
  reducer: {
    counter: counterReducer,
    tour: tourReducer,
  },
});
