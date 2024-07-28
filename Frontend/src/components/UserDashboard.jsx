import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const Dashboard = () => {
  const navigate = useNavigate();
  const token = localStorage.getItem("access_token");
  const user = JSON.parse(localStorage.getItem("user"));
  const [cars, setCars] = useState([]);

  const order_ride = async (username) => {
    console.log(username);
    const response = await fetch("http://localhost:8000/order-ride/", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ username }),
    });
    const responseBody = await response.json();
    if (responseBody.status === "success") {
      console.log();
      let order_data = responseBody.data;
      navigate("/users/order_ride", { state: { order_data } });
    } else {
      console.error("Unable to order a ride", responseBody.message);
    }
  };

  const fetch_user_dashboard = async () => {
    const response = await fetch("http://localhost:8000/user-dashboard/", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    const responseBody = await response.json();
    if (responseBody.status === "success") {
      setCars(responseBody.data);
      console.log(responseBody.data);
    } else {
      console.error("User Dashboard data fetch failed:", responseBody.message);
    }
  };

  useEffect(() => {
    fetch_user_dashboard();
  }, []);

  return (
    <div>
      <p></p>
      <h1>Welcome {user.username} to your Dashboard</h1>
      <h3>Available Rides</h3>
      <table>
        <thead>
          <tr>
            <td>Car Model</td>
            <td>Car Year</td>
            <td>Owner</td>
            <td>Phone Number</td>
            <td>Email</td>
            <td>Booked</td>
            <td>Action</td>
          </tr>
        </thead>
        <tbody>
          {cars.map((car, index) => (
            <tr key={index}>
              <td>{car.make}</td>
              <td>{car.year}</td>
              <td>{car.user.username}</td>
              <td>{car.user.phone_number}</td>
              <td>{car.user.email}</td>
              <td>{car.is_booked ? "Yes" : "No"}</td>
              <td>
                <button onClick={() => order_ride(car.user.username)}>
                  Order
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
export default Dashboard;
