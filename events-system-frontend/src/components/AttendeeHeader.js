import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './AttendeeHeader.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBell } from '@fortawesome/free-solid-svg-icons';

const AttendeeHeader = () => {
  const navigate = useNavigate();
  const [unreadCount, setUnreadCount] = useState(0);

  useEffect(() => {
    const fetchUnreadNotifications = async () => {
      try {
        const token = localStorage.getItem('jwt_token');
        const response = await fetch('/notifications/unread-count', {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });

        if (response.ok) {
          const data = await response.json();
          setUnreadCount(data.unread_count);
        } else {
          console.error('Failed to fetch unread notifications count');
        }
      } catch (error) {
        console.error('Error fetching unread notifications count:', error);
      }
    };

    fetchUnreadNotifications();
  }, []);

  return (
    <header className="header">
      <nav className="nav-links">
        <ul>
          <li><button onClick={() => navigate('/login')}>Logout</button></li>
          <li>
            <div className="settings-dropdown">
              <button>Profile</button>
              <div className="dropdown-content">
                <button onClick={() => navigate('/change-password')}>Change Password</button>
                <button onClick={() => navigate('/view-proof-of-payment')}>View Proof of Payment</button>
              </div>
            </div>
          </li>
          <li><button onClick={() => navigate('/my-events')}>My Events</button></li>
          <li><button onClick={() => navigate('/landing')}>Home</button></li>
          <li>
            <button
              className={`notification-button ${unreadCount > 0 ? 'glow' : ''}`}
              onClick={() => navigate('/attendee-notifications')}
            >
              <FontAwesomeIcon icon={faBell} />
              {unreadCount > 0 && <span className="notification-badge">{unreadCount}</span>}
            </button>
          </li>
        </ul>
      </nav>
    </header>
  );
};

export default AttendeeHeader;
