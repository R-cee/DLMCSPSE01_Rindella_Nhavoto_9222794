import React, { useState, useEffect } from 'react';
import './Notifications.css';
import HostHeader from './HostHeader';

const Notifications = () => {
  const [notifications, setNotifications] = useState([]);
  const [error, setError] = useState(null);
  const [userRole, setUserRole] = useState('');

  useEffect(() => {
    const fetchUserRole = () => {
      const user = JSON.parse(localStorage.getItem('user'));
      if (user && user.role) {
        setUserRole(user.role); 
      }
    };
    
    fetchUserRole();
    fetchNotifications();
  }, []);

  const fetchNotifications = async () => {
    try {
      const token = localStorage.getItem('jwt_token');
      const response = await fetch('/notifications', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setNotifications(data.notifications);
        markNotificationsAsRead(); 
      } else {
        setError('Failed to fetch notifications');
      }
    } catch (error) {
      setError('Error fetching notifications');
    }
  };

  const markNotificationsAsRead = async () => {
    try {
      const token = localStorage.getItem('jwt_token');
      await fetch('/notifications/mark-as-read', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
    } catch (error) {
      setError('Failed to mark notifications as read');
    }
  };

  return (
    <div className="notifications-container">
      {userRole && userRole === 'EventHost' && <HostHeader />}
      <h2>Notifications</h2>
      {error && <p className="error">{error}</p>}
      <table className="notifications-table">
        <thead>
          <tr>
            <th>Message</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          {notifications.length > 0 ? (
            notifications.map((notification, index) => (
              <tr 
                key={index} 
                className={notification.is_read ? "notification-item read" : "notification-item unread"}
              >
                <td>{notification.message}</td>
                <td>{new Date(notification.created_at).toLocaleString()}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="3">No notifications available.</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default Notifications;
