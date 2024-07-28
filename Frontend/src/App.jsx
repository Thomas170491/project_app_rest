import React from "react";
import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import Home from "./components/Home";
import Navbar from "./components/Navbar";
//import AdminDashboard from './components/AdminDashboard';
import RideAccepted from "./components/DriverAcceptRide";
import DriverDashboard from "./components/DriverDashboard";
import DeclineRide from "./components/DriverDeclineRide";
import Notification from "./components/Notification";
import OrderRide from "./components/OrderRide";
import OrderStatus from "./components/OrderStatus";
import Pay from "./components/Pay";
import ProtectedRoute from "./components/ProtectedRoute";
import { UserProvider } from "./components/UserContext";
import Dashboard from "./components/UserDashboard";
import UserLogin from "./components/UserLogin";

import "./App.css";
import Unauthorized from "./components/Unauthorized";

const App = () => {
  return (
    <Router>
      <UserProvider>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/users/login" element={<UserLogin />} />
          {/* <Route path="/admin/dashboard" element={<ProtectedRoute component={AdminDashboard} roles={['admin']} />} />  */}
          <Route path="/users/dashboard" element={<Dashboard />} />
          <Route path="/users/order_ride" element={<OrderRide />} />
          <Route path="/notification" element={<Notification />} />
          <Route path="/users/payment" element={<Pay />} />
          <Route
            path="/users/order_status/:rideId"
            element={
              <ProtectedRoute component={OrderStatus} roles={["user"]} />
            }
          />
          <Route
            path="/drivers/accept_ride/:rideId"
            element={
              <ProtectedRoute component={RideAccepted} roles={["driver"]} />
            }
          />
          <Route
            path="/drivers/dashboard"
            element={
              <ProtectedRoute component={DriverDashboard} roles={["driver"]} />
            }
          />
          <Route
            path="/drivers/decline_ride/:rideId"
            element={
              <ProtectedRoute component={DeclineRide} roles={["driver"]} />
            }
          />
          <Route path="/unauthorized" element={<Unauthorized />} />
        </Routes>
      </UserProvider>
    </Router>
  );
};

export default App;
