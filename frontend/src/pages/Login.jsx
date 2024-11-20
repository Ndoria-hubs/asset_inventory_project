import React, { useState } from "react";
import { useDispatch } from "react-redux";
import { Link, useNavigate } from "react-router-dom";
import { setUser } from "../features/auth/authSlice";
import api from "../services/api";
import styles from "./Login.module.css";
import logo from "../assets/login-photo.jpeg";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.get("/Users");
      const user = response.data.find(
        (u) => u.username === username && u.password === password
      );

      if (user) {
        dispatch(setUser({ user, token: "mockToken" }));
        if (user.role === "Admin") {
          navigate("/admin-dashboard");
        } else if (user.role === "Procurement Manager") {
          navigate("/manager-dashboard");
        } else {
          navigate("/user-dashboard");
        }
      } else {
        alert("Invalid username or password");
      }
    } catch (error) {
      console.error("Login failed:", error);
      alert("An error occurred while trying to log in.");
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.left}>
        <img src={logo} alt="Maze Background" className={styles.image} />
      </div>
      <div className={styles.right}>
        <form onSubmit={handleSubmit} className={styles.form}>
          <h1>Welcome. Let's get started!</h1>
          <div className={styles.inputGroup}>
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div className={styles.inputGroup}>
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit" className={styles.loginButton}>
            Login
          </button>

          <label className={styles.checkboxContainer}>
            <input type="checkbox" name="_remember_me" />
            remember me
          </label>
        </form>
      </div>
    </div>
  );
}

export default Login;
