import React, { useState } from "react";
<<<<<<< HEAD
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
=======
import { loginUser } from "../services/api";
import styles from "./Login.module.css";
import { Link, useNavigate } from "react-router-dom";

function Login({ onLogin }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    const credentials = { email, password };
    const data = await loginUser(credentials);

    if (data.message) {
      setMessage(data.message);
    } else {
      setMessage("Login successful!");
      onLogin(data.user_id);

      const navigate = useNavigate();

      if (data.role === "admin") {
        navigate("/admin-dashboard");
      } else if (data.role === "manager") {
        navigate("/manager-dashboard");
      } else {
        navigate("/user-dashboard");
      }
>>>>>>> origin/victor
    }
  };

  return (
<<<<<<< HEAD
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
=======
    <div className={styles["login-container"]}>
      <div className={styles.wrapper}>
        <div className={`${styles["form-wrapper"]} ${styles["sign-in"]}`}>
          <form onSubmit={handleSubmit}>
            <h1 className={styles["main-title"]}>Asset Maze</h1>
            <h2>Login</h2>
            {message && <p>{message}</p>}
            <div className={styles["input-group"]}>
              <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
              <label>Email</label>
            </div>
            <div className={styles["input-group"]}>
              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
              <label>Password</label>
            </div>
            <div className={styles.rememder}>
              <label>
                <input type="checkbox" /> Remember me
              </label>
            </div>
            <button type="submit" className={styles["login-button"]}>
              Login
            </button>
            {message && <div>{message}</div>}
            <div className={styles["signup-link"]}>
              <p>
                Don't have an account?{" "}
                <Link to="/signup" className={styles["signupbtn-link"]}>
                  Sign up
                </Link>
              </p>
            </div>
            <Link to="/" className={styles["home-button"]}>
              Back to Home
            </Link>
          </form>
        </div>
>>>>>>> origin/victor
      </div>
    </div>
  );
}

export default Login;
