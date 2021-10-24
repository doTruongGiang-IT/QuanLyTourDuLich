import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import axios from 'axios';
import { get_api_url } from '../../base';

const initialState = {
    tourList: [],
    tourDetails: [],
    loading: false,
    error: false
};

export const getTourList = createAsyncThunk(
    'tour/getTourList',
    async () => {
        const api_url = get_api_url();
        const res = await axios.get(`${api_url}/api/tour/`);
        return res.data;
    }
);

export const getTourDetails = createAsyncThunk(
    'tour/getTourDetails',
    async (id) => {
        const api_url = get_api_url();
        const res = await axios.get(`${api_url}/api/group?tour_id=${id}`);
        return res.data;
    }
);

export const addTour = createAsyncThunk(
    'tour/addTour',
    async (tour) => {
        // const res = axios.post('');
        // return res.data;
        console.log(tour);
    }
);

export const editTour = createAsyncThunk(
    'tour/editTour',
    async (editTour) => {
        // const res = axios.put('');
        // return res.data;
        console.log(editTour);
    }
);

export const deleteTour = createAsyncThunk(
    'tour/deleteTour',
    async (key) => {
        console.log(key);
        // const res = axios.delete('');
        // return res.data;
    }
);

export const tourSlice = createSlice({
    name: "tour",
    initialState,
    reducers: {},
    extraReducers: builder => {
        builder
            .addCase(getTourDetails.pending, (state) => {
                return {...state, loading: true };
            })
            .addCase(getTourDetails.fulfilled, (state, action) => {
                return {...state, loading: false, tourDetails: action.payload.results};
            })
            .addCase(getTourDetails.rejected, (state) => {
                return {...state, error: true, loading: false};
            })
            .addCase(getTourList.pending, (state) => {
                return {...state, loading: true };
            })
            .addCase(getTourList.fulfilled, (state, action) => {
                return {...state, loading: false, tourList: action.payload.results};
            })
            .addCase(getTourList.rejected, (state) => {
                return {...state, error: true, loading: false};
            })
            .addCase(addTour.pending, (state) => {
                return {...state, loading: true };
            })
            .addCase(addTour.fulfilled, (state, action) => {
                return {...state, loading: false, tourList: action.payload};
            })
            .addCase(addTour.rejected, (state) => {
                return {...state, error: true, loading: false};
            })
            .addCase(editTour.pending, (state) => {
                return {...state, loading: true };
            })
            .addCase(editTour.fulfilled, (state, action) => {
                return {...state, loading: false, tourList: action.payload};
            })
            .addCase(editTour.rejected, (state) => {
                return {...state, error: true, loading: false};
            })
            .addCase(deleteTour.pending, (state) => {
                return {...state, loading: true };
            })
            .addCase(deleteTour.fulfilled, (state, action) => {
                return {...state, loading: false, tourList: action.payload};
            })
            .addCase(deleteTour.rejected, (state) => {
                return {...state, error: true, loading: false};
            })
    }
});

export const selectTourList = (state) => state.tour.tourList;
export const selectTourDetails = (state) => state.tour.tourDetails;

export default tourSlice.reducer;