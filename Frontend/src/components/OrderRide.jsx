import React, { useState } from 'react';
import axiosInstance from './axiosInstance';

const OrderRide = () => {
  const [departure, setDeparture] = useState('');
  const [destination, setDestination] = useState('');
  const [rideDetails, setRideDetails] = useState(null);

  const handleOrderRide = async () => {
    try {
      const response = await axiosInstance.post('/users/order_ride', { departure, destination });
      setRideDetails(response.data);
    } catch (error) {
      console.error('Failed to order ride', error);
    }
  };

  return (
    <div>
      <h1>Order Ride</h1>
      <div>
        <label>Departure</label>
        <input type="text" value={departure} onChange={(e) => setDeparture(e.target.value)} />
      </div>
      <div>
        <label>Destination</label>
        <input type="text" value={destination} onChange={(e) => setDestination(e.target.value)} />
      </div>
      <button onClick={handleOrderRide}>Order Ride</button>
      {rideDetails && (
        <div>
          <h2>Ride Details</h2>
          <p>Ride ID: {rideDetails.ride_id}</p>
          <p>Price: {rideDetails.price}</p>
        </div>
      )}
    </div>
  );
};

export default OrderRide;
