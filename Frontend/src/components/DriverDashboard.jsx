import React, { useContext } from 'react';
import { UserContext } from './UserContext'; // Assuming you have a UserProvider that provides the current user context
import { Container, Row, Col, Button, ListGroup, ListGroupItem, Form } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { getDriverDashboard } from './api';

const DriverDashboard = () => {
  const { user } = useContext(UserContext); // Assuming you have a UserContext to get the current user info
  const [driversDashboardData, setDriversDashboardData] = useState(null);
  const navigate = useNavigate();

  // Fetch rides data (this should be replaced with your actual API call)
  useEffect(() => {
    const fetchDriverDashboardData = async () => {
      try {
        const data = await getDriverDashboard()
        setDriversDashboardData(data)
        
      } catch (error) {
        console.error('Error fetching data', error);
      }
    };


    fetchDriverDashboardData();
  }, );

  if (!driversDashboardData) {
    return <div>Loading...</div>;
  }



  return (
    <Container>
      <Row className="justify-content-center">
        <Col md={8}>
          <h2 className="mt-5">Driver Dashboard</h2>
          {/* Display the driver's username */}
          <div className="mb-3">
            <p>Welcome, {user.username}!</p>
          </div>
          <Button variant="primary" jclassName="mt-2" onClick={() => navigate('/drivers/display_rides')}>
            Display Rides
          </Button>
          <Link to='/drivers/display_rides'>Display Rides</Link>

        </Col>
      </Row>
    </Container>
  );
};

export default DriverDashboard;
