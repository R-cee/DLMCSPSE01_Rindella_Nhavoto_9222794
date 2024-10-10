import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './AdminDashboardPage.css';
import AdminHeader from './AdminHeader';

const AdminDashboardPage = () => {
  const [counters, setCounters] = useState({ pending: 0, approved: 0, rejected: 0 });
  const [profiles, setProfiles] = useState([]);
  const [selectedStatus, setSelectedStatus] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchCounters = async () => {
      try {
        const token = localStorage.getItem('jwt_token');
        const response = await fetch('/api/admin/profile-counters', {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });
        if (response.ok) {
          const data = await response.json();
          setCounters(data);
        } else {
          console.error('Failed to fetch profile counters');
        }
      } catch (error) {
        console.error('Error fetching profile counters:', error);
      }
    };

    fetchCounters();
  }, []);

  const handleStatusClick = async (status) => {
    setSelectedStatus(status);
    try {
      const token = localStorage.getItem('jwt_token'); 
      const response = await fetch(`/api/admin/profiles?status=${status}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setProfiles(data);
      } else {
        console.error(`Failed to fetch ${status} profiles`);
      }
    } catch (error) {
      console.error(`Error fetching ${status} profiles:`, error);
    }
  };

  const handleProfileClick = (profile) => {
    navigate(`/admin/vetting/${profile.user_id}`, { state: { profile, isAdmin: true } });
  };

  const handleManageUsers = () => {
    navigate('/admin/manage-users');
  };

  const handleManageEvents = () => {
    navigate('/admin/manage-events');
  };

  const handleCreateAdmin = () => {
    navigate('/admin/create-admin');
  };

  const handleViewLogs = () => {
    navigate('/admin/view-logs');
  };

  const handleLogout = () => {
    navigate('/login');
  };

  return (
    <div className="admin-dashboard">
      <AdminHeader />

      <div className="content">
        <h1>Admin Dashboard</h1>
        <h2>Profile Status</h2>
        <div className="counters">
          <div className="counter" onClick={() => handleStatusClick('Pending')}>
            <h3>Pending</h3>
            <p>{counters.pending}</p>
          </div>
          <div className="counter" onClick={() => handleStatusClick('Approved')}>
            <h3>Approved</h3>
            <p>{counters.approved}</p>
          </div>
          <div className="counter" onClick={() => handleStatusClick('Rejected')}>
            <h3>Rejected</h3>
            <p>{counters.rejected}</p>
          </div>
        </div>

        <div className="actions">
          <button className="manage-users-button" onClick={handleManageUsers}>Manage Users</button>
          <button className="manage-profiles-button" onClick={handleManageEvents}>Manage Events</button>
          <button className="create-admin-button" onClick={handleCreateAdmin}>Create Admin</button>
          <button className="view-logs-button" onClick={handleViewLogs}>View Logs</button>
        </div>

        {selectedStatus && (
          <div className="profiles-list">
            <h2>{selectedStatus} Profiles</h2>
            {profiles.length === 0 ? (
              <p>No profiles to display.</p>
            ) : (
              <ul>
                {profiles.map(profile => (
                  <li key={profile.user_id} onClick={() => handleProfileClick(profile)}>
                    <span>{profile.username}</span> - <span>{profile.first_name} {profile.last_name}</span> - <span>{profile.host_type}</span>
                  </li>
                ))}
              </ul>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminDashboardPage;
