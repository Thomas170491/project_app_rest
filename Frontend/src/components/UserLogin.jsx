import React, { useState } from "react";
import { Button, Card, Col, Container, Form, Row } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import { useUser } from "./UserContext";
var baseUrl = import.meta.env.VITE_REACT_APP_BASE_URL;
console.log(`https://${baseUrl}/admin/`);

const UserLogin = () => {
  console.log(`https://${baseUrl}/admin/`);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const { login } = useUser();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    const response = await fetch(`https://${baseUrl}/login/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password }),
    });
    const responseBody = await response.json();
    if (responseBody.status === "success") {
      console.log(responseBody);
      console.log(responseBody.data.token);
      const id = responseBody.data.id;
      const username = responseBody.data.username;
      const email = responseBody.data.email;
      const name = responseBody.data.name;
      const is_superuser = responseBody.data.is_superuser;
      const role = responseBody.data.role;

      await login(
        {
          id: id,
          username: username,
          email: email,
          name: name,
          role: role,
        },
        responseBody.data.token
      );
      if (is_superuser) {
        window.open(`https://${baseUrl}/admin/`);
      } else if (role === "driver") {
        navigate("/drivers/dashboard");
      } else {
        navigate("/users/dashboard");
      }
    } else {
      console.error("Login failed:", responseBody.message);
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
