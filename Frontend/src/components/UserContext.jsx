import { jwtDecode } from "jwt-decode";
import React, { createContext, useContext, useState } from "react";
import axiosInstance from "./axiosInstance";

export const UserContext = createContext();

export const UserProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  const login = async (token) => {
    try {
      const decodedToken = jwtDecode(token);
      const username = decodedToken.username;
      console.log("Decoded username:", username); // Debug log
      // Update user state
      setUser({ username });
      // Using a callback to log the updated state
      setUser((prevUser) => {
        const updatedUser = { username };
        console.log("Updated user:", updatedUser); // Debug log after state update
        return updatedUser;
      });
      axiosInstance.defaults.headers.common[
        "Authorization"
      ] = `Bearer ${token}`;
    } catch (error) {
      console.error("Login failed:", error);
    }
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    setUser(null);
    delete axiosInstance.defaults.headers.common["Authorization"];
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
