import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import RegistrationForm from './components/RegistrationForm';
import LoginForm from './components/LoginForm';
import HostDashboardPage from './components/HostDashboardPage';
import VettingForm from './components/VettingForm';


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/register" element={<RegistrationForm />} />
        <Route path="/login" element={<LoginForm />} />
        <Route path="/host-dashboard" element={<HostDashboardPage />} />
        <Route path="/vetting" element={<VettingForm />} />
      </Routes>
    </Router>
  );
}

export default App;
