import React, { useState, createContext } from 'react'

export const UserContext = createContext()


export const UserProvider = ({ children }) => {
    const[user, setUser] = useState({
        isAuthenticated : false,
        role : ''
    })
    const login = (userData) => {
        setUser({
            isAuthenticated : true, 
            ...userData
        })
    }
    const logout = () =>{
        setUser({
            isAuthenticated : false, 
            role : ''
        })
    }
    return (
        <UserContext.Provider value = {{ user, login, logout}}>
            {children}
        </UserContext.Provider>
    )
 }

