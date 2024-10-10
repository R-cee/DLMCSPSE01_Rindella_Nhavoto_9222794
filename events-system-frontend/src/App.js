import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import RegistrationForm from './components/RegistrationForm';
import LoginForm from './components/LoginForm';
import VettingForm from './components/VettingForm';
import AdminDashboardPage from './components/AdminDashboardPage';
import AdminLogs from './components/AdminLogs';



function App() {
  return (
    <Router>
      <Routes>
        <Route path="/register" element={<RegistrationForm />} />
        <Route path="/login" element={<LoginForm />} />
        <Route path="/admin-dashboard" element={<AdminDashboardPage />} />
        <Route path="/admin/vetting/:user_id" element={<VettingForm isAdmin={true} />} />
        <Route path="/admin/view-logs" element={<AdminLogs />} />

      </Routes>
    </Router>
  );
}

export default App;
