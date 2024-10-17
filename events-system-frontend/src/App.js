import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import RegistrationForm from './components/RegistrationForm';
import LoginForm from './components/LoginForm';
import HostDashboardPage from './components/HostDashboardPage';
import VettingForm from './components/VettingForm';
import HostEventsPage from './components/HostEventsPage';
import PaymentAccountForm from './components/PaymentAccountForm';
import HostReports from './components/HostReports';
import EventForm from './components/EventForm';
import Notification from './components/Notification'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/register" element={<RegistrationForm />} />
        <Route path="/login" element={<LoginForm />} />
        <Route path="/host-dashboard" element={<HostDashboardPage />} />
        <Route path="/vetting" element={<VettingForm />} />
        <Route path="/create-event" element={<EventForm />} />
        <Route path="/edit-event/:event_id" element={<EventForm />} />
        <Route path="/host-events" element={<HostEventsPage />} />
        <Route path="/host/payment-account" element={<PaymentAccountForm />} />
        <Route path="/host/reports" element={<HostReports />} />
        <Route path="/notifications" element={<Notification />} />
      </Routes>
    </Router>
  );
}

export default App;
