import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import axios from 'axios';
import { get_api_url } from '../../base';

const initialState = {
    locations: [],
    characteristics: [],
    types: [],
    prices: [],
    loading: false,
    error: false
};

const api_url = get_api_url();

export const getCharacteristicsFactor = createAsyncThunk(
    'factor/getCharacteristicFactor',
    async () => {
        const res = await axios.get(`${api_url}/api/tour/tour_characteristic`);
        return res.data;
    }
);

export const createCharacteristicsFactor = createAsyncThunk(
    'factor/createCharacteristicFactor',
    async (newChar) => {
        const res = await axios.post(`${api_url}/api/tour/tour_characteristic`, newChar);
        return res.data;
    }
);

export const updateCharacteristicsFactor = createAsyncThunk(
    'factor/updateCharacteristicFactor',
    async (charUpdate) => {
        const res = await axios.patch(`${api_url}/api/tour/tour_characteristic/${charUpdate.id}`, charUpdate);
        return res.data;
    }
);

export const deleteCharacteristicsFactor = createAsyncThunk(
    'factor/deleteCharacteristicFactor',
    async (id) => {
        const res = await axios.delete(`${api_url}/api/tour/tour_characteristic/${id}`);
        return res.data;
    }
);

export const tourFactorSlice = createSlice({
    name: 'factor',
    initialState,
    reducers: {},
    extraReducers: builder => {
        builder
            .addCase(getCharacteristicsFactor.pending, (state) => {
                return {...state, loading: true};
            })
            .addCase(getCharacteristicsFactor.fulfilled, (state, action) => {
                return {...state, loading: false, characteristics: action.payload};
            })
            .addCase(getCharacteristicsFactor.rejected, (state) => {
                return {...state, loading: false, error: true};
            })
            .addCase(createCharacteristicsFactor.pending, (state) => {
                return {...state, loading: true};
            })
            .addCase(createCharacteristicsFactor.fulfilled, (state) => {
                return {...state, loading: false};
            })
            .addCase(createCharacteristicsFactor.rejected, (state) => {
                return {...state, loading: false, error: true};
            })
            .addCase(updateCharacteristicsFactor.pending, (state) => {
                return {...state, loading: true};
            })
            .addCase(updateCharacteristicsFactor.fulfilled, (state) => {
                return {...state, loading: false};
            })
            .addCase(updateCharacteristicsFactor.rejected, (state) => {
                return {...state, loading: false, error: true};
            })
            .addCase(deleteCharacteristicsFactor.pending, (state) => {
                return {...state, loading: true};
            })
            .addCase(deleteCharacteristicsFactor.fulfilled, (state) => {
                return {...state, loading: false};
            })
            .addCase(deleteCharacteristicsFactor.rejected, (state) => {
                return {...state, loading: false, error: true};
            })
    }
});

export const selectLocationFactor = (state) => state.factors.locations;
export const selectCharacteristicFactor = (state) => state.factors.characteristics;
export const selectTypeFactor = (state) => state.factors.types;
export const selectPriceFactor = (state) => state.factors.prices;

export default tourFactorSlice.reducer;