import React, { createContext, useState, useEffect } from 'react';
import authenticationService from '../services/auth/AuthenticationService';

// used to store auth state and methods across component tree
// context object can be accessed by calling useContext(AuthContext)
export const AuthContext = createContext(undefined);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);

    useEffect(() => {
        // check for stored user in local storage
        const user = localStorage.getItem('user');
        if (user) {
            setUser(JSON.parse(user));
        }
    }, []);

    const register = async (registrationData) => {
        const response = await authenticationService.register(registrationData);
        setUser(response);
        localStorage.setItem('user', JSON.stringify(response));
    };

    const login = async (username, password) => {
        const response = await authenticationService.login(username, password);
        setUser(response);
        localStorage.setItem('user', JSON.stringify(response));
    };

    const logout = () => {
        authenticationService.logout();
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, setUser, register, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};
