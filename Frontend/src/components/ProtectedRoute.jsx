import React from "react";
import { Navigate } from "react-router-dom";

export const ProtectedRoute = ({ children, role }) => {
  const token = localStorage.getItem("access_token");
  const user = JSON.parse(localStorage.getItem("user"));

  if (!user || !token) {
    return <Navigate to="/users/login" />;
  }

  if (role && user.role !== role) {
    return <Navigate to="/unauthorized" />;
  }

  return children;
};

export const PublicRoute = ({ children }) => {
  const token = localStorage.getItem("access_token");
  const user = JSON.parse(localStorage.getItem("user"));

  if (token) {
    // Redirect based on user role or a default page
    if (user && user.role === "admin") {
      return <Navigate to="/admin/dashboard" />;
    }
    if (user && user.role === "driver") {
      return <Navigate to="/drivers/dashboard" />;
    }
    return <Navigate to="/users/dashboard" />;
  }

  return children;
};
