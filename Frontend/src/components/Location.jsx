import { GoogleMap, LoadScript, MarkerF } from "@react-google-maps/api";

import React, { useEffect, useRef, useState } from "react";

const baseUrl = import.meta.env.VITE_REACT_APP_WEBSOCKET_URL;

const Location = () => {
  const token = localStorage.getItem("access_token");
  const user = JSON.parse(localStorage.getItem("user"));
  const [userInfo, setUserInfo] = useState([]); // Me
  const [targetUserInfo, setTargetUserInfo] = useState([]); // Target User
  const [startRide, setStartRide] = useState(false);

  const [coordinates, setCoordinates] = useState({
    destination: null,
    user: null,
    driver: null,
  });

  let targetUser = "1";
  if (user.username === "admin") {
    targetUser = "2";
  }
  const wsRef = useRef(null);

  useEffect(() => {
    wsRef.current = new WebSocket(
      `${baseUrl}/ws/ride-share/?token=${token}`
      // `ws://localhost:8000/ws/ride-share/?token=${token}`
    );
    wsRef.current.onopen = () => {
      console.log("Connected to the server");
    };
    wsRef.current.onclose = () => {
      console.log("Dis Connected to the server");
    };
    wsRef.current.onerror = (error) => {
      console.log("Websocket error: ", error);
    };

    // Receive data from socket
    wsRef.current.onmessage = (message) => {
      console.log("backend", message.data);
      const data = JSON.parse(message.data);

      if (data.role === "customer") {
        setCoordinates((prev) => ({
          ...prev,
          user: {
            lat: data.latitude,
            lng: data.longitude,
          },
        }));
      } else {
        setCoordinates((prev) => ({
          ...prev,
          driver: {
            lat: data.latitude,
            lng: data.longitude,
          },
        }));
      }
      setCoordinates((prev) => ({
        ...prev,
        destination: data.destination,
      }));

      if (data.username === user.username) {
        setUserInfo((prevUserInfo) => [...prevUserInfo, data]);
      } else {
        setTargetUserInfo((prevTargetUserInfo) => [
          ...prevTargetUserInfo,
          data,
        ]);
      }
      console.log(data);
    };

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  useEffect(() => {
    const sendLocation = (position) => {
      const { latitude, longitude } = position.coords;
      if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
        let latitude = 29.802685;
        let longitude = 71.738248;

        wsRef.current.send(
          JSON.stringify({ latitude, longitude, targetUser, startRide })
        );
      }
    };

    const handleError = (error) => {
      console.log("Error getting location: ", error);
    };

    if (navigator.geolocation) {
      const options = {
        enableHighAccuracy: true,
        timeout: 5000,
        maximumAge: 0,
      };
      const watchId = navigator.geolocation.watchPosition(
        sendLocation,
        handleError,
        options
      );
      return () => navigator.geolocation.clearWatch(watchId);
    } else {
      console.error("Geolocation is not supported by this browser");
    }
  }, []);

  const handleRide = () => {
    setStartRide(true);
  };

  const mapStyles = {
    height: "400px",
    width: "800px",
  };
  const defaultCenter = {
    lat: 40.712776,
    lng: -74.005974,
  };

  const [mapLoaded, setMapLoaded] = useState(false);

  const mapRef = useRef(null);
  const directionsServiceRef = useRef(null);
  const directionsRendererRef = useRef(null);
  const onLoad = (mapInstance) => {
    mapRef.current = mapInstance;
    directionsServiceRef.current = new google.maps.DirectionsService();
    directionsRendererRef.current = new google.maps.DirectionsRenderer();
    directionsRendererRef.current.setMap(mapInstance);
    setMapLoaded(true); // Set map as loaded
  };
  useEffect(() => {
    if (mapLoaded && coordinates.driver && coordinates.user) {
      const directionsService = directionsServiceRef.current;
      const directionsRenderer = directionsRendererRef.current;

      if (directionsService && directionsRenderer) {
        directionsService.route(
          {
            origin: coordinates.driver,
            destination: coordinates.user,
            travelMode: google.maps.TravelMode.DRIVING,
          },
          (result, status) => {
            if (status === google.maps.DirectionsStatus.OK) {
              directionsRenderer.setDirections(result);
            } else {
              console.error("Error fetching directions:", result);
            }
          }
        );
      } else {
        console.error(
          "DirectionsService or DirectionsRenderer is not initialized"
        );
      }
    }
  }, [mapLoaded, coordinates.driver, coordinates.user]);

  return (
    <div>
      <h1>Sending Your Location.....</h1>

      {user.role === "customer" ? (
        <button onClick={handleRide}>Start Ride</button>
      ) : null}

      <div className="map-container">
        <LoadScript googleMapsApiKey="AIzaSyBD9TzCsljMc19-ZSoiBJrbuycySEBpirE">
          <GoogleMap
            mapContainerStyle={mapStyles}
            zoom={12}
            center={coordinates.user || defaultCenter} // Center map on default location
            onLoad={onLoad} // Added onLoad handler
          >
            {coordinates.user && (
              <MarkerF
                position={coordinates.user}
                label="Customer"
                // icon="http://maps.google.com/mapfiles/ms/icons/blue-dot.png" // Optional: custom icon
              />
            )}
            {coordinates.driver && (
              <MarkerF
                position={coordinates.driver}
                label="Driver"
                // icon="http://maps.google.com/mapfiles/ms/icons/blue-dot.png" // Optional: custom icon
              />
            )}

            {/* <MarkerF position={coordinates.user} label="" /> */}
          </GoogleMap>
        </LoadScript>
      </div>
      <div
        style={{
          display: "flex",
          gap: "50px",
          border: "1px solid black",
          padding: "0 50px",
        }}
      >
        <ul>
          <h5>My Current Location Updates</h5>
          {userInfo.map((message, index) => (
            <li key={index}>
              {message.username}: {message.latitude}, {message.longitude}
            </li>
          ))}
        </ul>
        <ul>
          <h5>Target user Location Updates</h5>
          {targetUserInfo.map((message, index) => (
            <li key={index}>
              {message.username}: {message.latitude}, {message.longitude}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Location;
