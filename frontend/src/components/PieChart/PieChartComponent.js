import React from 'react';
import {Pie, PieChart, Tooltip, ResponsiveContainer} from 'recharts';

const PieChartComponent = ({data}) => {
    const renderCustomizedLabel = ({
        cx, cy, midAngle, innerRadius, outerRadius, percent, index, name
    }) => {
        const RADIAN = Math.PI / 180;
        const radius = 25 + innerRadius + (outerRadius - innerRadius);
        const x = cx + radius * Math.cos(-midAngle * RADIAN);
        const y = cy + radius * Math.sin(-midAngle * RADIAN);
        return (
            <text x={x} y={y} fill="#8884d8" textAnchor={x > cx ? 'start' : 'end'} dominantBaseline="central">
                {`${name}: ${(percent * 100).toFixed(0)}%`}
            </text>
        );
    };

    return (
        <ResponsiveContainer width="100%" height={400}>
            <PieChart>
                <Pie dataKey="value" isAnimationActive={false} data={data} cx={250} cy={200} outerRadius={150} fill="#8884d8" label={renderCustomizedLabel} />
                <Tooltip />
            </PieChart>
        </ResponsiveContainer>
    )
}

export default PieChartComponent;
