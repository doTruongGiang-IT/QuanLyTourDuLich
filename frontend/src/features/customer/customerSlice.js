import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import axios from 'axios';
import { get_api_url } from '../../base';

const initialState = {
    customerList: [],
    customer: {},
    customerGroup: [],
    loading: false,
    error: false
};

const api_url = get_api_url();

export const getAllCustomer = createAsyncThunk(
    'customer/getAllCustomer',
    async () => {
        const res = await axios.get(`${api_url}/api/customer`);
        return res.data;
    }
);

export const getCustomer = createAsyncThunk(
    'customer/getCustomer',
    async (id) => {
        const res = await axios.get(`${api_url}/api/customer/${id}`);
        return res.data;
    }
);

export const createCustomer = createAsyncThunk(
    'customer/createCustomer',
    async (customer) => {
        const res = await axios.post(`${api_url}/api/customer/`, customer);
        return res.data;
    }
);

export const updateCustomer = createAsyncThunk(
    'customer/updateCustomer',
    async (customer) => {
        const res = await axios.patch(`${api_url}/api/customer/${customer.id}`, customer);
        return res.data;
    }
);

export const deleteCustomer = createAsyncThunk(
    'customer/deleteCustomer',
    async (id) => {
        const res = await axios.delete(`${api_url}/api/customer/${id}`);
        return res.data;
    }
);

export const getCustomerByGroup = createAsyncThunk(
    'customer/getCustomerByGroup',
    async (id) => {
        const res = await axios.get(`${api_url}/api/customer/group/${id}`);
        return res.data;
    }
);

export const addCustomerToGroup = createAsyncThunk(
    'customer/addCustomerTOGroup',
    async (cusGroup) => {
        const res = await axios.post(`${api_url}/api/customer/group/`, cusGroup);
        return res.data;
    }
);

export const deleteCustomerFromGroup = createAsyncThunk(
    'customer/deleteCustomerFromGroup',
    async (groupId, cusId) => {
        const res = await axios.delete(`${api_url}/api/customer/group/?group_id=${groupId}&customer_id=${cusId}`);
        return res.data;
    }
);

export const customerSlice = createSlice({
    name: 'customer',
    initialState,
    reducers: {},
    extraReducers: builder => {
        builder
            .addCase(getAllCustomer.pending, (state) => {
                return {...state, loading: true };
            })
            .addCase(getAllCustomer.fulfilled, (state, action) => {
                return {...state, loading: false, customerList: action.payload};
            })
            .addCase(getAllCustomer.rejected, (state) => {
                return {...state, error: true, loading: false};
            })
            .addCase(getCustomer.pending, (state) => {
                return {...state, loading: true };
            })
            .addCase(getCustomer.fulfilled, (state, action) => {
                return {...state, loading: false, customer: action.payload};
            })
            .addCase(getCustomer.rejected, (state) => {
                return {...state, error: true, loading: false};
            })
            .addCase(createCustomer.pending, (state) => {
                return {...state, loading: true };
            })
            .addCase(createCustomer.fulfilled, (state) => {
                return {...state, loading: false};
            })
            .addCase(createCustomer.rejected, (state) => {
                return {...state, error: true, loading: false};
            })
            .addCase(updateCustomer.pending, (state) => {
                return {...state, loading: true };
            })
            .addCase(updateCustomer.fulfilled, (state) => {
                return {...state, loading: false};
            })
            .addCase(updateCustomer.rejected, (state) => {
                return {...state, error: true, loading: false};
            })
            .addCase(deleteCustomer.pending, (state) => {
                return {...state, loading: true };
            })
            .addCase(deleteCustomer.fulfilled, (state) => {
                return {...state, loading: false};
            })
            .addCase(deleteCustomer.rejected, (state) => {
                return {...state, error: true, loading: false};
            })
            .addCase(getCustomerByGroup.pending, (state) => {
                return {...state, loading: true };
            })
            .addCase(getCustomerByGroup.fulfilled, (state, action) => {
                return {...state, loading: false, customerGroup: action.payload};
            })
            .addCase(getCustomerByGroup.rejected, (state) => {
                return {...state, error: true, loading: false};
            })
            .addCase(addCustomerToGroup.pending, (state) => {
                return {...state, loading: true };
            })
            .addCase(addCustomerToGroup.fulfilled, (state, action) => {
                return {...state, loading: false};
            })
            .addCase(addCustomerToGroup.rejected, (state) => {
                return {...state, error: true, loading: false};
            })
            .addCase(deleteCustomerFromGroup.pending, (state) => {
                return {...state, loading: true };
            })
            .addCase(deleteCustomerFromGroup.fulfilled, (state, action) => {
                return {...state, loading: false};
            })
            .addCase(deleteCustomerFromGroup.rejected, (state) => {
                return {...state, error: true, loading: false};
            })
    }
})

export const selectCustomerList = (state) => state.customer.customerList;
export const selectCustomer = (state) => state.customer.customer;
export const selectCustomerGroup = (state) => state.customer.customerGroup;

export default customerSlice.reducer;