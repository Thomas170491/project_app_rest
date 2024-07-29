import React, { useContext } from "react";
import { Nav, Navbar } from "react-bootstrap";
import { Link, useNavigate } from "react-router-dom";
import { UserContext } from "./UserContext";

const NavigationBar = () => {
  const navigate = useNavigate();
  const { logout } = useContext(UserContext);
  const token = localStorage.getItem("access_token");
  const user = JSON.parse(localStorage.getItem("user"));

  const notificationPage = async () => {
    navigate("/notification");
  };
  const payPage = async () => {
    navigate("/users/payment");
  };
  const UserDashboard = () => {
    navigate('/users/dashboard')
  }


  const logoutRequest = async () => {
    console.log("heree");
    const response = await fetch("http://localhost:8000/logout/", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    const responseBody = await response.json();
    if (responseBody.status === "success") {
      console.log(responseBody);
      logout();
      navigate("/users/login");
    } else {
      console.error("There is error in logging out", responseBody.message);
    }
  };
  return (
    <Navbar bg="light" expand="lg">
      <Navbar.Brand as={Link} to="/">
        RideShare
      </Navbar.Brand>
      <Navbar.Toggle aria-controls="navbarNav" />
      <Navbar.Collapse id="navbarNav">
        <Nav className="ml-auto">
          {user === null ? (
            <Nav.Link as={Link} to="/users/login">
              User Login
            </Nav.Link>
          ) : (
            <>
              <Nav.Link onClick={() => logoutRequest()}>Logout</Nav.Link>
              <br />
              <Nav.Link onClick={() => notificationPage()}>
                Notifications
              </Nav.Link>
              <br />
    
              {user.role === "driver" && (
                <>
                  <Nav.Link as={Link} to="/drivers/dashboard">
                    Driver Dashboard
                  </Nav.Link>
                  <Nav.Link as={Link} to="/" onClick={logout}>
                    Logout
                  </Nav.Link>
                </>
              )}
              {user.role === "customer" && (
                <>
                  <Nav.Link as={Link} to="/users/dashboard" onClick={()=> UserDashboard() }>
                    User Dashboard
                  </Nav.Link>
                  <br />
              
                  <Nav.Link onClick={() => payPage()}>
                    Pay
                  </Nav.Link>
                </>
              )}
            </>
          )}
        </Nav>
      </Navbar.Collapse>
    </Navbar>
  );
};

export default NavigationBar;
