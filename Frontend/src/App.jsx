import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './components/Home';
//import AdminDashboard from './components/AdminDashboard';
import DriverDashboard from './components/DriverDashboard';
import Dashboard from './components/UserDashboard';
import UserLogin from './components/UserLogin';
import OrderRide from './components/OrderRide';
import RideAccepted from './components/DriverAcceptRide';
import DeclineRide from './components/DriverDeclineRide';
import { UserProvider } from './components/UserContext';
import ProtectedRoute from './components/ProtectedRoute';

import './App.css'
import Unauthorized from './components/Unauthorized';

const App = () => {
  return (
    <Router>
      <UserProvider>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          {/* <Route path="/admin/dashboard" element={<ProtectedRoute component={AdminDashboard} roles={['admin']} />} />  */}
          <Route path="/drivers/dashboard" element={<ProtectedRoute component={DriverDashboard} roles={['driver']} />} />
          <Route path="/users/dashboard" element={<ProtectedRoute component={Dashboard} roles={['user']} />} />
          <Route path="/users/login" element={<UserLogin />} />
          <Route path="/drivers/accept_ride/:rideId" element={< RideAccepted />} />
          <Route path="/drivers/decline_ride/:rideId" element={<DeclineRide />} />
          <Route path="/users/order-ride" element={<ProtectedRoute component={OrderRide} roles={['user']} />} />
        </Routes>
      </UserProvider>
    </Router>
  );
};

export default App;
