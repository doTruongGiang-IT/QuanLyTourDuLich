import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import axios from 'axios';
import { get_api_url } from '../../base';

const initialState = {
    tourList: [],
    tourLocation: {},
    listLocation: [],
    tourCharacteristics: [],
    tourTypes: [],
    tourPrices: [],
    tourDetails: [],
    tourEdit: {},
    loading: false,
    error: false
};

const api_url = get_api_url();

export const getTourList = createAsyncThunk(
    'tour/getTourList',
    async () => {
        const res = await axios.get(`${api_url}/api/tour?is_format=true`);
        return res.data;
    }
);

export const getTourLocation = createAsyncThunk(
    'tour/getTourLocation',
    async (id) => {
        const res = await axios.get(`${api_url}/api/tour/${id}`);
        return res.data;
    }
);

export const getListLocation = createAsyncThunk(
    'tour/getListLocation',
    async () => {
        const res = await axios.get(`${api_url}/api/tour/location`);
        return res.data;
    }
);

export const getTourCharacteristic = createAsyncThunk(
    'tour/getTourCharacteristic',
    async () => {
        const res = await axios.get(`${api_url}/api/tour/tour_characteristic`);
        return res.data;
    }
);

export const getTourType = createAsyncThunk(
    'tour/getTourType',
    async () => {
        const res = await axios.get(`${api_url}/api/tour/tour_type`);
        return res.data;
    }
);

export const getTourPrice = createAsyncThunk(
    'tour/getTourPrice',
    async () => {
        const res = await axios.get(`${api_url}/api/tour/tour_price`);
        return res.data;
    }
);

export const getTourDetails = createAsyncThunk(
    'tour/getTourDetails',
    async (id) => {
        const res = await axios.get(`${api_url}/api/group?tour_id=${id}`);
        return res.data;
    }
);

export const addTour = createAsyncThunk(
    'tour/addTour',
    async (tour) => {
        const res = await axios.post(`${api_url}/api/tour/`, tour);
        return res.data;
    }
);

export const editTour = createAsyncThunk(
    'tour/editTour',
    async (editTour) => {
        const res = await axios.patch(`${api_url}/api/tour/${editTour.id}`, editTour);
        return res.data;
    }
);

export const deleteTour = createAsyncThunk(
    'tour/deleteTour',
    async (id) => {
        const res = await axios.delete(`${api_url}/api/tour/${id}`);
        return res.data;
    }
);

export const tourSlice = createSlice({
    name: "tour",
    initialState,
    reducers: {},
    extraReducers: builder => {
        builder
            .addCase(getTourCharacteristic.pending, (state) => {
                return {...state, loading: true };
            })
            .addCase(getTourCharacteristic.fulfilled, (state, action) => {
                return {...state, loading: false, tourCharacteristics: action.payload};
            })
            .addCase(getTourCharacteristic.rejected, (state) => {
                return {...state, error: true, loading: false};
            })
            .addCase(getTourType.pending, (state) => {
                return {...state, loading: true };
            })
            .addCase(getTourType.fulfilled, (state, action) => {
                return {...state, loading: false, tourTypes: action.payload};
            })
            .addCase(getTourType.rejected, (state) => {
                return {...state, error: true, loading: false};
            })
            .addCase(getTourPrice.pending, (state) => {
                return {...state, loading: true };
            })
            .addCase(getTourPrice.fulfilled, (state, action) => {
                return {...state, loading: false, tourPrices: action.payload};
            })
            .addCase(getTourPrice.rejected, (state) => {
                return {...state, error: true, loading: false};
            })
            .addCase(getTourLocation.pending, (state) => {
                return {...state, loading: true };
            })
            .addCase(getTourLocation.fulfilled, (state, action) => {
                return {...state, loading: false, tourLocation: action.payload};
            })
            .addCase(getTourLocation.rejected, (state) => {
                return {...state, error: true, loading: false};
            })
            .addCase(getListLocation.pending, (state) => {
                return {...state, loading: true };
            })
            .addCase(getListLocation.fulfilled, (state, action) => {
                return {...state, loading: false, listLocation: action.payload};
            })
            .addCase(getListLocation.rejected, (state) => {
                return {...state, error: true, loading: false};
            })
            .addCase(getTourDetails.pending, (state) => {
                return {...state, loading: true };
            })
            .addCase(getTourDetails.fulfilled, (state, action) => {
                return {...state, loading: false, tourDetails: action.payload};
            })
            .addCase(getTourDetails.rejected, (state) => {
                return {...state, error: true, loading: false};
            })
            .addCase(getTourList.pending, (state) => {
                return {...state, loading: true };
            })
            .addCase(getTourList.fulfilled, (state, action) => {
                return {...state, loading: false, tourList: action.payload};
            })
            .addCase(getTourList.rejected, (state) => {
                return {...state, error: true, loading: false};
            })
            .addCase(addTour.pending, (state) => {
                return {...state, loading: true };
            })
            .addCase(addTour.fulfilled, (state, action) => {
                return {...state, loading: false};
            })
            .addCase(addTour.rejected, (state) => {
                return {...state, error: true, loading: false};
            })
            .addCase(editTour.pending, (state) => {
                return {...state, loading: true };
            })
            .addCase(editTour.fulfilled, (state, action) => {
                return {...state, loading: false, tourEdit: action.payload};
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
export const selectTourLocation = (state) => state.tour.tourLocation;
export const selectListLocation = (state) => state.tour.listLocation;
export const selectTourCharacteristic = (state) => state.tour.tourCharacteristics;
export const selectTourType = (state) => state.tour.tourTypes;
export const selectTourPrice = (state) => state.tour.tourPrices;
export const selectTourEdit = (state) => state.tour.tourEdit;

export default tourSlice.reducer;