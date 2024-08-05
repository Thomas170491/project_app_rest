import React from "react";
import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import DriverDashboard from "./components/DriverDashboard";
import Home from "./components/Home";
import Location from "./components/Location";
import Navbar from "./components/Navbar";
import Notification from "./components/Notification";
import OrderRide from "./components/OrderRide";
import Pay from "./components/Pay";
import { ProtectedRoute, PublicRoute } from "./components/ProtectedRoute";
import { UserProvider } from "./components/UserContext";
import Dashboard from "./components/UserDashboard";
import UserLogin from "./components/UserLogin";

import "./App.css";
import Unauthorized from "./components/Unauthorized";

function App() {
  return (
    <Router>
      <UserProvider>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route
            path="/users/login"
            element={
              <PublicRoute>
                <UserLogin />
              </PublicRoute>
            }
          />
          <Route
            path="/users/dashboard"
            element={
              <ProtectedRoute role={"customer"}>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/users/order_ride"
            element={
              <ProtectedRoute role={"customer"}>
                <OrderRide />
              </ProtectedRoute>
            }
          />
          <Route
            path="/notification"
            element={
              <ProtectedRoute>
                <Notification />
              </ProtectedRoute>
            }
          />
          <Route
            path="/share-location"
            element={
              <ProtectedRoute>
                <Location />
              </ProtectedRoute>
            }
          />
          <Route
            path="/users/payment"
            element={
              <ProtectedRoute role={"customer"}>
                <Pay />
              </ProtectedRoute>
            }
          />
          <Route
            path="/drivers/dashboard"
            element={
              <ProtectedRoute role={"driver"}>
                <DriverDashboard />
              </ProtectedRoute>
            }
          />
          <Route path="/unauthorized" element={<Unauthorized />} />
        </Routes>
      </UserProvider>
    </Router>
  );
}

export default App;
