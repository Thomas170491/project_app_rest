import React, { useEffect, useState, useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { UserContext } from './UserContext';
import { getUserDashboard } from './api';


const UserDashboard = () => {
  const { user } = useContext(UserContext);
  const [dashboardData, setDashboardData] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const data = await getUserDashboard();
        setDashboardData(data);
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error);
      }
    };

    fetchDashboardData();
  }, []);

  if (!dashboardData) {
    return <div>Loading...</div>;
  }

  if(data.status == 401){
    alert('You are not allowed to visit this page')
    return navigate('/')
  }

  return (
    <div>
      <h2>User Dashboard</h2>
      <p>Welcome to your dashboard, {user.username}!</p>
      <ul>
        <li>
          <Link to="/order-ride">Order a Ride</Link>
        </li>
        <li>
          <Link to="/order-status">Check the status of your ride orders</Link>
        </li>
      </ul>
    </div>
  );
};

export default UserDashboard;