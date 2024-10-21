import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './HostEventsPage.css';
import HostHeader from './HostHeader';

const HostEventsPage = () => {
  const [events, setEvents] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const token = localStorage.getItem('jwt_token');
        const response = await fetch('/host-events', {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });
        
        if (response.ok) {
          const data = await response.json();
          setEvents(data);
        } else {
          console.error('Failed to fetch events');
        }
      } catch (error) {
        console.error('Error fetching events:', error);
      }
    };

    fetchEvents();
  }, []);

  const handleCardClick = (event) => {
    navigate(`/edit-event/${event.event_id}`, { state: { event } });
  };

  return (
    <div className="host-events-page">
      <HostHeader />
      <h2>My Events</h2>
      {events.length === 0 ? (
        <div className="no-events">
          <p>No Events to Display</p>
        </div>
      ) : (
        <ul className="events-list">
          {events.map((event) => (
            <li key={event.event_id} className="event-item" onClick={() => handleCardClick(event)}>
              <img src={`/event_images/${event.event_poster}`} alt={event.event_name} className="event-poster" />
              <h2>{event.event_name}</h2>
              <p>{event.event_location}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default HostEventsPage;
