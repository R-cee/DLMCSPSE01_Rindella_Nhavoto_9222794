import React from 'react';
import { useLocation } from 'react-router-dom';
import { loadStripe } from '@stripe/stripe-js';
import { Elements } from '@stripe/react-stripe-js';
import CheckoutForm from './CheckoutForm';

const stripePromise = loadStripe('your-public-key-here');

const CheckoutPage = () => {
  const location = useLocation();
  const { event } = location.state; 

  return (
    <div>
      <Elements stripe={stripePromise}>
        <CheckoutForm event={event} />
      </Elements>
    </div>
  );
};

export default CheckoutPage;
