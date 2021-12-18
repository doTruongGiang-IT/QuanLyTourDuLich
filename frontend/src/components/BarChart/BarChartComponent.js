import React from 'react';
import {BarChart, Bar, ResponsiveContainer, CartesianGrid, XAxis, YAxis, Tooltip, Legend, LabelList, Label} from 'recharts';

const BarChartComponent = ({data}) => {
    return (
        <ResponsiveContainer width="100%" height={500}>
            <BarChart data={data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" interval={0} height={100} display="none"/>
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="cost - VND" fill="#8884d8" />
                {/* <Bar dataKey="revenue - VND" fill="#82ca9d" /> */}
                <Bar dataKey="revenue - VND" fill="#82ca9d">
                    <LabelList dataKey="name" position="bottom" />
                </Bar>
            </BarChart>
        </ResponsiveContainer>
    )
};

export default BarChartComponent;