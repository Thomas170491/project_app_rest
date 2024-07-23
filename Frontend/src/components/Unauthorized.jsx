import React from 'react';
import { Container, Row, Col, Card } from 'react-bootstrap';

const Unauthorized = () => {
  return (
    <Container className="mt-5">
      <Row className="justify-content-md-center">
        <Col md={8}>
          <Card>
            <Card.Body>
              <h2 className="text-center">Unauthorized</h2>
              <p className="text-center">You do not have permission to view this page.</p>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default Unauthorized;
