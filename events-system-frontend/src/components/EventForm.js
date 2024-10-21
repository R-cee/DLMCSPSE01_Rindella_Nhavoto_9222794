import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import './EventForm.css';
import HostHeader from './HostHeader';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const EventForm = () => {
  const { event_id } = useParams();
  const navigate = useNavigate();
  const mode = event_id ? 'edit' : 'create';

  const [formData, setFormData] = useState({
    event_name: '',
    event_description: '',
    event_country: '',
    event_location: '',
    event_date: '',
    event_price: '',
    event_capacity: '',
    event_poster: '',
    event_category: '',
    custom_category: '',
  });

  const [isEditable, setIsEditable] = useState(mode === 'create');
  const [errors, setErrors] = useState({});
  const [success, setSuccess] = useState(false);
  const [userRole, setUserRole] = useState('');

  useEffect(() => {
    const role = localStorage.getItem('role');
    setUserRole(role);
  }, []);

  useEffect(() => {
    if (mode === 'edit') {
      const fetchEvent = async () => {
        try {
          const token = localStorage.getItem('jwt_token');
          const response = await fetch(`/edit-event/${event_id}`, {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
          if (response.ok) {
            const eventData = await response.json();
            setFormData(eventData);
            setIsEditable(false);
          } else {
            console.error('Failed to fetch event data');
          }
        } catch (error) {
          console.error('Error fetching event:', error);
        }
      };

      fetchEvent();
    }
  }, [event_id, mode]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleFileChange = (e) => {
    setFormData({
      ...formData,
      event_poster: e.target.files[0] || formData.event_poster,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
  
    const formDataToSend = new FormData();
    for (let key in formData) {
      if (key === 'event_poster' && formData[key] instanceof File) {
        formDataToSend.append(key, formData[key]); 
      } else {
        formDataToSend.append(key, formData[key]);
      }
    }

    const url = mode === 'create' ? '/create-event' : `/update-event/${event_id}`;
    try {
      const token = localStorage.getItem('jwt_token');
  
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formDataToSend,
      });
      
      if (response.ok) {
        setSuccess(true);
  
        toast.success('Event created/updated successfully!', {
          position: toast.POSITION.TOP_RIGHT,
          autoClose: 3000,
          onClose: () => {
            if (userRole === 'EventHost') {
              navigate('/host-dashboard'); 
            }
          }
        });
      } else {
        const data = await response.json();
        setErrors(data.errors || {});
  
        toast.error('Failed to create/update event. Please try again.', {
          position: toast.POSITION.TOP_RIGHT,
          autoClose: 5000,
        });
  
        console.error('Server returned an error:', data);
      }
    } catch (error) {
      toast.error('An error occurred while creating/updating the event. Please check your connection and try again.', {
        position: toast.POSITION.TOP_RIGHT,
        autoClose: 5000,
      });
      
      console.error('Error:', error);
    }
  };

  const handleEditClick = (e) => {
    e.preventDefault(); 
    setIsEditable(true);
  };

  return (
    <div className="event-form-container">
     {userRole === 'EventHost' && <HostHeader />}
     <ToastContainer />

      <h2>{mode === 'create' ? 'Create New Event' : 'View/Edit Event'}</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Event Name:</label>
          <input
            type="text"
            name="event_name"
            value={formData.event_name}
            onChange={handleChange}
            required
            disabled={!isEditable}
          />
        </div>
        <div className="form-group">
          <label>Event Description:</label>
          <textarea
            name="event_description"
            value={formData.event_description}
            onChange={handleChange}
            rows="4"
            required
            disabled={!isEditable}
          />
        </div>
        <div className="form-group">
          <label>Event Country:</label>
          <input
            type="text"
            name="event_country"
            value={formData.event_country}
            onChange={handleChange}
            required
            disabled={!isEditable}
          />
        </div>
        <div className="form-group">
          <label>Event Location:</label>
          <input
            type="text"
            name="event_location"
            value={formData.event_location}
            onChange={handleChange}
            required
            disabled={!isEditable}
          />
        </div>
        <div className="form-group">
          <label>Event Date:</label>
          <input
            type="datetime-local"
            name="event_date"
            value={formData.event_date}
            onChange={handleChange}
            required
            disabled={!isEditable}
            min={new Date().toISOString().slice(0, 16)}
          />
        </div>
        <div className="form-group">
          <label>Event Price:</label>
          <input
            type="number"
            name="event_price"
            value={formData.event_price}
            onChange={handleChange}
            required
            disabled={!isEditable}
          />
        </div>
        <div className="form-group">
          <label>Event Capacity:</label>
          <input
            type="number"
            name="event_capacity"
            value={formData.event_capacity}
            onChange={handleChange}
            required
            disabled={!isEditable}
          />
        </div>
        <div className="form-group">
          <label>Event Category:</label>
          <select
            name="event_category"
            value={formData.event_category}
            onChange={handleChange}
            required
            disabled={!isEditable}
          >
            <option value="">Select Category</option>
            <option value="Music">Music</option>
            <option value="Sports">Sports</option>
            <option value="Education">Education</option>
            <option value="Culture">Culture</option>
            <option value="Arts">Arts</option>
            <option value="Food">Food</option>
            <option value="Travel">Travel</option>
            <option value="Other">Other</option>
          </select>
        </div>
        {formData.event_category === 'Other' && (
          <div className="form-group">
            <label>Custom Category:</label>
            <input
              type="text"
              name="custom_category"
              value={formData.custom_category}
              onChange={handleChange}
              required
              disabled={!isEditable}
            />
          </div>
        )}
        <div className="form-group">
          <label>Event Poster:</label>
          <input
            type="file"
            name="event_poster"
            onChange={handleFileChange}
            disabled={!isEditable}
          />
        </div>
        {mode === 'edit' && !isEditable ? (
          <button type="button" onClick={handleEditClick}>
            Edit
          </button>
        ) : (
          <button type="submit">{mode === 'create' ? 'Submit' : 'Update Event'}</button>
        )}
      </form>
    </div>
  );
};

export default EventForm;
