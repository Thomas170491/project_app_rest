import React, { useEffect, useRef } from "react";

const Location = () => {
  const token = localStorage.getItem("access_token");
  const user = JSON.parse(localStorage.getItem("user"));

  const targetUser = "2";
  const wsRef = useRef(null);

  useEffect(() => {
    wsRef.current = new WebSocket(
      `ws://localhost:8000/ws/ride-share/?token=${token}`
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
        wsRef.current.send(JSON.stringify({ latitude, longitude, targetUser }));
      }
    };

    const handleError = (error) => {
      console.log("Error getting location: ", error);
    };

    if (navigator.geolocation) {
      navigator.geolocation.watchPosition(sendLocation, handleError);
    } else {
      console.error("Geolocation is not supported by this browser");
    }
  }, []);

  return (
    <div>
      <h1>Sending Your Location.....</h1>
      <p>Here map will be added later</p>
    </div>
  );
};

export default Location;
