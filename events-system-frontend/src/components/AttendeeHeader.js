import React from 'react';
import { useNavigate } from 'react-router-dom';
import './AttendeeHeader.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBell } from '@fortawesome/free-solid-svg-icons';

const Header = () => {
  const navigate = useNavigate();

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
            <button className="notification-button" onClick={() => navigate('/notifications')}>
              <FontAwesomeIcon icon={faBell} />
            </button>
          </li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;
