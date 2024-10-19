import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import RegistrationForm from './components/RegistrationForm';
import LoginForm from './components/LoginForm';
import LandingPage from './components/LandingPage';
import CheckoutPage from './components/CheckoutPage';
import CheckoutForm from './components/CheckoutForm';
import EventDetails from './components/EventDetails';
import MyEvents from './components/MyEvents';
import ViewProofOfPayment from './components/ViewProofOfPayment';
import AttendeeNotifications from './components/AttendeeNotifications';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/register" element={<RegistrationForm />} />
        <Route path="/login" element={<LoginForm />} />
        <Route path="/landing" element={<LandingPage />} />
        <Route path="/checkout" element={<CheckoutPage />} />
        <Route path="/events/:event_id" element={<EventDetails />} />
        <Route path="/checkout/:event_id" element={<CheckoutForm />} />
        <Route path="/my-events" element={<MyEvents />} />        
        <Route path="/view-proof-of-payment" element={<ViewProofOfPayment />} />
        <Route path="/attendee-notifications" element={<AttendeeNotifications />} />
      </Routes>
    </Router>
  );
}

export default App;
