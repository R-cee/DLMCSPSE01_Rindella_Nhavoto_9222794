import React, { useState, useEffect } from 'react';
import './AttendeeNotifications.css';
import AttendeeHeader from './AttendeeHeader';

const Notifications = () => {
  const [notifications, setNotifications] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchNotifications();
  }, []);

  const fetchNotifications = async () => {
    try {
      const token = localStorage.getItem('jwt_token');
      if (!token) {
        setError('Authentication token is missing');
        return;
      }
  
      const response = await fetch('/attendee-notifications', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
  
      if (!response.ok) {
        const data = await response.json();
        setError(data.error || 'Failed to fetch notifications');
        console.error(`Error fetching notifications: ${data.error}`);
      } else {
        const data = await response.json();
        setNotifications(data.notifications);
      }
    } catch (error) {
      setError('An unexpected error occurred while fetching notifications.');
      console.error('Error:', error);
    }
  };

  return (
    <div className="notifications-container">
      <AttendeeHeader />
      <h2>Notifications</h2>
      {error && <p className="error">{error}</p>}
      <table className="notifications-table">
        <thead>
          <tr>
            <th>Message</th>
          </tr>
        </thead>
        <tbody>
        {notifications.length > 0 ? (
          notifications.map((notification, index) => (
            <tr key={index} className={notification.is_read ? "notification-item read" : "notification-item unread"}>
              <td>{notification.message}</td>
            </tr>
          ))
        ) : (
          <tr>
            <td colSpan="2">No notifications available.</td>
          </tr>
        )}
    </tbody>
      </table>
    </div>
  );
};

export default Notifications;
