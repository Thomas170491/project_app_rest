import React, { createContext, useContext, useState } from 'react';
import axiosInstance from './axiosInstance';
import { jwtDecode } from "jwt-decode";

export const UserContext = createContext();

export const UserProvider = ({ children }) => {
  const [user, setUser] = useState(null);

    const login = async (token) => {
    try {
      const decodedToken = jwtDecode(token);
      const username = decodedToken.username;
      console.log('Decoded username:', username); // Debug log
      setUser({ username });
      console.log('User :',{user})
      axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    } catch (error) {
      console.error("Login failed:", error);
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
