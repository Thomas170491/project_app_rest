import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, Row, Col, Card, Button } from 'react-bootstrap';

const RideAccepted = ({ rideOrder }) => {
  const navigate = useNavigate();

  return (
    <Container className="mt-5">
      <Row className="justify-content-md-center">
        <Col md={8}>
          <Card>
            <Card.Header>Ride Accepted</Card.Header>
            <Card.Body>
              <p><strong>Ride ID:</strong> {rideOrder.id}</p>
              <p><strong>Passenger Name:</strong> {rideOrder.name}</p>
              <p><strong>Departure:</strong> {rideOrder.departure}</p>
              <p><strong>Destination:</strong> {rideOrder.destination}</p>
              <p><strong>Accepted Time:</strong> {rideOrder.accepted_time}</p>
              <p><strong>Status:</strong> {rideOrder.status}</p>
              <p><strong>Driver ID:</strong> {rideOrder.driver_id}</p>
              <Button
                variant="primary"
                onClick={() => navigate('/dashboard')}
                className="me-2"
              >
                Back to Dashboard
              </Button>
              <Button
                variant="primary"
                onClick={() => navigate('/display-rides')}
              >
                See Remaining Available Rides
              </Button>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default RideAccepted;
