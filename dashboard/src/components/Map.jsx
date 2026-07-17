import React from "react";
import "leaflet/dist/leaflet.css";
import { CircleMarker, MapContainer, Popup, TileLayer, useMap, useMapEvents } from "react-leaflet";

function colorFor(pm25) {
  if (pm25 > 55) return "#9b1c31";
  if (pm25 > 35) return "#d97706";
  if (pm25 > 15) return "#facc15";
  return "#16a34a";
}

function RecenterMap({ center }) {
  const map = useMap();
  React.useEffect(() => {
    map.setView(center, 11, { animate: true });
  }, [center[0], center[1], map]);
  return null;
}

function distanceKm(a, b) {
  const toRad = (value) => (value * Math.PI) / 180;
  const earthKm = 6371;
  const dLat = toRad(b.lat - a.lat);
  const dLon = toRad(b.lng - a.lng);
  const lat1 = toRad(a.lat);
  const lat2 = toRad(b.lat);
  const h = Math.sin(dLat / 2) ** 2 + Math.cos(lat1) * Math.cos(lat2) * Math.sin(dLon / 2) ** 2;
  return earthKm * 2 * Math.atan2(Math.sqrt(h), Math.sqrt(1 - h));
}

function estimateAtPoint(latlng, readings, cityMeta) {
  const usable = readings.filter((row) => row.latitude && row.longitude);
  if (!usable.length) return null;
  const weighted = usable.map((row) => {
    const km = distanceKm({ lat: row.latitude, lng: row.longitude }, latlng);
    return { row, weight: 1 / Math.max(0.8, km) };
  });
  const totalWeight = weighted.reduce((sum, item) => sum + item.weight, 0);
  const value = (key) => weighted.reduce((sum, item) => sum + Number(item.row[key] || 0) * item.weight, 0) / totalWeight;
  const centerDistance = cityMeta ? distanceKm({ lat: cityMeta.lat, lng: cityMeta.lon }, latlng) : 0;
  const edgeFactor = Math.min(1.2, 1 + centerDistance / 250);
  const pm25 = value("pm25") * edgeFactor;
  const no2 = value("no2") * edgeFactor;
  const temperature = value("temperature") + Math.min(2.5, centerDistance / 35);
  return {
    lat: latlng.lat.toFixed(4),
    lng: latlng.lng.toFixed(4),
    pm25: pm25.toFixed(2),
    pm10: (value("pm10") * edgeFactor).toFixed(2),
    no2: no2.toFixed(2),
    o3: value("o3").toFixed(2),
    temperature: temperature.toFixed(2),
    energy: (95 + Math.max(0, temperature - 24) * 6.5 + pm25 * 0.35).toFixed(2),
    severity: pm25 > 55 || no2 > 45 ? "Critical" : pm25 > 35 || no2 > 25 ? "Warning" : "Normal",
  };
}

function ClickInspector({ readings, cityMeta }) {
  const [inspection, setInspection] = React.useState(null);
  useMapEvents({
    click(event) {
      setInspection(estimateAtPoint(event.latlng, readings, cityMeta));
    },
  });
  if (!inspection) return null;
  return (
    <Popup position={[Number(inspection.lat), Number(inspection.lng)]}>
      <strong>Selected location</strong>
      <br />
      Lat/Lon: {inspection.lat}, {inspection.lng}
      <br />
      PM2.5: {inspection.pm25} ug/m3
      <br />
      PM10: {inspection.pm10} ug/m3
      <br />
      NO2: {inspection.no2} ug/m3
      <br />
      O3: {inspection.o3} ug/m3
      <br />
      Temperature: {inspection.temperature} C
      <br />
      Energy demand: {inspection.energy} MWh
      <br />
      Alert level: {inspection.severity}
    </Popup>
  );
}

export default function TwinMap({ readings, cityMeta }) {
  const center = cityMeta ? [cityMeta.lat, cityMeta.lon] : [28.6139, 77.2090];
  return (
    <MapContainer center={center} zoom={11} className="map" scrollWheelZoom>
      <RecenterMap center={center} />
      <ClickInspector readings={readings} cityMeta={cityMeta} />
      <TileLayer attribution="&copy; OpenStreetMap" url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      {readings.map((row, idx) => (
        <CircleMarker
          key={`${row.station_id}-${idx}`}
          center={[row.latitude, row.longitude]}
          radius={12}
          pathOptions={{ color: colorFor(row.pm25), fillColor: colorFor(row.pm25), fillOpacity: 0.62 }}
        >
          <Popup>
            <strong>{row.city}</strong>
            <br />
            PM2.5: {row.pm25}
            <br />
            NO2: {row.no2}
            <br />
            Temperature: {row.temperature} C
          </Popup>
        </CircleMarker>
      ))}
    </MapContainer>
  );
}
