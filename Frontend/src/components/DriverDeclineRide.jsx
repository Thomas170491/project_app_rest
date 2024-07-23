import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Button, Container, Card } from 'react-bootstrap';

const DeclineRide = () => {
  const { rideId } = useParams();
  const [ride, setRide] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchRide = async () => {
      try {
        const response = await axios.get(`/drivers/decline_ride/${rideId}`);
        setRide(response.data);
      } catch (error) {
        console.error('Error fetching ride details:', error);
      }
    };

    fetchRide();
  }, [rideId]);

  return (
    <Container>
      <Card className="mt-4">
        <Card.Header>
          <h3>Ride Declined</h3>
        </Card.Header>
        <Card.Body>
          {ride ? (
            <>
              <p><strong>Ride ID:</strong> {ride.ride_id}</p>
              <p><strong>Driver ID:</strong> {ride.driver_id}</p>
              <Button variant="primary" onClick={() => navigate('/drivers/dashboard')}>
                Back to Dashboard
              </Button>
            </>
          ) : (
            <p>Loading...</p>
          )}
        </Card.Body>
      </Card>
    </Container>
  );
};

export default DeclineRide;