import React, { useContext, useState, useEffect } from 'react';
import { Form, Button, Container, Row, Col } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { loginUser } from './api';
import { UserContext } from './UserContext';

function UserLogin() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const navigate = useNavigate();
  const { user, login } = useContext(UserContext);

  useEffect(() => {
    if (user.isAuthenticated) {
      navigate(user.role === 'admin' ? '/admins/dashboard' : 
               user.role === 'driver' ? '/drivers/dashboard' : 
               '/users/dashboard');
    }
  }, [user, navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await loginUser(username, password);

      console.log('Login API response:', response);

      if (response && response.token) {
        const userData = {
          username, 
          isAuthenticated: true,
          role: response.role // Add role to userData if available
        };
        const nextPage = response.next_page;

        if (nextPage) {
          localStorage.setItem('access_token', response.token);
          login(userData); 
          navigate(nextPage); 
        } else {
          throw new Error('Next page is not defined in the response');
        }
      } else {
        alert(`Unexpected response format: ${JSON.stringify(response)}`);
      }
    } catch (error) {
      console.error('Login error:', error);
      alert(`Login error: ${error.message || 'An unexpected error occurred'}`);
    }
  };

  return (
    <Container>
      <Row className="justify-content-center">
        <Col md={6}>
          <h2 className="mt-5">User Login</h2>
          <Form onSubmit={handleSubmit}>
            <Form.Group controlId="formUsername">
              <Form.Label>Username</Form.Label>
              <Form.Control
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </Form.Group>

            <Form.Group controlId="formPassword">
              <Form.Label>Password</Form.Label>
              <Form.Control
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </Form.Group>

            <Form.Group controlId="formRememberMe">
              <Form.Check
                type="checkbox"
                label="Remember me"
                checked={rememberMe}
                onChange={(e) => setRememberMe(e.target.checked)}
              />
            </Form.Group>

            <Button variant="primary" type="submit">
              Sign In
            </Button>
          </Form>
        </Col>
      </Row>
    </Container>
  );
}

export default UserLogin;
