import React, { useState, useEffect } from 'react';
import './ChangePasswordForm.css';
import AttendeeHeader from './AttendeeHeader';
import HostHeader from './HostHeader';
import AdminHeader from './AdminHeader';  

const ChangePasswordForm = () => {
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [message, setMessage] = useState('');
  const [userRole, setUserRole] = useState('');

  useEffect(() => {
    const role = localStorage.getItem('role');
    if (role) {
      setUserRole(role);
    }
  }, []);

  const handleChangePassword = async (e) => {
    e.preventDefault();

    if (newPassword !== confirmPassword) {
      setMessage('New passwords do not match.');
      return;
    }

    try {
      const token = localStorage.getItem('jwt_token');
      const response = await fetch('/change-password', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ old_password: oldPassword, new_password: newPassword }),
      });

      if (response.ok) {
        setMessage('Password changed successfully.');
      } else {
        setMessage('Failed to change password.');
      }
    } catch (error) {
      console.error('Error changing password:', error);
      setMessage('An error occurred.');
    }
  };

  return (
    <div className="change-password-page">
      {userRole && userRole.toLowerCase() === 'attendee' && <AttendeeHeader />}
      {userRole && userRole.toLowerCase() === 'eventhost' && <HostHeader />}
      {userRole && userRole.toLowerCase() === 'admin' && <AdminHeader />}
           
      <h1>Change Password</h1>
      <form onSubmit={handleChangePassword} className="change-password-form">
        <div className="form-group">
          <label>Old Password:</label>
          <input
            type="password"
            value={oldPassword}
            onChange={(e) => setOldPassword(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label>New Password:</label>
          <input
            type="password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label>Confirm New Password:</label>
          <input
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Change Password</button>
        {message && <p className="message">{message}</p>}
      </form>
    </div>
  );
};

export default ChangePasswordForm;
