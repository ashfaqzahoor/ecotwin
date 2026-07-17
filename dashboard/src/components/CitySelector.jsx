import React from "react";

export default function CitySelector({ cities, value, onChange }) {
  return (
    <label className="field">
      <span>City</span>
      <select value={value} onChange={(event) => onChange(event.target.value)}>
        {Object.keys(cities).map((city) => (
          <option key={city} value={city}>
            {city}
          </option>
        ))}
      </select>
    </label>
  );
}
