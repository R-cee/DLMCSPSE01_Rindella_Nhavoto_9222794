import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './HostDashboardPage.css';
import Header from './HostHeader';

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
    toast.success('Event created successfully!', {
      position: toast.POSITION.TOP_RIGHT,
      autoClose: 3000,
      onClose: () => navigate('/landing')
    });
  };

  const handleGetStarted = () => {
    const token = localStorage.getItem('jwt_token');
    fetch('/api/vetting', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
      }
    }).then((response) => {
      if (response.ok) {
        toast.success('Vetting process started successfully!', {
          position: toast.POSITION.TOP_RIGHT,
          autoClose: 3000, 
          onClose: () => navigate('/landing') 
        });
      } else {
        toast.error('Vetting process failed. Please try again.', {
          position: toast.POSITION.TOP_RIGHT,
          autoClose: 3000
        });
      }
    }).catch((error) => {
      toast.error('An error occurred. Please try again.', {
        position: toast.POSITION.TOP_RIGHT,
        autoClose: 3000
      });
    });
  };

  const handleViewEvents = () => {
    navigate('/host-events');
  };

  return (
    <div className="host-dashboard">
      <ToastContainer />
      <Header />
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
