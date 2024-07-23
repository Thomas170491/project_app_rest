import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Button, Container, Row, Col, ListGroup } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';

const DriverDashboard = () => {
  const [rides, setRides] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchRides = async () => {
      try {
        const response = await axios.get('/drivers/display_rides');
        setRides(response.data);
      } catch (error) {
        console.error('Error fetching rides:', error);
      }
    };

    fetchRides();
  }, []);

  const handleAccept = async (rideId) => {
    try {
      await axios.post(`/drivers/accept_ride/${rideId}`);
      // Refresh the rides list after accepting
      const response = await axios.get('/drivers/display_rides');
      setRides(response.data);
    } catch (error) {
      console.error('Error accepting ride:', error);
    }
  };

  const handleDecline = async (rideId) => {
    try {
      await axios.post(`/drivers/decline_ride/${rideId}`);
      // Refresh the rides list after declining
      const response = await axios.get('/drivers/display_rides');
      setRides(response.data);
    } catch (error) {
      console.error('Error declining ride:', error);
    }
  };

  return (
    <Container>
      <Row>
        <Col>
          <h2>Driver Dashboard</h2>
          <ListGroup>
            {rides.map((ride) => (
              <ListGroup.Item key={ride.ride_id}>
                <h5>Ride ID: {ride.ride_id}</h5>
                <p>Status: {ride.status}</p>
                <p>Departure: {ride.departure}</p>
                <p>Destination: {ride.destination}</p>
                <Button onClick={() => handleAccept(ride.ride_id)} variant="success" className="me-2">
                  Accept
                </Button>
                <Button onClick={() => handleDecline(ride.ride_id)} variant="danger">
                  Decline
                </Button>
              </ListGroup.Item>
            ))}
          </ListGroup>
        </Col>
      </Row>
    </Container>
  );
};

export default DriverDashboard;
