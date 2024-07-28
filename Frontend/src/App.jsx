import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './components/Home';
//import AdminDashboard from './components/AdminDashboard';
import DriverDashboard from './components/DriverDashboard';
import Dashboard from './components/UserDashboard';
import UserLogin from './components/UserLogin';
import OrderRide from './components/OrderRide';
import OrderStatus from './components/OrderStatus'
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
          <Route path="/users/login" element={<UserLogin />} />
          {/* <Route path="/admin/dashboard" element={<ProtectedRoute component={AdminDashboard} roles={['admin']} />} />  */}
          <Route path="/users/dashboard" element={<ProtectedRoute component={Dashboard} roles={['user']} />} />
          <Route path="/users/order_ride" element={<ProtectedRoute component={OrderRide} roles={['user']} />} />
          <Route path = '/users/order_status/:rideId' element={<ProtectedRoute component={OrderStatus} roles={['user']}/>} />
          <Route path="/drivers/accept_ride/:rideId" element={<ProtectedRoute component={RideAccepted} roles= {['driver']} />} />
          <Route path="/drivers/dashboard" element={<ProtectedRoute component={DriverDashboard} roles={['driver']} />} />
          <Route path="/drivers/decline_ride/:rideId" element={<ProtectedRoute component={DeclineRide} roles={['driver']} />} />
          <Route path='/unauthorized' element ={<Unauthorized />} />
          

        </Routes>
      </UserProvider>
    </Router>
  );
};

export default App;
