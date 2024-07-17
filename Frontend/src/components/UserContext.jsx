import React, { useState, createContext } from 'react'

export const UserContext = createContext()

export const UserProvider = ({ children }) => {
    const[user, setUser] = useState({
        isAuthenticated : true,
        role : 'admin'
    })
    const login = (role) => {
        setUser({
            isAuthenticated : true, role
        })
    }
    const logout = () =>{
        setUser({
            isAuthenticated : false, role : ' '
        })
    }
    return (
        <UserContext.Provider value = {{ user, login, logout}}>
            {children}
        </UserContext.Provider>
    )
 }