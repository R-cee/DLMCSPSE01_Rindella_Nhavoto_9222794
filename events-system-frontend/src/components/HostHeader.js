import React from 'react';
import { useNavigate } from 'react-router-dom';
import './HostHeader.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBell } from '@fortawesome/free-solid-svg-icons';

const Header = () => {
  const navigate = useNavigate();

  return (
    <header className="header">
      <nav className="nav-links">
      <ul>
            <li><button onClick={()=> navigate('/login')}>Logout</button></li>
            <li>
              <div className="settings-dropdown">
                <button>Profile</button>
                <div className="dropdown-content">
                  <button onClick={() => navigate('')}>Change Password</button>
                  <button onClick={() => navigate('')}>Payment Account</button>
                  <button onClick={() => navigate('/host/reports')}>Reports</button>
                </div>
              </div>
            </li>
            <li><button onClick={()=> navigate('/host-dashboard')}>Home</button></li>
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
