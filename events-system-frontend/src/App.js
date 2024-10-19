import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import RegistrationForm from './components/RegistrationForm';
import LoginForm from './components/LoginForm';
import VettingForm from './components/VettingForm';
<<<<<<< HEAD
import HostEventsPage from './components/HostEventsPage';
import PaymentAccountForm from './components/PaymentAccountForm';
import HostReports from './components/HostReports';
import EventForm from './components/EventForm';
import Notification from './components/Notification'
=======
import AdminDashboardPage from './components/AdminDashboardPage';
import AdminLogs from './components/AdminLogs';
import ManageEventsPage from './components/ManageEventsPage';
import ManageUserPage from './components/ManageUserPage';
import AdminCreationForm from './components/AdminCreationForm';
>>>>>>> admin

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/register" element={<RegistrationForm />} />
        <Route path="/login" element={<LoginForm />} />
<<<<<<< HEAD
        <Route path="/host-dashboard" element={<HostDashboardPage />} />
        <Route path="/vetting" element={<VettingForm />} />
        <Route path="/create-event" element={<EventForm />} />
        <Route path="/edit-event/:event_id" element={<EventForm />} />
        <Route path="/host-events" element={<HostEventsPage />} />
        <Route path="/host/payment-account" element={<PaymentAccountForm />} />
        <Route path="/host/reports" element={<HostReports />} />
        <Route path="/notifications" element={<Notification />} />
=======
        <Route path="/admin-dashboard" element={<AdminDashboardPage />} />
        <Route path="/admin/vetting/:user_id" element={<VettingForm isAdmin={true} />} />
        <Route path="/admin/view-logs" element={<AdminLogs />} />
        <Route path="/admin/manage-events" element={<ManageEventsPage />} />
        <Route path="/admin/create-admin" element={<AdminCreationForm />} />
        <Route path="/admin/manage-users" element={<ManageUserPage />} />
>>>>>>> admin
      </Routes>
    </Router>
  );
}

export default App;
