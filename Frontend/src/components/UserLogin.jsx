import React, { useState } from 'react';
import { json, useNavigate } from 'react-router-dom';
import { useUser } from './UserContext';
import { Form, Button, Container, Row, Col, Card } from 'react-bootstrap';
import axiosInstance from './axiosInstance';

const UserLogin = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const { login } = useUser();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {

    e.preventDefault();
    const response = await fetch('http://localhost:5000/users/login',{
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body : JSON.stringify({ username, password })
        
      
    })
    const responseBody = await response.json()
    //console.log('Response:' , responseBody)
    const token = responseBody.token
    localStorage.setItem('acces_token',token )
    try {
      await login({ username, password });
      
      navigate(`${responseBody['next_page']}`);

    } catch (error) {
      console.error('Login failed:', error);
    }
  };

  return (
    <Container className="mt-5">
      <Row className="justify-content-md-center">
        <Col md={6}>
          <Card>
            <Card.Body>
              <h2 className="text-center mb-4">Login</h2>
              <Form onSubmit={handleSubmit}>
                <Form.Group controlId="formUsername">
                  <Form.Label>Username</Form.Label>
                  <Form.Control
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="Enter username"
                  />
                </Form.Group>
                <Form.Group controlId="formPassword" className="mt-3">
                  <Form.Label>Password</Form.Label>
                  <Form.Control
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Password"
                  />
                </Form.Group>
                <Button variant="primary" type="submit" className="mt-4 w-100">
                  Login
                </Button>
              </Form>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default UserLogin;
