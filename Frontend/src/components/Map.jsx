import { GoogleMap, LoadScript, Marker } from "@react-google-maps/api";
import React from "react";

const Map = ({ coordinates, handleMapClick, handleMarkerDrag }) => {
  const mapStyles = {
    height: "400px",
    width: "800px",
  };

  const defaultCenter = {
    lat: 40.712776, // New York
    lng: -74.005974,
  };

  const handleMapClickInternal = (e) => {
    const lat = e.latLng.lat();
    const lng = e.latLng.lng();
    handleMapClick(lat, lng);
  };

  return (
    <LoadScript googleMapsApiKey="AIzaSyBD9TzCsljMc19-ZSoiBJrbuycySEBpirE">
      <GoogleMap
        mapContainerStyle={mapStyles}
        zoom={12}
        center={defaultCenter}
        onClick={handleMapClickInternal}
      >
        {coordinates.departure.lat && (
          <Marker
            position={coordinates.departure}
            onDragEnd={(e) => handleMarkerDrag(e, "departure")}
            draggable={true}
          />
        )}
        {coordinates.destination.lat && (
          <Marker
            position={coordinates.destination}
            onDragEnd={(e) => handleMarkerDrag(e, "destination")}
            draggable={true}
          />
        )}
      </GoogleMap>
    </LoadScript>
  );
};

export default Map;
