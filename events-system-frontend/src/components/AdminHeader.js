import React from 'react';
import { useNavigate } from 'react-router-dom';
import './AttendeeHeader.css';

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
              </div>
            </div>
          </li>
          <li><button onClick={() => navigate('/admin-dashboard')}>Home</button></li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;
