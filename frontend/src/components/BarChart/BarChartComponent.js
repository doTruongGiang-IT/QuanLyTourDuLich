import React from 'react';
import {BarChart, Bar, ResponsiveContainer, CartesianGrid, XAxis, YAxis, Tooltip, Legend} from 'recharts';

const BarChartComponent = ({data}) => {
    return (
        <ResponsiveContainer width="100%" height={400}>
            <BarChart data={data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="cost - VND" fill="#8884d8" />
                <Bar dataKey="revenue - VND" fill="#82ca9d" />
            </BarChart>
        </ResponsiveContainer>
    )
};

export default BarChartComponent;