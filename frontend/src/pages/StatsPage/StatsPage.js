import React, {useEffect, useState} from 'react';
import './StatsPage.css';
import {useSelector, useDispatch} from 'react-redux';
import { getStatsStaff, selectStatsStaff } from '../../features/stats/statsSlice';
import PieChartComponent from '../../components/PieChart/PieChartComponent';
import BarChartComponent from '../../components/BarChart/BarChartComponent';

const dataIncome = [
    {
        "name": "Jan",
        "revenue - VND": 2521,
        "cost - VND": 4000,
    },
    {
        "name": "Feb",
        "revenue - VND": 1021,
        "cost - VND": 3000,
    },
    {
        "name": "March",
        "revenue - VND": 521,
        "cost - VND": 2000,
    },
    {
        "name": "April",
        "revenue - VND": 1521,
        "cost - VND": 2780,
    },
    {
        "name": "May",
        "revenue - VND": 239,
        "cost - VND": 1890,
    },
    {
        "name": "June",
        "revenue - VND": 921,
        "cost - VND": 2390,
    },
    {
        "name": "July",
        "revenue - VND": 1821,
        "cost - VND": 3490,
    },
    {
        "name": "Aug",
        "revenue - VND": 521,
        "cost - VND": 2490,
    },
    {
        "name": "Sep",
        "revenue - VND": 1243,
        "cost - VND": 2990,
    },
    {
        "name": "Oct",
        "revenue - VND": 1645,
        "cost - VND": 3190,
    },
    {
        "name": "Nov",
        "revenue - VND": 1221,
        "cost - VND": 4490,
    },
    {
        "name": "Dec",
        "revenue - VND": 2121,
        "cost - VND": 4190,
    },
];

const StatsPage = () => {
    const dispatch = useDispatch();
    const statsStaff = useSelector(selectStatsStaff);
    const [statsStaffState, setStatsStaffState] = useState(statsStaff);
    let dataStaff = statsStaff.length > 0 ? statsStaff.map((stat) => {
        return {"name": stat.name.replace('nhan vien ', 'NV'), "value": stat.number_of_tours}; 
    }) : [];

    useEffect(() => {
        dispatch(getStatsStaff());
    }, [dispatch, statsStaffState]);

    return (
        <div className="statistics">
            <div className="statistics_section">
                <div className="pie_chart">
                    <h2>Statistics Staff</h2>
                    <PieChartComponent data={dataStaff} />
                </div>
                <div className="bar_chart">
                    <h2>Statistics Revenue for Group</h2>
                    <BarChartComponent data={dataIncome} />
                </div>
            </div>
            <div className="statistics_section">
                <div className="bar_chart">
                    <h2>Statistics Cost and Revenue for Tour</h2>
                    <BarChartComponent data={dataIncome} />
                </div>
            </div>
        </div>
    )
}

export default StatsPage;
