import React, { createContext, useContext, useState } from 'react';
import axiosInstance from './axiosInstance';

export const UserContext = createContext();

export const UserProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  const login = async ({ username, password }) => {
    try {
      const response = await axiosInstance.post('users/login', { username, password });
      const { access_token } = response.data;
      localStorage.setItem('access_token', access_token);
      setUser({ username });
      axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
    } catch (error) {
      console.error("Login failed:", error);
      // Handle login error (e.g., show a message to the user)
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    setUser(null);
    delete axiosInstance.defaults.headers.common['Authorization'];
  };

  return (
    <UserContext.Provider value={{ user, login, logout }}>
      {children}
    </UserContext.Provider>
  );
};

export const useUser = () => {
  return useContext(UserContext);
};
