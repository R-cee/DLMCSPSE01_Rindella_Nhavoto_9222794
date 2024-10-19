import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { loadStripe } from '@stripe/stripe-js';
import { Elements } from '@stripe/react-stripe-js';
import CheckoutForm from './CheckoutForm';
import AttendeeHeader from './AttendeeHeader';
import './LandingPage.css';

const stripePromise = loadStripe('pk_test_123pol');

const jwtToken = localStorage.getItem('jwt_token');

const LandingPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const username = location.state?.username || 'Guest';

  const [countries, setCountries] = useState([]);
  const [locations, setLocations] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCountry, setSelectedCountry] = useState('');
  const [selectedLocation, setSelectedLocation] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [events, setEvents] = useState([]);
  const [flippedEvents, setFlippedEvents] = useState({});
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [likedEvents, setLikedEvents] = useState({});

  useEffect(() => {
    const fetchCountries = async () => {
      try {
        const response = await fetch('/events/countries');
        const data = await response.json();
        setCountries(data);
      } catch (error) {
        console.error('Error fetching countries:', error);
      }
    };

    fetchCountries();
  }, []);

  useEffect(() => {
    if (selectedCountry) {
      const fetchFilters = async () => {
        try {
          const response = await fetch(`/events/filters?country=${selectedCountry}`);
          const data = await response.json();
          setLocations(data.locations);
          setCategories(data.categories);
        } catch (error) {
          console.error('Error fetching filters:', error);
        }
      };
      fetchFilters();
    }
  }, [selectedCountry]);

  useEffect(() => {
    if (selectedCountry) {
      const fetchEvents = async () => {
        try {
          const url = `/events?country=${selectedCountry}&location=${selectedLocation}&category=${selectedCategory}&status=Approved`;
          const response = await fetch(url);
          const data = await response.json();

          const currentDate = new Date();
          const upcomingEvents = data.filter((event) => new Date(event.event_date) > currentDate);

          setEvents(upcomingEvents);
        } catch (error) {
          console.error('Error fetching events:', error);
        }
      };
      fetchEvents();
    }
  }, [selectedCountry, selectedLocation, selectedCategory]);

  const handleCountryChange = (e) => {
    setSelectedCountry(e.target.value);
    setSelectedLocation(''); 
    setSelectedCategory(''); 
  };

  const handleLocationChange = (e) => {
    setSelectedLocation(e.target.value);
  };

  const handleCategoryChange = (e) => {
    setSelectedCategory(e.target.value);
  };

  const handleEventClick = (e, event_id) => {
    if (
      e.target.classList.contains('booking-dropdown') ||
      e.target.classList.contains('proceed-button') ||
      e.target.classList.contains('like-button') ||
      e.target.classList.contains('settings-dropdown')
    ) {
      return;
    }

    setFlippedEvents((prev) => ({
      ...prev,
      [event_id]: !prev[event_id],
    }));
  };

  const handlePaymentMethodChange = async (event, paymentMethod) => {
    setSelectedEvent(event);
    if (paymentMethod === 'stripe') {
      navigate(`/checkout`, {
        state: { event, method: 'stripe' },
        headers: {
          Authorization: `Bearer ${jwtToken}`,
        },
      });
    }
  };

  const handleLikeClick = async (event_id) => {
    const isLiked = likedEvents[event_id];

    try {
      const response = await fetch(`/events/${event_id}/like`, {
        method: isLiked ? 'DELETE' : 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${jwtToken}`, 
        },
        body: JSON.stringify({ user_id: location.state.user_id }),
      });

      if (response.ok) {
        setLikedEvents((prev) => ({
          ...prev,
          [event_id]: !isLiked,
        }));
      } else {
        console.error(isLiked ? 'Failed to unlike the event' : 'Failed to like the event');
      }
    } catch (error) {
      console.error(isLiked ? 'Error unliking event:' : 'Error liking event:', error);
    }
  };

  return (
    <div className="landing-page">
     <AttendeeHeader />
      <div className="content">
        <h1>Welcome, {username}!</h1>
        <p>Select a Country to View Events:</p>
        <div className="filters">
          <select onChange={handleCountryChange} value={selectedCountry}>
            <option value="">Select Country</option>
            {countries.map((country, index) => (
              <option key={index} value={country}>{country}</option>
            ))}
          </select>

          {selectedCountry && (
            <>
              <select onChange={handleLocationChange} value={selectedLocation}>
                <option value="">Select Location</option>
                {locations.map((location, index) => (
                  <option key={index} value={location}>{location}</option>
                ))}
              </select>

              <select onChange={handleCategoryChange} value={selectedCategory}>
                <option value="">Select Category</option>
                {categories.map((category, index) => (
                  <option key={index} value={category}>{category}</option>
                ))}
              </select>
            </>
          )}
        </div>

        {events.length > 0 ? (
          <div className="events-container">
            {events.map((event) => (
              <div
                key={event.event_id}
                className={`event-card ${flippedEvents[event.event_id] ? 'flipped' : ''}`}
                onClick={(e) => handleEventClick(e, event.event_id)}
              >
                <div className="event-card-inner">
                  {}
                  <div className="event-card-front">
                    <img
                      src={`/event_images/${event.event_poster}`}
                      alt={event.event_name}
                      className="event-poster"
                    />
                    <div className="event-details">
                      <h3>{event.event_name}</h3>
                      <p><strong>Date:</strong> {new Date(event.event_date).toLocaleString()}</p>
                      <p><strong>Location:</strong> {event.event_location}</p>
                    </div>
                  </div>

                  <div className="event-card-back">
                    <h3>{event.event_name}</h3>
                    <p><strong>Description:</strong> {event.event_description}</p>
                    <p><strong>Price:</strong> ${event.event_price}</p>
                    <p><strong>Tickets Remaining:</strong> {event.event_capacity} tickets</p>

                    <select
                      className="booking-dropdown"
                      onClick={(e) => e.stopPropagation()}
                      onChange={(e) => handlePaymentMethodChange(event, e.target.value)}
                      defaultValue=""
                    >
                      <option value="" disabled>Buy Tickets</option>
                      <option value="stripe">Card Payment</option>
                    </select>

                    <button
                      className="like-button"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleLikeClick(event.event_id);
                      }}
                    >
                      {likedEvents[event.event_id] ? 'Unlike' : 'Like'}
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          selectedCountry && <p>No approved events available for the selected filters.</p>
        )}
      </div>

      {selectedEvent && (
        <Elements stripe={stripePromise}>
          <CheckoutForm event={selectedEvent} />
        </Elements>
      )}
    </div>
  );
};

export default LandingPage;
