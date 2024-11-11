// src/pages/Login.js
import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { Link } from 'react-router-dom';
import { setUser } from '../features/auth/authSlice';
import api from '../services/api';
import styles from './Login.module.css';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const dispatch = useDispatch();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.get('/Users');
      const user = response.data.find(
        (u) => u.username === username && u.password === password
      );

      if (user) {
        dispatch(setUser({ user, token: 'mockToken' }));

        if (user.role === 'Admin') {
          window.location.href = '/admin-dashboard';
        } else if (user.role === 'Procurement Manager') {
          window.location.href = '/manager-dashboard';
        } else {
          window.location.href = '/user-dashboard';
        }

        alert("Login successful");
      } else {
        alert("Invalid username or password");
      }
    } catch (error) {
      console.error("Login failed:", error);
      alert("An error occurred while trying to log in.");
    }
  };

  return (
    <div className={styles['login-container']}>
      <div className={styles.wrapper}>
        <div className={`${styles['form-wrapper']} ${styles['sign-in']}`}>
          <form onSubmit={handleSubmit}>
            {/* Added "Asset Maze" Title */}
            <h1 className={styles['main-title']}>Asset Maze</h1>
            <h2>Login</h2>
            <div className={styles['input-group']}>
              <input
                type="text"
                required
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
              <label>Username</label>
            </div>
            <div className={styles['input-group']}>
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <label>Password</label>
            </div>
            <div className={styles.rememder}>
              <label><input type="checkbox" /> Remember me</label>
            </div>
            <button type="submit" className={styles['login-button']}>Login</button>
            <div className={styles['signup-link']}>
              <p>Don't have an account? <Link to="/signup" className={styles['signupbtn-link']}>Sign up</Link></p>
            </div>
            <Link to="/" className={styles['home-button']}>Back to Home</Link>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Login;
