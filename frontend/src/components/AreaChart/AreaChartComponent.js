import React from 'react';
import {AreaChart, Area, ResponsiveContainer, CartesianGrid, XAxis, YAxis, Tooltip, Legend, LabelList} from 'recharts';

const AreaChartComponent = ({data}) => {
    return (
        //margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
        <ResponsiveContainer width="100%" height={500}>
            <AreaChart data={data}>
                <defs>
                    <linearGradient id="colorUv" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#8884d8" stopOpacity={0.8}/>
                        <stop offset="95%" stopColor="#8884d8" stopOpacity={0}/>
                    </linearGradient>
                    <linearGradient id="colorPv" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#82ca9d" stopOpacity={0.8}/>
                        <stop offset="95%" stopColor="#82ca9d" stopOpacity={0}/>
                    </linearGradient>
                </defs>
                <XAxis dataKey="name" interval={0} height={100} angle={45} />
                {/* <XAxis interval={0} height={100} display="none"/> */}
                <YAxis />
                <CartesianGrid strokeDasharray="3 3" />
                <Tooltip />
                <Legend />
                <Area type="monotone" dataKey="cost - VND" stroke="#8884d8" fillOpacity={1} fill="url(#colorUv)" />
                <Area type="monotone" dataKey="revenue - VND" stroke="#82ca9d" fillOpacity={1} fill="url(#colorPv)" >
                    {/* <LabelList dataKey="name" position="bottom" /> */}
                </Area>
            </AreaChart>
        </ResponsiveContainer>
    )
}

export default AreaChartComponent;
