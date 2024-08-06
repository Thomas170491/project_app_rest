import React, { useEffect, useRef, useState } from "react";
const baseUrl = import.meta.env.VITE_REACT_APP_WEBSOCKET_URL;

const Location = () => {
  const token = localStorage.getItem("access_token");
  const user = JSON.parse(localStorage.getItem("user"));
  const [userInfo, setUserInfo] = useState([]); // Me
  const [targetUserInfo, setTargetUserInfo] = useState([]); // Target User

  const targetUser = "2";
  const wsRef = useRef(null);

  useEffect(() => {
    wsRef.current = new WebSocket(
      `wss://${baseUrl}/ws/ride-share/?token=${token}`
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
        // let latitude = 1111.111;
        // let longitude = 1111.111;
        wsRef.current.send(JSON.stringify({ latitude, longitude, targetUser }));
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

  return (
    <div>
      <h1>Sending Your Location.....</h1>
      <p>Here map will be added later</p>
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
