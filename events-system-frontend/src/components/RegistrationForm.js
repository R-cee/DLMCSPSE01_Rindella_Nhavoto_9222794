import React, { useState } from 'react';
import Slideshow from './Slideshow'; 
import './RegistrationForm.css';  

const RegistrationForm = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    role: 'Attendee',
    password: ''
  });

  const [errors, setErrors] = useState({});
  const [success, setSuccess] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        setSuccess(true);
      } else {
        const data = await response.json();
        setErrors(data.errors || {});
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  if (success) {
    return <p>Registration successful! Please <a href="/login">login</a>.</p>;
  }

  return (
    <div className="registration-container">
      <Slideshow /> 
      <div className="form-container">
        <h2>Register</h2>
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
            <label>Email:</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="Enter your email"
              required
            />
            {errors.email && <p>{errors.email}</p>}
          </div>
          <div>
            <label>Role:</label>
            <select
              name="role"
              value={formData.role}
              onChange={handleChange}
              required
            >
              <option value="EventHost">Event Host</option>
              <option value="Attendee">Attendee</option>
            </select>
            {errors.role && <p>{errors.role}</p>}
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
          <button type="submit">Register</button>
        </form>
        <p>
        Have an account? <a href="/login">Login here</a>
      </p>
      </div>
    </div>
  );
};

export default RegistrationForm;
