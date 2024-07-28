import React from "react";
import { Navigate } from "react-router-dom";

const ProtectedRoute = ({ children, role }) => {
  const token = localStorage.getItem("access_token");
  const user = localStorage.getItem("user");

  if (!user || !token) {
    return <Navigate to="/users/login" />;
  }

  // if (role && user.role !== role) {
  //   return <Navigate to="/unauthorized" />;
  // }

  return children;
};

export default ProtectedRoute;
