import React, { useEffect, useState } from 'react';
import './ViewProofOfPayment.css';
import AttendeeHeader from './AttendeeHeader';

const ViewProofOfPayment = () => {
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    const fetchTransactions = async () => {
      try {
        const token = localStorage.getItem('jwt_token'); 
        const response = await fetch('/view-proof-of-payment', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`, 
          },
        });

        if (response.ok) {
          const data = await response.json();
          setTransactions(data.transactions);
        } else {
          console.error('Failed to fetch transactions.');
        }
      } catch (error) {
        console.error('Error fetching transactions:', error);
      }
    };

    fetchTransactions();
  }, []);

  return (
    <div className="proof-of-payment-page">
      <AttendeeHeader />
      <h1>Proof of Payment</h1>
      {transactions.length > 0 ? (
        <table className="transactions-table">
          <thead>
            <tr>
              <th>Event Name</th>
              <th>Amount Paid</th>
              <th>Payment Status</th>
              <th>Ticket Quantity</th>
              <th>Transaction Date</th>
            </tr>
          </thead>
          <tbody>
            {transactions.map((transaction) => (
              <tr>
                <td>{transaction.event_name}</td>
                <td>{transaction.amount_paid}</td>
                <td>{transaction.payment_status}</td>
                <td>{transaction.quantity}</td>
                <td>{new Date(transaction.transaction_date).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No transactions found.</p>
      )}
    </div>
  );
};

export default ViewProofOfPayment;
