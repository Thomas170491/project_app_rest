import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './components/Home';
import AdminDashboard from './components/AdminDashboard';
import DriverDashboard from './components/DriverDashboard';
import UserDashboard from './components/UserDashboard';
import UserLogin from './components/UserLogin';
//import OrderRide from './components/OrderRide';
import AcceptRide from './components/DriverAcceptRide';
import DeclineRide from './components/DriverDeclineRide';
import { UserProvider } from './components/UserContext';
import ProtectedRoute from './components/ProtectedRoute';
import './App.css'

const App = () => {
  return (
    <Router>
      <UserProvider>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/admin/dashboard" element={<ProtectedRoute component={AdminDashboard} roles={['admin']} />} />
          <Route path="/drivers/dashboard" element={<ProtectedRoute component={DriverDashboard} roles={['driver']} />} />
          <Route path="/users/dashboard" element={<ProtectedRoute component={UserDashboard} roles={['user']} />} />
          <Route path="/users/login" element={<UserLogin />} />
          {/* <Route path="/users/order_ride" element={<OrderRide />} /> */}
          <Route path="/drivers/accept_ride/:rideId" element={<AcceptRide />} />
          <Route path="/drivers/decline_ride/:rideId" element={<DeclineRide />} />
        </Routes>
      </UserProvider>
    </Router>
  );
};

export default App;
