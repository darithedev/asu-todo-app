'use client';

import { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext({});

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is logged in (check local storage for token)
    const token = localStorage.getItem('token');
    if (token) {
      // TODO: Validate token and get user info
    }
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    try {
      // TODO: Implement login logic
      // const response = await axios.post('/api/auth/login', { email, password });
      // setUser(response.data.user);
      // localStorage.setItem('token', response.data.token);
    } catch (error) {
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
