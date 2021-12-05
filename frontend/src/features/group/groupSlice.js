import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import axios from 'axios';
import { get_api_url } from '../../base';

const initialState = {
    group: {},
    loading: false,
    error: false
};

const api_url = get_api_url();

export const getGroup = createAsyncThunk(
    'group/getGroup',
    async (id) => {
        const res = await axios.get(`${api_url}/api/group/${id}`);
        return res.data;
    }
);

export const createGroup = createAsyncThunk(
    'group/createGroup',
    async (group) => {
        const res = await axios.post(`${api_url}/api/group/`, group);
        return res.data;
    }
);

export const updateGroup = createAsyncThunk(
    'group/updateGroup',
    async (group) => {
        const res = await axios.patch(`${api_url}/api/group/${group.id}`, group);
        return res.data;
    }
);

export const deleteGroup = createAsyncThunk(
    'group/deleteGroup',
    async (id) => {
        const res = await axios.delete(`${api_url}/api/group/${id}`);
        return res.data;
    }
);

export const groupSlice = createSlice({
    name: "group",
    initialState,
    reducers: {},
    extraReducers: builder => {
        builder
            .addCase(getGroup.pending, (state) => {
                return {...state, loading: true };
            })
            .addCase(getGroup.fulfilled, (state, action) => {
                return {...state, loading: false, group: action.payload};
            })
            .addCase(getGroup.rejected, (state) => {
                return {...state, error: true, loading: false};
            })
            .addCase(createGroup.pending, (state) => {
                return {...state, loading: true };
            })
            .addCase(createGroup.fulfilled, (state, ) => {
                return {...state, loading: false};
            })
            .addCase(createGroup.rejected, (state) => {
                return {...state, error: true, loading: false};
            })
            .addCase(updateGroup.pending, (state) => {
                return {...state, loading: true };
            })
            .addCase(updateGroup.fulfilled, (state, ) => {
                return {...state, loading: false};
            })
            .addCase(updateGroup.rejected, (state) => {
                return {...state, error: true, loading: false};
            })
            .addCase(deleteGroup.pending, (state) => {
                return {...state, loading: true };
            })
            .addCase(deleteGroup.fulfilled, (state, ) => {
                return {...state, loading: false};
            })
            .addCase(deleteGroup.rejected, (state) => {
                return {...state, error: true, loading: false};
            })
    }
});

export const selectGroup = (state) => state.group.group;

export default groupSlice.reducer;