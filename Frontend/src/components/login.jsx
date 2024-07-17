import React, { useContext, useState } from 'react';
import { Form, Button, Container, Row, Col } from 'react-bootstrap';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { UserContext } from './UserProvider'; // Import the UserContext

function UserLogin(){

    const [username, setUsername] = useState('')
    const[password, setPassword] = useState('')
    const [rememberMe, setRememberMe] = useState(false)
    const loginUser =  useContext(UserContext)
    const navigate = useNavigate() // for redirection

    const handleSubmit = async (e) => {
        e.preventDefault() //avoid default behavior of an event
        try{
            const response =  await axios.post('/users/login', {username, password, rememberMe})
            if (response.status === 200 ){
                const userData = response.data
                const next_page = response.data.next_page
                loginUser(userData)
                navigate(next_page)
            }
        } catch(error){
            console.error(error)

        }


    } 
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
    };
    
    export default UserLogin;
