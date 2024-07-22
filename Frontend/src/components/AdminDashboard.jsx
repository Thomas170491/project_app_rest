import React, { useContext, useState } from 'react'
import { UserContext } from './UserContext'; // Assuming you have a UserProvider that provides the current user context
import { Container, Row, Col, Button, ListGroup, ListGroupItem, Form } from 'react-bootstrap';
import { Link, useNavigate } from 'react-router-dom';
import { getAdminDashboard } from './api';


const AdminDashboard = () => {
  const { user } = useContext(UserContext);
  const [users, setUsers] = useState([]);
  const [drivers, setDrivers] = useState([]);
  const [admins, setAdmins] = useState([]);
  const navigate = useNavigate();

  // Fetch data (replace with your actual API call)
  useEffect(() => {
    const fetchAdminData = async () => {
      try {
        const response = await getAdminDashboard();

        setUsers(response.data.users);
        setDrivers(response.data.drivers);
        setAdmins(response.data.admins);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchAdminData();
  }, []);

  const handleDeleteUser = async (userId) => {
    try {
      await axios.post(`/api/admins/delete_user/${userId}`);
      setUsers(users.filter(user => user.id !== userId));
    } catch (error) {
      console.error('Error deleting user:', error);
    }
  };

  const handleEditUser = (userId) => {
    navigate(`/admins/edit_user/${userId}`);
  };

  const handleDeleteDriver = async (driverId) => {
    try {
      await axios.post(`/api/admins/delete_driver/${driverId}`);
      setDrivers(drivers.filter(driver => driver.id !== driverId));
    } catch (error) {
      console.error('Error deleting driver:', error);
    }
  };

  const handleEditDriver = (driverId) => {
    navigate(`/admins/edit_driver/${driverId}`);
  };

  const handleDeleteAdmin = async (adminId) => {
    try {
      await axios.post(`/api/admins/delete_admin/${adminId}`);
      setAdmins(admins.filter(admin => admin.id !== adminId));
    } catch (error) {
      console.error('Error deleting admin:', error);
    }
  };

  return (
    <div className="container mt-4">
      <h1>Admin Dashboard</h1>
      
      {/* Display the admin's username */}
      <div className="mb-3">
        <p>Welcome, {user.username}!</p>
      </div>

      {/* Link to send invitation */}
      <div className="mb-3">
        <Link to="/admins/send_link" className="btn btn-primary">Send Invitation</Link>
      </div>

      <h2>Users</h2>
      <table className="table table-striped">
        <thead>
          <tr>
            <th>Username</th>
            <th>Email</th>
            <th>Role</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {users.map(user => (
            <tr key={user.id}>
              <td>{user.username}</td>
              <td>{user.email}</td>
              <td>User</td>
              <td>
                <button onClick={() => handleDeleteUser(user.id)} className="btn btn-danger btn-sm">Delete</button>
                <button onClick={() => handleEditUser(user.id)} className="btn btn-primary btn-sm">Edit</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2>Drivers</h2>
      <table className="table table-striped">
        <thead>
          <tr>
            <th>Username</th>
            <th>Email</th>
            <th>Role</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {drivers.map(driver => (
            <tr key={driver.id}>
              <td>{driver.username}</td>
              <td>{driver.email}</td>
              <td>Driver</td>
              <td>
                <button onClick={() => handleDeleteDriver(driver.id)} className="btn btn-danger btn-sm">Delete</button>
                <button onClick={() => handleEditDriver(driver.id)} className="btn btn-primary btn-sm">Edit</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2>Admins</h2>
      <table className="table table-striped">
        <thead>
          <tr>
            <th>Username</th>
            <th>Email</th>
            <th>Role</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {admins.map(admin => (
            <tr key={admin.id}>
              <td>{admin.username}</td>
              <td>{admin.email}</td>
              <td>Admin</td>
              <td>
                <button onClick={() => handleDeleteAdmin(admin.id)} className="btn btn-danger btn-sm">Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AdminDashboard;
