import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import axios from 'axios';
import { get_api_url } from '../../base';

const initialState = {
    costTypes: [],
    costList: [],
    loading: false,
    error: false
};

const api_url = get_api_url();

export const getCostTypes = createAsyncThunk(
    'groupCost/getCostTypes',
    async () => {
        const res = await axios.get(`${api_url}/api/group/cost_type`);
        return res.data;
    }
);

export const getCostList = createAsyncThunk(
    'groupCost/getCostList',
    async () => {
        const res = await axios.get(`${api_url}/api/group/cost`);
        return res.data;
    }
);

export const createCost = createAsyncThunk(
    'groupCost/createCost',
    async (cost) => {
        const res = await axios.post(`${api_url}/api/group/cost`, cost);
        return res.data;
    }
);

export const updateCost = createAsyncThunk(
    'groupCost/updateCost',
    async (cost) => {
        const res = await axios.patch(`${api_url}/api/group/cost/${cost.id}`, cost);
        return res.data;
    }
);

export const deleteCost = createAsyncThunk(
    'groupCost/deleteCost',
    async (id) => {
        const res = await axios.delete(`${api_url}/api/group/cost/${id}`);
        return res.data;
    }
);

export const groupCostSlice = createSlice({
    name: 'groupCost',
    initialState,
    reducers: {},
    extraReducers: builder => {
        builder 
            .addCase(getCostTypes.pending, state => {
                return {...state, loading: true};
            })
            .addCase(getCostTypes.fulfilled, (state, action) => {
                return {...state, loading: false, costTypes: action.payload};
            })
            .addCase(getCostTypes.rejected, state => {
                return {...state, loading: false, error: true};
            })
            .addCase(getCostList.pending, state => {
                return {...state, loading: true};
            })
            .addCase(getCostList.fulfilled, (state, action) => {
                return {...state, loading: false, costList: action.payload};
            })
            .addCase(getCostList.rejected, state => {
                return {...state, loading: false, error: true};
            })
            .addCase(createCost.pending, state => {
                return {...state, loading: true};
            })
            .addCase(createCost.fulfilled, (state) => {
                return {...state, loading: false};
            })
            .addCase(createCost.rejected, state => {
                return {...state, loading: false, error: true};
            })
            .addCase(updateCost.pending, state => {
                return {...state, loading: true};
            })
            .addCase(updateCost.fulfilled, (state) => {
                return {...state, loading: false};
            })
            .addCase(updateCost.rejected, state => {
                return {...state, loading: false, error: true};
            })
            .addCase(deleteCost.pending, state => {
                return {...state, loading: true};
            })
            .addCase(deleteCost.fulfilled, (state) => {
                return {...state, loading: false};
            })
            .addCase(deleteCost.rejected, state => {
                return {...state, loading: false, error: true};
            })
    }
});

export const selectCostTypes = (state) => state.groupCost.costTypes;
export const selectCostList = (state) => state.groupCost.costList;

export default groupCostSlice.reducer;