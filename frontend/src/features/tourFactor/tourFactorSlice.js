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

export const getTypesFactor = createAsyncThunk(
    'factor/getTypesFactor',
    async () => {
        const res = await axios.get(`${api_url}/api/tour/tour_type`);
        return res.data;
    }
);

export const createTypesFactor = createAsyncThunk(
    'factor/createTypeFactor',
    async (newType) => {
        const res = await axios.post(`${api_url}/api/tour/tour_type`, newType);
        return res.data;
    }
);

export const updateTypesFactor = createAsyncThunk(
    'factor/updateTypeFactor',
    async (typeUpdate) => {
        const res = await axios.patch(`${api_url}/api/tour/tour_type/${typeUpdate.id}`, typeUpdate);
        return res.data;
    }
);

export const deleteTypesFactor = createAsyncThunk(
    'factor/deleteTypeFactor',
    async (id) => {
        const res = await axios.delete(`${api_url}/api/tour/tour_type/${id}`);
        return res.data;
    }
);

export const getLocationsFactor = createAsyncThunk(
    'factor/getLocationsFactor',
    async () => {
        const res = await axios.get(`${api_url}/api/tour/location`);
        return res.data;
    }
);

export const createLocationsFactor = createAsyncThunk(
    'factor/createLocationsFactor',
    async (newLocate) => {
        const res = await axios.post(`${api_url}/api/tour/location`, newLocate);
        return res.data;
    }
);

export const updateLocationsFactor = createAsyncThunk(
    'factor/updateLocationsFactor',
    async (locateUpdate) => {
        const res = await axios.patch(`${api_url}/api/tour/location/${locateUpdate.id}`, locateUpdate);
        return res.data;
    }
);

export const deleteLocationsFactor = createAsyncThunk(
    'factor/deleteLocationsFactor',
    async (id) => {
        const res = await axios.delete(`${api_url}/api/tour/location/${id}`);
        return res.data;
    }
);

export const getPricesFactor = createAsyncThunk(
    'factor/getPricesFactor',
    async () => {
        const res = await axios.get(`${api_url}/api/tour/tour_price`);
        return res.data;
    }
);

export const createPriceFactor = createAsyncThunk(
    'factor/createPriceFactor',
    async (newPrice) => {
        const res = await axios.post(`${api_url}/api/tour/tour_price`, newPrice);
        return res.data;
    }
);

export const updatePriceFactor = createAsyncThunk(
    'factor/updatePriceFactor',
    async (priceUpdate) => {
        const res = await axios.patch(`${api_url}/api/tour/tour_price/${priceUpdate.id}`, priceUpdate);
        return res.data;
    }
);

export const deletePriceFactor = createAsyncThunk(
    'factor/deletePriceFactor',
    async (id) => {
        const res = await axios.delete(`${api_url}/api/tour/tour_price/${id}`);
        return res.data;
    }
);

export const tourFactorSlice = createSlice({
    name: 'factor',
    initialState,
    reducers: {},
    extraReducers: builder => {
        builder
            // Characteristic
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

            // Types
            .addCase(getTypesFactor.pending, (state) => {
                return {...state, loading: true};
            })
            .addCase(getTypesFactor.fulfilled, (state, action) => {
                return {...state, loading: false, types: action.payload};
            })
            .addCase(getTypesFactor.rejected, (state) => {
                return {...state, loading: false, error: true};
            })
            .addCase(createTypesFactor.pending, (state) => {
                return {...state, loading: true};
            })
            .addCase(createTypesFactor.fulfilled, (state) => {
                return {...state, loading: false};
            })
            .addCase(createTypesFactor.rejected, (state) => {
                return {...state, loading: false, error: true};
            })
            .addCase(updateTypesFactor.pending, (state) => {
                return {...state, loading: true};
            })
            .addCase(updateTypesFactor.fulfilled, (state) => {
                return {...state, loading: false};
            })
            .addCase(updateTypesFactor.rejected, (state) => {
                return {...state, loading: false, error: true};
            })
            .addCase(deleteTypesFactor.pending, (state) => {
                return {...state, loading: true};
            })
            .addCase(deleteTypesFactor.fulfilled, (state) => {
                return {...state, loading: false};
            })
            .addCase(deleteTypesFactor.rejected, (state) => {
                return {...state, loading: false, error: true};
            })
            
            // Locations
            .addCase(getLocationsFactor.pending, (state) => {
                return {...state, loading: true};
            })
            .addCase(getLocationsFactor.fulfilled, (state, action) => {
                return {...state, loading: false, locations: action.payload};
            })
            .addCase(getLocationsFactor.rejected, (state) => {
                return {...state, loading: false, error: true};
            })
            .addCase(createLocationsFactor.pending, (state) => {
                return {...state, loading: true};
            })
            .addCase(createLocationsFactor.fulfilled, (state) => {
                return {...state, loading: false};
            })
            .addCase(createLocationsFactor.rejected, (state) => {
                return {...state, loading: false, error: true};
            })
            .addCase(updateLocationsFactor.pending, (state) => {
                return {...state, loading: true};
            })
            .addCase(updateLocationsFactor.fulfilled, (state) => {
                return {...state, loading: false};
            })
            .addCase(updateLocationsFactor.rejected, (state) => {
                return {...state, loading: false, error: true};
            })
            .addCase(deleteLocationsFactor.pending, (state) => {
                return {...state, loading: true};
            })
            .addCase(deleteLocationsFactor.fulfilled, (state) => {
                return {...state, loading: false};
            })
            .addCase(deleteLocationsFactor.rejected, (state) => {
                return {...state, loading: false, error: true};
            })

            // Prices
            .addCase(getPricesFactor.pending, (state) => {
                return {...state, loading: true};
            })
            .addCase(getPricesFactor.fulfilled, (state, action) => {
                return {...state, loading: false, prices: action.payload};
            })
            .addCase(getPricesFactor.rejected, (state) => {
                return {...state, loading: false, error: true};
            })
            .addCase(createPriceFactor.pending, (state) => {
                return {...state, loading: true};
            })
            .addCase(createPriceFactor.fulfilled, (state) => {
                return {...state, loading: false};
            })
            .addCase(createPriceFactor.rejected, (state) => {
                return {...state, loading: false, error: true};
            })
            .addCase(updatePriceFactor.pending, (state) => {
                return {...state, loading: true};
            })
            .addCase(updatePriceFactor.fulfilled, (state) => {
                return {...state, loading: false};
            })
            .addCase(updatePriceFactor.rejected, (state) => {
                return {...state, loading: false, error: true};
            })
            .addCase(deletePriceFactor.pending, (state) => {
                return {...state, loading: true};
            })
            .addCase(deletePriceFactor.fulfilled, (state) => {
                return {...state, loading: false};
            })
            .addCase(deletePriceFactor.rejected, (state) => {
                return {...state, loading: false, error: true};
            })
    }
});

export const selectLocationFactor = (state) => state.factors.locations;
export const selectCharacteristicFactor = (state) => state.factors.characteristics;
export const selectTypeFactor = (state) => state.factors.types;
export const selectPriceFactor = (state) => state.factors.prices;

export default tourFactorSlice.reducer;