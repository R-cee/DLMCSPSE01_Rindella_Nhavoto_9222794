import React, { useState, useEffect } from 'react';
import './AdminLogs.css';
import AdminHeader from './AdminHeader';

const AdminLogs = () => {
  const [logs, setLogs] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [actionFilter, setActionFilter] = useState('');
  const [usernameSearch, setUsernameSearch] = useState('');

  const fetchLogs = async () => {
    try {
      const token = localStorage.getItem('jwt_token');
      const response = await fetch(
        `/admin/view-logs?page=${page}&action=${actionFilter}&username=${usernameSearch}`,
        {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
        }
      );
      if (response.ok) {
        const data = await response.json();
        setLogs(data.interactions);
        setTotalPages(data.total_pages);
      } else {
        console.error('Failed to fetch logs');
      }
    } catch (error) {
      console.error('Error fetching logs:', error);
    }
  };

  useEffect(() => {
    fetchLogs();
  }, [page, actionFilter, usernameSearch]);

  const handlePageChange = (newPage) => {
    if (newPage > 0 && newPage <= totalPages) {
      setPage(newPage);
    }
  };

  return (
    <div className="admin-logs-container">
      <AdminHeader />
      <h2>User Interactions Logs</h2>
      <div className="filters">
      <select onChange={(e) => setActionFilter(e.target.value)} value={actionFilter}>
        <option value="">All Actions</option>
        <option value="Login">Login</option>
        <option value="Event_created">Event Created</option>
        <option value="Paid">Paid</option>
        <option value="Liked">Liked</option>
        <option value="Profile_submitted">Profile Submitted</option>
        <option value="Profile_approved">Profile Approved</option>
        <option value="Event_updated">Event Updated</option>
        <option value="Event_approved">Event Approved</option>
        <option value="User_unblocked">User Unblocked</option>
        <option value="User_blocked">User Blocked</option>
        <option value="Refund issued">Refund Issued</option>
      </select>
        <input
          type="text"
          placeholder="Search by Username"
          value={usernameSearch}
          onChange={(e) => setUsernameSearch(e.target.value)}
        />
      </div>

      <table className="logs-table">
        <thead>
          <tr>
            <th>Username</th>
            <th>Action</th>
            <th>Creation Date</th>
            <th>Event ID</th>
          </tr>
        </thead>
        <tbody>
          {logs.map((log) => (
            <tr key={log.interaction_id}>
              <td>{log.username}</td>
              <td>{log.action}</td>
              <td>{log.timestamp}</td>
              <td>{log.event_id ? log.event_id : 'N/A'}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <div className="pagination">
        <button onClick={() => handlePageChange(page - 1)} disabled={page === 1}>
          Previous
        </button>
        <span>
          Page {page} of {totalPages}
        </span>
        <button onClick={() => handlePageChange(page + 1)} disabled={page === totalPages}>
          Next
        </button>
      </div>
    </div>
  );
};

export default AdminLogs;
