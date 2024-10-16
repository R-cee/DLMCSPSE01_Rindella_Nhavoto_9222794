import React, { useState } from 'react';
import './AdminCreationForm.css';
import AdminHeader from './AdminHeader';
import { useNavigate } from 'react-router-dom';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const AdminCreationForm = () => {
  const [formData, setFormData] = useState({
    name: '',
    surname: '',
    phone_number: '',
    email: '',
    country: '',
    password: '',
    username: '',
  });

  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    try {
      const token = localStorage.getItem('jwt_token'); 
      const response = await fetch('/admin/create-admin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        toast.success('Admin created successfully!', {
          position: toast.POSITION.TOP_RIGHT,
          autoClose: 3000,
          onClose: () => navigate('/admin-dashboard'),
        });

        setFormData({
          name: '',
          surname: '',
          phone_number: '',
          email: '',
          country: '',
          password: '',
          username: '',
        });
      } else {
        const errorData = await response.json();
        setError(errorData.error);
        toast.error(`Error: ${errorData.error}`, { position: toast.POSITION.TOP_RIGHT });
      }
    } catch (error) {
      setError('Failed to create admin. Please try again later.');
      toast.error('Failed to create admin. Please try again later.', { position: toast.POSITION.TOP_RIGHT });
    }
  };

  return (
    <div className="admin-creation-form">
      <AdminHeader />
      <ToastContainer />
      <h1>Create Admin</h1>
      {error && <p className="error-message">{error}</p>}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Name:</label>
          <input type="text" name="name" value={formData.name} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>Surname:</label>
          <input type="text" name="surname" value={formData.surname} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>Phone Number:</label>
          <input type="text" name="phone_number" value={formData.phone_number} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>Email:</label>
          <input type="email" name="email" value={formData.email} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>Country:</label>
          <input type="text" name="country" value={formData.country} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>Username:</label>
          <input type="text" name="username" value={formData.username} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>Password:</label>
          <input type="password" name="password" value={formData.password} onChange={handleChange} required />
        </div>
        <button type="submit">Create Admin</button>
      </form>
    </div>
  );
};

export default AdminCreationForm;
