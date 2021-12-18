import React, {useEffect, useState} from 'react';
import './StatsPage.css';
import {useSelector, useDispatch} from 'react-redux';
import { getStatsStaff, selectStatsStaff, getStatsRevenueGroups, selectStatsRevenueGroups, getStatsRevenueTours, selectStatsRevenueTours } from '../../features/stats/statsSlice';
import PieChartComponent from '../../components/PieChart/PieChartComponent';
import BarChartComponent from '../../components/BarChart/BarChartComponent';
import AreaChartComponent from '../../components/AreaChart/AreaChartComponent';

const StatsPage = () => {
    const dispatch = useDispatch();
    const statsStaff = useSelector(selectStatsStaff);
    const statsGroups = useSelector(selectStatsRevenueGroups);
    const statsTours = useSelector(selectStatsRevenueTours);
    const [statsStaffState, setStatsStaffState] = useState(statsStaff);
    const [statsGroupsState, setStatsGroupsState] = useState(statsGroups);
    const [statsToursState, setStatsToursState] = useState(statsTours);
    let revenueGroups = JSON.parse(localStorage.getItem("groupsRevenue"));

    let dataStaff = statsStaff.length > 0 ? statsStaff.map((stat) => {
        return {"name": stat.name, "value": stat.number_of_tours}; 
    }) : [];

    let dataTours = statsTours.length > 0 ? statsTours.map((tour) => {
        return {"id": tour.id, "name": tour.name, "revenue - VND": tour.revenue, "cost - VND": tour.cost}; 
    }) : [];

    let dataGroups = revenueGroups.length > 0 ? revenueGroups.map((group) => {
        return {"id": group.id, "name": group.name, "revenue - VND": group.revenue, "cost - VND": group.cost}; 
    }) : [];

    useEffect(() => {
        dispatch(getStatsStaff());
        dispatch(getStatsRevenueTours());
    }, [dispatch, statsStaffState, statsToursState]);

    useEffect(() => {
        let revenueGroups = [];
        if(statsTours.length > 0) {
            statsTours.forEach(async (tour) => {
                let response = await dispatch(getStatsRevenueGroups(tour.id));
                response.payload.forEach(group => {
                    if(!revenueGroups.includes(group)) {
                        revenueGroups.push(group);
                    };
                    localStorage.setItem("groupsRevenue", JSON.stringify(revenueGroups));
                });
            });
            
        };
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [dispatch]);

    return (
        <div className="statistics">
            <div className="statistics_section">
                <div className="pie_chart">
                    <h2>Statistics Staff</h2>
                    <PieChartComponent data={dataStaff} />
                </div>
                <div className="bar_chart">
                    <h2>Statistics Revenue for Tours</h2>
                    <BarChartComponent data={dataTours} />
                </div>
            </div>
            <div className="statistics_section">
                <div className="bar_chart">
                    <h2>Statistics Cost and Revenue for Groups</h2>
                    <AreaChartComponent data={dataGroups} />
                </div>
            </div>
        </div>
    )
}

export default StatsPage;
