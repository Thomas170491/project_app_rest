import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { Navbar, Nav } from 'react-bootstrap';
import { UserContext } from './UserContext'; // Importation du UserContext

const NavigationBar = () => {
    const {user, logout} = useContext(UserContext)

    return (
        <Navbar bg="light" expand="lg">
          <Navbar.Brand as={Link} to="/">RideShare</Navbar.Brand>
          <Navbar.Toggle aria-controls="navbarNav" />
          <Navbar.Collapse id="navbarNav">
            <Nav className="ml-auto">
              {user.isAuthenticated ? (
                <>
                  {user.role === 'admin' && (
                    <>
                      <Nav.Link as={Link} to="/admins/dashboard">Admin Dashboard</Nav.Link>
                      <Nav.Link as={Link} to="/" onClick={logout}>Logout</Nav.Link>
                      {/* Ajouter de nouvelles routes pour l'admin ici */}
                    </>
                  )}
                  {user.role === 'driver' && (
                    <>
                      <Nav.Link as={Link} to="/drivers/dashboard">Driver Dashboard</Nav.Link>
                      <Nav.Link as={Link} to="/" onClick={logout}>Logout</Nav.Link>
                      {/* Ajouter de nouvelles routes pour le driver ici */}
                    </>
                  )}
                  {user.role === 'user' && (
                    <>
                      <Nav.Link as={Link} to="/users/dashboard">User Dashboard</Nav.Link>
                      <Nav.Link as={Link} to="/" onClick={logout}>Logout</Nav.Link>
                      {/* Ajouter de nouvelles routes pour l'utilisateur ici */}
                    </>
                  )}
                </>
              ) : (
                <>
                  <Nav.Link as={Link} to="/users/login">User Login</Nav.Link>
              
                  {/* Ajouter de nouvelles routes publiques ici */}
                </>
              )}
            </Nav>
          </Navbar.Collapse>
        </Navbar>
      );
    };
    
    export default NavigationBar;
