import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import axios from 'axios';
import { get_api_url } from '../../base';

const initialState = {
    statsStaff: [],
    loading: false,
    error: false
};

const api_url = get_api_url();

export const getStatsStaff = createAsyncThunk(
    'stats/getStatsStaff',
    async () => {
        const res = await axios.get(`${api_url}/api/stats/tour_of_staff`);
        return res.data;
    }
)

export const statsSlice = createSlice({
    name: "stats",
    initialState,
    reducers: {},
    extraReducers: builder => {
        builder
            .addCase(getStatsStaff.pending, (state) => {
                return {...state, loading: true };
            })
            .addCase(getStatsStaff.fulfilled, (state, action) => {
                return {...state, loading: false, statsStaff: action.payload};
            })
            .addCase(getStatsStaff.rejected, (state) => {
                return {...state, error: true, loading: false};
            })
    }
});

export const selectStatsStaff = (state) => state.stats.statsStaff;

export default statsSlice.reducer;