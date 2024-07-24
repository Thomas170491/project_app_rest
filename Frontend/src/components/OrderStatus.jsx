import React, { useState } from 'react';
import axiosInstance from './axiosInstance';

const OrderStatus = ({ rideId }) => {
  const [rideStatus, setRideStatus] = useState(null);

  const handleFetchStatus = async () => {
    try {
      const response = await axiosInstance.get(`/users/order_status/${rideId}`);
      setRideStatus(response.data);
    } catch (error) {
      console.error('Failed to fetch ride status', error);
    }
  };

  return (
    <div>
      <h1>Ride Status</h1>
      <button onClick={handleFetchStatus}>Fetch Ride Status</button>
      {rideStatus && (
        <div>
          <p>Ride Status: {rideStatus.ride_status}</p>
        </div>
      )}
    </div>
  );
};

export default OrderStatus;
