import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './components/Home';
import AdminDashboard from './components/AdminDashboard';
import DriverDashboard from './components/DriverDashboard';
import UserDashboard from './components/UserDashboard';
import UserLogin from './components/UserLogin';
import { UserProvider } from './components/UserContext'; // Importation du UserProvider
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  return (
    <UserProvider>
      <Router>
        <div>
          <Navbar />
          <div className='container mt-3'>
            <Routes>
              {/* Add routes here */}
              <Route path='/' element={<Home />} />
              <Route path='/admins/dashboard' element={<AdminDashboard />} />
              <Route path='/drivers/dashboard' element={<DriverDashboard />} />
              <Route path='/users/dashboard' element={<UserDashboard />} />
              <Route path='/users/login' element={<UserLogin />} />
            </Routes>
          </div>
        </div>
      </Router>
    </UserProvider>
  );
}

export default App;
