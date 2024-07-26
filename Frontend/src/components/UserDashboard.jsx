import React, { useEffect, useState } from 'react';
import axiosInstance from './axiosInstance';
import { useUser } from './UserContext';
import { Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const { user } = useUser();
  const [dashboardData, setDashboardData] = useState('');
  const navigate = useNavigate();

  const fetchDashboardData = async () => {
    try {
      console.log('Fetching dashboard data'); // Debug log
      const response = await axiosInstance.get('/users/dashboard');
      console.log('Dashboard data fetched:', response.data); // Debug log
      setDashboardData(response.data);
    } catch (error) {
      console.error('Failed to fetch dashboard data', error);
    }
  };

  useEffect(() => {
    console.log('Dashboard component mounted'); // Debug log

    if (user) {
      fetchDashboardData();
    } else {
      console.log('User is not authenticated'); // Debug log
      navigate('/users/login');
    }
  }, [user, navigate]);

  return (
    <div>
      <h1>Dashboard</h1>
      {user && <p>Welcome, {user.username}!</p>}
      {dashboardData && (
        <div>
          <Button variant="primary" onClick={() => navigate('/order-ride')}>
            Order a Ride
          </Button>
          <Button variant="primary" onClick={() => navigate('/order-status')}>
            Check the status of your ride orders
          </Button>
        </div>
      )}
      <Button variant="secondary" onClick={fetchDashboardData}>
        Fetch Data Manually
      </Button>
    </div>
  );
};
export default Dashboard 