import React, { useState, useEffect } from 'react';
import './PaymentAccountForm.css';
import HostHeader from './HostHeader';

const PaymentAccountForm = () => {
  const [formData, setFormData] = useState({
    stripe_account_id: '',
    mpesa_number: ''
  });

  const [errors, setErrors] = useState({});
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    const fetchAccountDetails = async () => {
      try {
        const token = localStorage.getItem('jwt_token');
        const response = await fetch('/host/payment-account', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          }
        });

        if (response.ok) {
          const data = await response.json();
          setFormData({
            stripe_account_id: data.stripe_account_id || '',
            mpesa_number: data.mpesa_number || ''
          });
        } else {
          console.error('Failed to fetch account details');
        }
      } catch (error) {
        console.error('Error fetching account details:', error);
      }
    };

    fetchAccountDetails();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('jwt_token');
      const response = await fetch('/host/payment-account', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        setSuccess(true);
        setErrors({});
      } else {
        const data = await response.json();
        setErrors(data.errors || {});
        console.error('Server returned an error:', data);
      }
    } catch (error) {
      console.error('Error saving payment details:', error);
      alert('An error occurred while saving the payment account details.');
    }
  };

  return (
    <div className="payment-account-form">
      <HostHeader />
      <h2>Payment Account Details</h2>
      {success && <p className="success-message">Payment details saved successfully!</p>}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Stripe Account ID:</label>
          <input
            type="text"
            name="stripe_account_id"
            value={formData.stripe_account_id}
            onChange={handleChange}
          />
        </div>
        <div className="form-group">
          <label>Mpesa Number:</label>
          <input
            type="text"
            name="mpesa_number"
            value={formData.mpesa_number}
            onChange={handleChange}
          />
        </div>
        <button type="submit">Save Payment Details</button>
      </form>
    </div>
  );
};

export default PaymentAccountForm;
