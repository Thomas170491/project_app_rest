import React, { useEffect, useState } from 'react';
import axiosInstance from './axiosInstance';
import { useUser } from './UserContext';

const Dashboard = () => {
  const { user } = useUser();
  const [dashboardData, setDashboardData] = useState(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const response = await axiosInstance.get('/users/dashboard');
        setDashboardData(response.data);
      } catch (error) {
        console.error('Failed to fetch dashboard data', error);
      }
    };

    fetchDashboardData();
  }, []);

  return (
    <div>
      <h1>Dashboard</h1>
      {user && <p>Welcome, {user.username}!</p>}
      {dashboardData && (
        <div>
          {/* Render dashboard data here */}
        </div>
      )}
    </div>
  );
};

export default Dashboard;
