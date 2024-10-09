import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './LoginForm.css';

const LoginForm = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    remember: false,
  });

  const [errors, setErrors] = useState({});
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
  
    try {
      const response = await fetch('/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
  
      if (response.ok) {
        const data = await response.json();
  
        localStorage.setItem('jwt_token', data.access_token);
  
        localStorage.setItem('role', data.role);
  
        console.log('User role stored in localStorage:', data.role); 
  
        navigate(data.redirect, { state: { username: data.username } });
      } else {
        const data = await response.json();
        setErrors({ form: data.errors || 'Invalid username or password' });
      }
    } catch (error) {
      console.error('Error:', error);
      setErrors({ form: 'An error occurred. Please try again later.' });
    }
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Username:</label>
          <input
            type="text"
            name="username"
            value={formData.username}
            onChange={handleChange}
            placeholder="Enter your username"
            required
          />
          {errors.username && <p>{errors.username}</p>}
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            placeholder="Enter your password"
            required
          />
          {errors.password && <p>{errors.password}</p>}
        </div>
        <div>
          <label>
            <input
              type="checkbox"
              name="remember"
              checked={formData.remember}
              onChange={handleChange}
            />
            Remember Me
          </label>
        </div>
        {errors.form && <p className="error-message">{errors.form}</p>}
        <button type="submit">Login</button>
      </form>
      <p>
        Don't have an account? <a href="/register">Register here</a>.
      </p>
    </div>
  );
};

export default LoginForm;
