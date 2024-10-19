import React, { useState, useEffect } from 'react';
import './MyEvents.css';
import AdminHeader from './AdminHeader';

const MyEvents = () => {
  const [purchasedEvents, setPurchasedEvents] = useState([]);
  const [likedEvents, setLikedEvents] = useState([]);

  useEffect(() => {
    const fetchMyEvents = async () => {
      try {
        const token = localStorage.getItem('jwt_token');
        const response = await fetch('/api/my-events', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
        });

        if (response.ok) {
          const data = await response.json();
          setPurchasedEvents(data.purchased_events);
          setLikedEvents(data.liked_events);
        } else {
          console.error('Failed to fetch user events');
        }
      } catch (error) {
        console.error('Error fetching user events:', error);
      }
    };

    fetchMyEvents();
  }, []);

  return (
    <>
      <div className="my-events-page">
        <AdminHeader />
        <h2>Purchased Events</h2>
        {purchasedEvents.length > 0 ? (
          <div className="events-container">
            {purchasedEvents.map((event) => (
              <div key={event.event_id} className="event-card">
                <img src={`/event_images/${event.event_poster}`} alt={event.event_name} className="event-poster" />
                <div className="event-details">
                  <h3>{event.event_name}</h3>
                  <p><strong>Date:</strong> {new Date(event.event_date).toLocaleString()}</p>
                  <p><strong>Location:</strong> {event.event_location}</p>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p>No purchased events available.</p>
        )}

        <h2>Liked Events</h2>
        {likedEvents.length > 0 ? (
          <div className="events-container">
            {likedEvents.map((event) => (
              <div key={event.event_id} className="event-card">
                <img src={`/event_images/${event.event_poster}`} alt={event.event_name} className="event-poster" />
                <div className="event-details">
                  <h3>{event.event_name}</h3>
                  <p><strong>Date:</strong> {new Date(event.event_date).toLocaleString()}</p>
                  <p><strong>Location:</strong> {event.event_location}</p>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p>No liked events available.</p>
        )}
      </div>
    </>
  );
};

export default MyEvents;
