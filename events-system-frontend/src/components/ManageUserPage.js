import React, { useState, useEffect } from 'react';
import './ManageUserPage.css';
import AdminHeader from './AdminHeader';    
import { useNavigate } from 'react-router-dom';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const ManageUserPage = () => {
    const [users, setUsers] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        fetchUsers();
    }, []);

    const fetchUsers = async () => {
        try {
            const token = localStorage.getItem('jwt_token'); 
            const response = await fetch('/api/admin/users', {
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            });
            if (response.ok) {
                const data = await response.json();
                setUsers(data);
            } else {
                toast.error('Failed to fetch users', { position: toast.POSITION.TOP_RIGHT });
            }
        } catch (error) {
            toast.error('Error fetching users', { position: toast.POSITION.TOP_RIGHT });
        }
    };

    const toggleUserStatus = async (user_id) => {
        try {
            const token = localStorage.getItem('jwt_token');
            const response = await fetch(`/api/admin/user-status/${user_id}`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            });
            const data = await response.json();
            if (data.success) {
                fetchUsers(); 
                toast.success('User status updated successfully', {
                    position: toast.POSITION.TOP_RIGHT,
                    onClose: () => navigate('/admin-dashboard') 
                });
            } else {
                toast.error('Error updating user status', { position: toast.POSITION.TOP_RIGHT });
            }
        } catch (error) {
            toast.error('Error updating user status', { position: toast.POSITION.TOP_RIGHT });
        }
    };

    return (
        <div className="manage-user-page">
            <AdminHeader />
            <ToastContainer /> {/* Add ToastContainer to display toast messages */}
            <h2>Manage Users</h2>
            <table>
                <thead>
                    <tr>
                        <th>Username</th>
                        <th>Email</th>
                        <th>Role</th>
                        <th>Status</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {users.map((user) => (
                        <tr key={user.user_id}>
                            <td>{user.username}</td>
                            <td>{user.email}</td>
                            <td>{user.role}</td>
                            <td>{user.status}</td>
                            <td>
                                <button
                                    className={`status-button ${user.status === 'active' ? 'active' : 'blocked'}`}
                                    onClick={() => toggleUserStatus(user.user_id)}
                                >
                                    {user.status === 'active' ? 'Block' : 'Unblock'}
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default ManageUserPage;
