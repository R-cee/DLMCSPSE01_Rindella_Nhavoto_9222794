import React, { useState, useEffect } from 'react';
import { useStripe, useElements, CardNumberElement, CardExpiryElement, CardCvcElement } from '@stripe/react-stripe-js';
import { useNavigate } from 'react-router-dom';
import './CheckoutForm.css';
import AttendeeHeader from './AttendeeHeader';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { loadStripe } from '@stripe/stripe-js';
import { Elements } from '@stripe/react-stripe-js';

const stripePromise = loadStripe('pk_test_51Q9xXHP5Lv2xb3IZmKeM5mzcg1pi6KTaqDFg5qdRqkgTeknH8bWGf9QS6bBl93UnKi5TzlqCEjFWgyVWygGHqlcd00S1owcfET');

const CheckoutForm = ({ event }) => {
  const stripe = useStripe();
  const elements = useElements();
  const navigate = useNavigate();
  const [clientSecret, setClientSecret] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);
  const [cardNumberError, setCardNumberError] = useState(null);
  const [cardExpiryError, setCardExpiryError] = useState(null);
  const [cardCvcError, setCardCvcError] = useState(null);
  const [ticketQuantity, setTicketQuantity] = useState(1);
  const [totalPrice, setTotalPrice] = useState(event.event_price);
  const [userRole, setUserRole] = useState('');

  useEffect(() => {
    const role = localStorage.getItem('role');
    setUserRole(role);
  }, []);

  useEffect(() => {
    setTotalPrice(event.event_price * ticketQuantity);
  }, [ticketQuantity, event.event_price]);

  useEffect(() => {
    const createPaymentIntent = async () => {
        try {
            const token = localStorage.getItem('jwt_token');
            const response = await fetch('/create-payment-intent', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify({ amount: totalPrice * 100 }),
            });

            const data = await response.json();
            if (data.clientSecret) {
                setClientSecret(data.clientSecret);
            } else {
                throw new Error('Failed to get clientSecret from server');
            }
        } catch (error) {
            toast.error('Error creating payment intent.');
        }
    };

    createPaymentIntent();
}, [totalPrice]);

const handleSubmit = async (e) => {
  e.preventDefault();
  setIsLoading(true);
  setErrorMessage(null);

  if (!stripe || !elements || !clientSecret) {
    setErrorMessage('Stripe is not loaded properly or clientSecret is missing.');
    setIsLoading(false);
    return;
  }

  const cardNumberElement = elements.getElement(CardNumberElement);

  const { paymentIntent, error } = await stripe.confirmCardPayment(clientSecret, {
    payment_method: {
      card: cardNumberElement,
    },
  });

  if (error) {
    toast.error('Payment failed. Please try again.', {
      position: toast.POSITION.TOP_RIGHT,
    });
    setIsLoading(false);
  } else if (paymentIntent && paymentIntent.status === 'succeeded') {
    try {
      const token = localStorage.getItem('jwt_token');
      const response = await fetch('/checkout', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          payment_intent_id: paymentIntent.id,
          event_id: event.event_id,
          tickets_purchased: ticketQuantity,
        }),
      });

      if (response.ok) {
        toast.success('Payment successful!', {
          position: toast.POSITION.TOP_RIGHT,
          autoClose: 3000,
          onClose: () => navigate('/landing'),
        });
      } else {
        const data = await response.json();
        setErrorMessage(data.error || 'Failed to record payment');
      }
    } catch (err) {
      setErrorMessage(`Failed to complete payment: ${err.message}`);
      toast.error(`Failed to complete payment: ${err.message}`, {
        position: toast.POSITION.TOP_RIGHT,
      });
    } finally {
      setIsLoading(false);
    }
  }
};

  const handleQuantityChange = (increment) => {
    setTicketQuantity((prevQuantity) => {
      const updatedQuantity = prevQuantity + increment;
      return updatedQuantity >= 1 ? updatedQuantity : 1;
    });
  };

  const handleCardNumberChange = (event) => {
    setCardNumberError(event.error ? event.error.message : null);
  };

  const handleCardExpiryChange = (event) => {
    setCardExpiryError(event.error ? event.error.message : null);
  };

  const handleCardCvcChange = (event) => {
    setCardCvcError(event.error ? event.error.message : null);
  };

  return (
    <div className="checkout-form-container">
    {userRole === 'Attendee' && <AttendeeHeader />}
      <ToastContainer />
      <h3>{event.event_name}</h3>
      <form onSubmit={handleSubmit} className="checkout-form">
        <div className="price-tickets-container">
          <div className="form-group">
            <label htmlFor="price">Price (per ticket):</label>
            <input
              type="text"
              className="price-input"
              value={`${event.event_price}`}
              disabled
            />
          </div>
          <div className="form-group">
            <label htmlFor="tickets">Quantity:</label>
            <div className="quantity-input">
              <button type="button" onClick={() => handleQuantityChange(-1)} className="quantity-arrow">&minus;</button>
              <input type="number" className="tickets-input" value={ticketQuantity} readOnly />
              <button type="button" onClick={() => handleQuantityChange(1)} className="quantity-arrow">&#43;</button>
            </div>
          </div>
        </div>
        <div className="form-group">
          <label htmlFor="total-price">Total Price:</label>
          <input
            type="text"
            className="price-input"
            value={`${totalPrice.toFixed(2)}`} 
            disabled
          />
        </div>
        <div className="form-group">
          <label htmlFor="cardNumber">Card Number:</label>
          <CardNumberElement className="card-input" onChange={handleCardNumberChange} />
          {cardNumberError && <div className="error-message">{cardNumberError}</div>}
        </div>
        <div className="form-group">
          <label htmlFor="cardExpiry">Expiration Date:</label>
          <CardExpiryElement className="card-input" onChange={handleCardExpiryChange} />
          {cardExpiryError && <div className="error-message">{cardExpiryError}</div>}
        </div>
        <div className="form-group">
          <label htmlFor="cardCvc">CVC:</label>
          <CardCvcElement className="card-input" onChange={handleCardCvcChange} />
          {cardCvcError && <div className="error-message">{cardCvcError}</div>}
        </div>
        {errorMessage && <div className="error-message">{errorMessage}</div>}
        <button type="submit" disabled={!stripe || isLoading}>
          {isLoading ? 'Processing...' : 'Pay Now'}
        </button>
      </form>
    </div>
  );
};

const CheckoutFormWrapper = ({ event }) => {
  return (
    <Elements stripe={stripePromise}>
      <CheckoutForm event={event} />
    </Elements>
  );
};

export default CheckoutFormWrapper;
