import React, { useState } from 'react';
import axiosInstance from './axiosInstance';

const Pay = ({ rideId }) => {
  const [paymentDetails, setPaymentDetails] = useState(null);

  const handlePay = async () => {
    try {
      const response = await axiosInstance.get(`/users/pay/${rideId}`);
      setPaymentDetails(response.data);
    } catch (error) {
      console.error('Failed to initiate payment', error);
    }
  };

  return (
    <div>
      <h1>Pay for Ride</h1>
      <button onClick={handlePay}>Pay</button>
      {paymentDetails && (
        <div>
          <p>Payment Client ID: {paymentDetails.client_id}</p>
          <a href={paymentDetails.approval_url} target="_blank" rel="noopener noreferrer">
            Approve Payment
          </a>
        </div>
      )}
    </div>
  );
};

export default Pay;