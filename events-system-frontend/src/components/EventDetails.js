import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import './EventDetails.css';

const EventDetails = () => {
  const { event_id } = useParams(); 
  const [event, setEvent] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchEventDetails = async () => {
      try {
        const response = await fetch(`/api/events/${event_id}`);
        if (response.ok) {
          const data = await response.json();
          setEvent(data);
        } else {
          setError('Failed to fetch event details.');
        }
      } catch (error) {
        setError('An error occurred while fetching event details.');
      }
    };

    fetchEventDetails();
  }, [event_id]);

  if (error) {
    return <div className="error">{error}</div>;
  }

  if (!event) {
    return <div>Loading...</div>; 
  }

  return (
    <div className="event-details">
      <h1>{event.event_name}</h1>
      <p><strong>Description:</strong> {event.event_description}</p>
      <p><strong>Date:</strong> {new Date(event.event_date).toLocaleString()}</p>
      <p><strong>Location:</strong> {event.event_location}</p>
      <p><strong>Price:</strong> ${event.event_price}</p>
      <p><strong>Capacity:</strong> {event.event_capacity}</p>
      <p><strong>Category:</strong> {event.event_category}</p>
      <img src={`/event_images/${event.event_poster}`} alt={event.event_name} />
    </div>
  );
};

export default EventDetails;
