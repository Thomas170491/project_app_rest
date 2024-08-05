import React, { useState } from "react";
import { Button, Form } from "react-bootstrap";
import { useLocation, useNavigate } from "react-router-dom";
import Map from "./Map"; // Assuming you have a Map component
const baseUrl = import.meta.env.VITE_REACT_APP_BASE_URL;

import "leaflet/dist/leaflet.css";

const OrderRide = () => {
  const navigate = useNavigate();
  const token = localStorage.getItem("access_token");
  const user = JSON.parse(localStorage.getItem("user"));
  const location = useLocation();
  const { order_data } = location.state || {};

  const [departure, setDeparture] = useState("");
  const [destination, setDestination] = useState("");
  const [totalDistance, setTotalDistance] = useState("");
  const [coordinates, setCoordinates] = useState({
    departure: { lat: "", lng: "" },
    destination: { lat: "", lng: "" },
  });

  const bookRideOrder = (e) => {
    e.preventDefault();
    console.log(coordinates);
  };

  const handleDepartureChange = (e) => {
    setDeparture(e.target.value);
  };

  const handleDestinationChange = (e) => {
    setDestination(e.target.value);
  };

  // Handle Map Clicks
  const handleMapClick = (lat, lng) => {
    if (!coordinates.departure.lat) {
      setCoordinates((prevCoordinates) => ({
        ...prevCoordinates,
        departure: { lat, lng },
      }));
    } else if (!coordinates.destination.lat) {
      setCoordinates((prevCoordinates) => ({
        ...prevCoordinates,
        destination: { lat, lng },
      }));
    }
  };

  const handleMarkerDrag = (e, type) => {
    const lat = e.latLng.lat();
    const lng = e.latLng.lng();
    setCoordinates((prevCoordinates) => ({
      ...prevCoordinates,
      [type]: { lat, lng },
    }));
  };

  const bookRide = async (e) => {
    e.preventDefault();
    console.log(coordinates);
    const response = await fetch(`https://${baseUrl}/book-ride/`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        departure,
        destination,
        order_data,
        totalDistance,
        coordinates,
      }),
    });
    const responseBody = await response.json();
    if (responseBody.status === "success") {
      navigate("/notification");
    } else {
      console.error("Cant book the Ride", responseBody.message);
    }
  };
  return (
    <div>
      <h1>Order Ride</h1>
      <div>
        <Form onSubmit={bookRide}>
          <Form.Group>
            <Form.Label>Departure</Form.Label>
            <Form.Control
              type="text"
              onChange={(e) => setDeparture(e.target.value)}
              placeholder="Enter Departure"
            />
          </Form.Group>
          <Form.Group className="mt-3">
            <Form.Label>Destination</Form.Label>
            <Form.Control
              type="text"
              onChange={(e) => setDestination(e.target.value)}
              placeholder="Enter Destination"
            />
          </Form.Group>
          <Form.Group className="mt-3">
            <Form.Label>Total Distance in KM</Form.Label>
            <Form.Control
              type="text"
              onChange={(e) => setTotalDistance(e.target.value)}
              placeholder="Enter Total Distance"
            />
          </Form.Group>
          <Button variant="primary" type="submit" className="mt-4 w-100">
            Order Ride
          </Button>
        </Form>
      </div>
      <div>
        <Map
          coordinates={coordinates}
          YOUR_GOOGLE_MAPS_API_KEY
          handleMapClick={handleMapClick}
          handleMarkerDrag={handleMarkerDrag}
        />
      </div>
    </div>
  );
};

export default OrderRide;
