import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import axios from 'axios';
import { get_api_url } from '../../base';

const initialState = {
    statsStaff: [],
    statsRevenueGroups: [],
    formatRevenueGroups: [],
    statsRevenueTours: [],
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
);

export const getStatsRevenueGroups = createAsyncThunk(
    'stats/getStatsRevenueGroups',
    async (id) => {
        const res = await axios.get(`${api_url}/api/stats/stats_cost_revenue_group/${id}`);
        return res.data;
    }
);

export const getStatsRevenueTours = createAsyncThunk(
    'stats/getStatsRevenueTours',
    async () => {
        const res = await axios.get(`${api_url}/api/stats/stats_cost_revenue_tour`);
        return res.data;
    }
);

export const statsSlice = createSlice({
    name: "stats",
    initialState,
    reducers: {
        addRevenueGroup: (state, action) => {
            return [...state.formatRevenueGroups, ...action.payload];
        },
    },
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
            .addCase(getStatsRevenueGroups.pending, (state) => {
                return {...state, loading: true };
            })
            .addCase(getStatsRevenueGroups.fulfilled, (state, action) => {
                return {...state, loading: false, statsRevenueGroups: action.payload};
            })
            .addCase(getStatsRevenueGroups.rejected, (state) => {
                return {...state, error: true, loading: false};
            })
            .addCase(getStatsRevenueTours.pending, (state) => {
                return {...state, loading: true };
            })
            .addCase(getStatsRevenueTours.fulfilled, (state, action) => {
                return {...state, loading: false, statsRevenueTours: action.payload};
            })
            .addCase(getStatsRevenueTours.rejected, (state) => {
                return {...state, error: true, loading: false};
            })
    }
});

export const {addRevenueGroup} = statsSlice.actions;

export const selectStatsStaff = (state) => state.stats.statsStaff;
export const selectStatsRevenueGroups = (state) => state.stats.statsRevenueGroups;
export const selectFormatRevenueGroups = (state) => state.stats.formatRevenueGroups;
export const selectStatsRevenueTours = (state) => state.stats.statsRevenueTours;

export default statsSlice.reducer;