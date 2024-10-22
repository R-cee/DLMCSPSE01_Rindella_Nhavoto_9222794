import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import './HostDashboardPage.css';
import HostHeader from './HostHeader';

const HostDashboardPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const username = location.state?.username || "EventHost";

  const [profileStatus, setProfileStatus] = useState(null);

  useEffect(() => {
    const fetchProfileStatus = async () => {
      try {
        const token = localStorage.getItem('jwt_token'); 
  
        const response = await fetch('/api/profile-status', {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });
  
        if (response.ok) {
          const data = await response.json();
          setProfileStatus(data.status);
        } else {
          console.error('Failed to fetch profile status');
        }
      } catch (error) {
        console.error('Error fetching profile status:', error);
      }
    };
  
    fetchProfileStatus();
  }, []);

  const handleCreateEvent = () => {
    navigate('/create-event');
  };

  const handleGetStarted = () => {
    const token = localStorage.getItem('jwt_token');
    
    fetch('/vetting', {
      method: 'GET',  // We're only fetching the empty form data here
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        console.error(data.error);  
      } else {
        navigate('/vetting', { state: { formData: data } });
      }
    })
    .catch(error => {
      console.error('Error fetching vetting form:', error);
    });
  };
  

  const handleViewEvents = () => {
    navigate('/host-events');
  };

  return (
    <div className="host-dashboard">
      <HostHeader />
      <div className="content">
        <h1>Welcome, {username}!</h1>
        {profileStatus === 'Pending' && (
          <p>Your profile is in the vetting process. Await approval to continue.</p>
        )}
        <button
          className="get-started-button"
          onClick={handleGetStarted}
          disabled={profileStatus === 'Pending' || profileStatus === 'Approved'} 
          style={profileStatus === 'Pending' || profileStatus === 'Approved' ? { backgroundColor: '#ccc', cursor: 'not-allowed' } : {}}
        >
          Get Started
        </button>
        <button
          className="create-event-button"
          onClick={handleCreateEvent}
          disabled={profileStatus !== 'Approved'}
          style={profileStatus !== 'Approved' ? { backgroundColor: '#ccc', cursor: 'not-allowed' } : {}}
        >
          <span>+</span> Publish Event
        </button>
        <button
          className="view-events-button"
          onClick={handleViewEvents}
          disabled={profileStatus !== 'Approved'} 
          style={profileStatus !== 'Approved' ? { backgroundColor: '#ccc', cursor: 'not-allowed' } : {}}
        >
          View My Events
        </button>
      </div>
    </div>
  );
};

export default HostDashboardPage;
