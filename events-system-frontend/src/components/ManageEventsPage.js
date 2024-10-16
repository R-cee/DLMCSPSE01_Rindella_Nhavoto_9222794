import React, { useState, useEffect } from 'react';
import './ManageEventsPage.css';
import AdminHeader from './AdminHeader';

const ManageEventsPage = () => {
    const [events, setEvents] = useState([]);
    const [selectedEventId, setSelectedEventId] = useState(null);
    const [reason, setReason] = useState(''); 

    useEffect(() => {
        fetchEvents();
    }, []);

    const fetchEvents = async () => {
        try {
            const token = localStorage.getItem('jwt_token'); 
            const response = await fetch('/api/admin/events', {
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

    const updateEventStatus = async (eventId, status) => {
        const payload = { status };
        
        if (status === 'Rejected' && reason) {
            payload.reason = reason;
        }

        try {
            const token = localStorage.getItem('jwt_token'); 
            const response = await fetch(`/admin/event/update-status/${eventId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify(payload),
            });
            if (response.ok) {
                fetchEvents(); 
            } else {
                const data = await response.json();
                console.error('Error updating event status:', data);
                alert(`Failed to update event status: ${data.error}`);
            }
        } catch (error) {
            console.error('Error updating event status:', error);
        }
    };

    return (
        <div className="manage-events-page">
            <AdminHeader />
            <h2>Manage Events</h2>
            <div className="event-cards-container">
                {events.map((event) => (
                    <div key={event.event_id} className="event-card">
                        <img src={`/event_images/${event.event_poster}`} alt={event.event_name} />
                        <div className="event-info">
                            <h3>{event.event_name}</h3>
                            <p>{event.event_description}</p>
                            <p>{event.event_location}</p>
                            <p>{event.event_date}</p>
                            <p>Status: {event.event_status}</p>
                            <div className="action-buttons">
                                <button onClick={() => updateEventStatus(event.event_id, 'Approved')}>
                                    Approve
                                </button>
                                <button onClick={() => setSelectedEventId(event.event_id)}>
                                    Reject
                                </button>
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {selectedEventId && (
                <div className="reject-reason-container">
                    <h3>Reason for rejection:</h3>
                    <textarea
                        value={reason}
                        onChange={(e) => setReason(e.target.value)}
                        placeholder="State the reason for rejection"
                    />
                    <button
                        onClick={() => {
                            updateEventStatus(selectedEventId, 'Rejected');
                            setSelectedEventId(null); // Close the reason box after submitting
                            setReason('');
                        }}
                    >
                        Submit Rejection
                    </button>
                </div>
            )}
        </div>
    );
};

export default ManageEventsPage;
