import React, { useState, useEffect } from 'react';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import './HostReports.css';
import HostHeader from './HostHeader';

ChartJS.register(ArcElement, Tooltip, Legend);

const HostReports = () => {
  const [reports, setReports] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchReports = async () => {
      try {
        const token = localStorage.getItem('jwt_token'); 
        const response = await fetch('/host/reports', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`, 
          },
        });

        if (response.ok) {
          const data = await response.json();
          setReports(data);
        } else {
          const errorData = await response.json();
          setError(errorData.error);
        }
      } catch (error) {
        setError('Failed to fetch reports. Please try again later.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchReports();
  }, []);

  return (
    <div className="host-reports-page">
      <HostHeader />
      <h1>Host Reports</h1>
      {isLoading ? (
        <p>Loading reports...</p>
      ) : error ? (
        <p className="error-message">{error}</p>
      ) : (
        reports.map((report, index) => (
          <div key={index} className="report-card">
            <h2>{report.event_name}</h2>
            <p><strong>Date:</strong> {new Date(report.event_date).toLocaleString()}</p>
            <p><strong>Location:</strong> {report.event_location}</p>
            <p><strong>Category:</strong> {report.event_category}</p>
            <p><strong>Total Sales:</strong> ${report.total_sales.toFixed(2)}</p>

            <div className="chart-container">
              <h3>Ticket Sales</h3>
              <Pie
                data={{
                  labels: ['Tickets Sold', 'Tickets Unsold'],
                  datasets: [
                    {
                      label: `${report.event_name} - Tickets Sold vs Unsold`,
                      data: [report.tickets_sold, report.tickets_unsold],
                      backgroundColor: ['#4caf50', '#f44336'],
                    },
                  ],
                }}
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                }}
              />
            </div>
            
            <h3>Transactions</h3>
            <table className="transactions-table">
              <thead>
                <tr>
                  <th>Transaction ID</th>
                  <th>User ID</th>
                  <th>Amount Paid</th>
                  <th>Payment Status</th>
                  <th>Timestamp</th>
                </tr>
              </thead>
              <tbody>
                {report.transactions.length > 0 ? (
                  report.transactions.map((transaction) => (
                    <tr key={transaction.transaction_id}>
                      <td>{transaction.transaction_id}</td>
                      <td>{transaction.user_id}</td>
                      <td>${transaction.amount_paid.toFixed(2)}</td>
                      <td>{transaction.payment_status}</td>
                      <td>{new Date(transaction.transaction_date).toLocaleString()}</td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="5">No transactions available.</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        ))
      )}
    </div>
  );
};

export default HostReports;
