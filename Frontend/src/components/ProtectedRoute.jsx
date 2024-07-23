
import React, { useContext } from 'react';
import { Navigate } from 'react-router-dom';
import { UserContext } from './UserContext';

const ProtectedRoute = ({ element, requiredRole }) => {
  const { user } = useContext(UserContext);

  const isAuthenticated = user.isAuthenticated;
  const hasRole = requiredRole ? user.role === requiredRole : true;

  if (!isAuthenticated || user.role === "") {
    return <Navigate to="/users/login" />;
  }

  if (requiredRole && !hasRole ) {
    return <Navigate to="/" />;
  }

  return element;
};

export default ProtectedRoute;
