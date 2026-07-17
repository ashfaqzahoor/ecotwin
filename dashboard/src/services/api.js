const API_BASES = [
  import.meta.env.VITE_API_BASE,
  "http://127.0.0.1:8000/api",
  "http://localhost:8000/api",
].filter(Boolean);

const cities = {
  Delhi: { lat: 28.6139, lon: 77.209, country: "IN" },
  Mumbai: { lat: 19.076, lon: 72.8777, country: "IN" },
  Bengaluru: { lat: 12.9716, lon: 77.5946, country: "IN" },
  Hyderabad: { lat: 17.385, lon: 78.4867, country: "IN" },
  Chennai: { lat: 13.0827, lon: 80.2707, country: "IN" },
  Kolkata: { lat: 22.5726, lon: 88.3639, country: "IN" },
  Pune: { lat: 18.5204, lon: 73.8567, country: "IN" },
  Ahmedabad: { lat: 23.0225, lon: 72.5714, country: "IN" },
  Jaipur: { lat: 26.9124, lon: 75.7873, country: "IN" },
  Lucknow: { lat: 26.8467, lon: 80.9462, country: "IN" },
  Kanpur: { lat: 26.4499, lon: 80.3319, country: "IN" },
  Nagpur: { lat: 21.1458, lon: 79.0882, country: "IN" },
  Indore: { lat: 22.7196, lon: 75.8577, country: "IN" },
  Bhopal: { lat: 23.2599, lon: 77.4126, country: "IN" },
  Patna: { lat: 25.5941, lon: 85.1376, country: "IN" },
  Chandigarh: { lat: 30.7333, lon: 76.7794, country: "IN" },
  Amritsar: { lat: 31.634, lon: 74.8723, country: "IN" },
  Ludhiana: { lat: 30.901, lon: 75.8573, country: "IN" },
  Surat: { lat: 21.1702, lon: 72.8311, country: "IN" },
  Vadodara: { lat: 22.3072, lon: 73.1812, country: "IN" },
  Rajkot: { lat: 22.3039, lon: 70.8022, country: "IN" },
  Kochi: { lat: 9.9312, lon: 76.2673, country: "IN" },
  Thiruvananthapuram: { lat: 8.5241, lon: 76.9366, country: "IN" },
  Coimbatore: { lat: 11.0168, lon: 76.9558, country: "IN" },
  Visakhapatnam: { lat: 17.6868, lon: 83.2185, country: "IN" },
  Vijayawada: { lat: 16.5062, lon: 80.648, country: "IN" },
  Bhubaneswar: { lat: 20.2961, lon: 85.8245, country: "IN" },
  Guwahati: { lat: 26.1445, lon: 91.7362, country: "IN" },
  Jammu: { lat: 32.7266, lon: 74.857, country: "IN" },
  Srinagar: { lat: 34.0837, lon: 74.7973, country: "IN" },
};

function citySeed(city) {
  return [...city].reduce((total, char) => total + char.charCodeAt(0), 0);
}

function wave(hour, offset = 0) {
  return Math.sin(((hour + offset) / 24) * Math.PI * 2);
}

function cityFactor(city) {
  const factors = {
    Delhi: 1.6,
    Kanpur: 1.52,
    Patna: 1.48,
    Lucknow: 1.42,
    Kolkata: 1.34,
    Ludhiana: 1.32,
    Amritsar: 1.28,
    Ahmedabad: 1.25,
    Jaipur: 1.22,
    Mumbai: 1.15,
    Hyderabad: 1.12,
    Chennai: 1,
    Pune: 0.95,
    Jammu: 0.92,
    Srinagar: 0.88,
    Bengaluru: 0.85,
    Kochi: 0.78,
    Thiruvananthapuram: 0.72,
  };
  return factors[city] || 0.95 + (citySeed(city) % 40) / 100;
}

function demoSensors(city = "Delhi") {
  const meta = cities[city] || cities.Delhi;
  const factor = cityFactor(city);
  const seed = citySeed(city);
  return Array.from({ length: 8 }, (_, index) => {
    const hour = index + 2;
    const commute = hour === 8 || hour === 9 ? 1.3 : 1;
    const pm25 = Number((factor * 30 * (1 + 0.18 * wave(hour, -7)) * commute + (seed % 5)).toFixed(2));
    const temperature = Number((26 + factor * 3 + 6 * wave(hour, -5)).toFixed(2));
    return {
      station_id: `${city.toLowerCase()}-central`,
      city,
      observed_at: new Date(Date.now() - (8 - index) * 3600_000).toISOString(),
      pm25,
      pm10: Number((pm25 * 1.82).toFixed(2)),
      no2: Number((pm25 * 0.72 * commute).toFixed(2)),
      o3: Number(Math.max(10, 65 - pm25 * 0.45).toFixed(2)),
      co: Number((0.4 + pm25 / 80).toFixed(2)),
      so2: Number((8 + factor * 4).toFixed(2)),
      temperature,
      humidity: Number((62 - temperature * 0.45).toFixed(2)),
      wind_speed: Number((2 + (index % 4) * 0.7).toFixed(2)),
      pressure: 1006 + index,
      precipitation: index % 3 === 0 ? 0.4 : 0,
      latitude: meta.lat + (index - 4) * 0.012,
      longitude: meta.lon + (4 - index) * 0.013,
      source: "frontend-fallback",
    };
  });
}

function demoPredictions(city = "Delhi", horizon = 72) {
  const latest = demoSensors(city).at(-1);
  return Array.from({ length: horizon }, (_, index) => {
    const hour = index + 1;
    const commute = hour % 24 === 8 || hour % 24 === 18 ? 1.18 : 1;
    const pm25 = Number((latest.pm25 * (1 + 0.12 * wave(hour)) * commute).toFixed(2));
    const temperature = Number((latest.temperature + 4 * wave(hour, -5)).toFixed(2));
    return {
      city,
      horizon_hours: hour,
      predicted_at: new Date(Date.now() + hour * 3600_000).toISOString(),
      pm25,
      pm10: Number((pm25 * 1.8).toFixed(2)),
      no2: Number((latest.no2 * (1 + 0.08 * wave(hour)) * commute).toFixed(2)),
      o3: Number(Math.max(8, latest.o3 * (1 - 0.05 * wave(hour))).toFixed(2)),
      temperature,
      energy_demand: Number((95 + Math.max(0, temperature - 24) * 6.5 + pm25 * 0.35).toFixed(2)),
    };
  });
}

function demoAlerts(city = "Delhi") {
  const peak = Math.max(...demoPredictions(city, 72).map((row) => row.pm25));
  return [
    {
      city,
      pollutant: "pm25",
      severity: peak > 40 ? "critical" : "warning",
      value: Number(peak.toFixed(2)),
      threshold: 15,
      predicted_duration_hours: 72,
      message: `${city} is forecast to exceed the PM2.5 safety threshold.`,
      recommended_action: "Reduce traffic exposure, restrict dust-generating activity, and prioritize public transport.",
    },
  ];
}

function simulateFallback(payload) {
  const baseline = demoPredictions(payload.city, payload.horizon_hours || 72);
  const traffic = (payload.traffic_reduction || 0) / 100;
  const green = (payload.green_cover_increase || 0) / 100;
  const industry = (payload.industrial_emissions_reduction || 0) / 100;
  const transit = (payload.public_transport_adoption || 0) / 100;
  const simulated = baseline.map((row) => ({
    ...row,
    pm25: Number((row.pm25 * (1 - 0.18 * traffic - 0.08 * green - 0.2 * industry - 0.12 * transit)).toFixed(2)),
    pm10: Number((row.pm10 * (1 - 0.1 * traffic - 0.07 * green - 0.18 * industry - 0.07 * transit)).toFixed(2)),
    no2: Number((row.no2 * (1 - 0.28 * traffic - 0.1 * industry - 0.22 * transit)).toFixed(2)),
    temperature: Number((row.temperature * (1 - 0.1 * green)).toFixed(2)),
  }));
  return { city: payload.city, parameters: payload, baseline, simulated };
}

async function request(path, options = {}) {
  let lastError;
  for (const base of API_BASES) {
    try {
      const response = await fetch(`${base}${path}`, {
        headers: { "Content-Type": "application/json" },
        ...options,
      });
      if (!response.ok) throw new Error(`EcoTwin API error: ${response.status}`);
      return response.json();
    } catch (error) {
      lastError = error;
    }
  }
  throw new Error(`Could not reach EcoTwin backend at port 8000. ${lastError?.message || ""}`.trim());
}

export const api = {
  cities: () => request("/sensors/cities").catch(() => cities),
  sensors: (city) => request(`/sensors?city=${encodeURIComponent(city)}`).catch(() => demoSensors(city)),
  predictions: (city, horizon = 72) => request(`/predictions?city=${encodeURIComponent(city)}&horizon_hours=${horizon}`).catch(() => demoPredictions(city, horizon)),
  alerts: (city) => request(`/alerts?city=${encodeURIComponent(city)}`).catch(() => demoAlerts(city)),
  simulate: (payload) => request("/simulation", { method: "POST", body: JSON.stringify(payload) }).catch(() => simulateFallback(payload)),
  ask: (question, city) =>
    request("/assistant", { method: "POST", body: JSON.stringify({ question, city }) }).catch(() => {
      const tomorrow = demoPredictions(city, 24).at(-1);
      return {
        intent: "forecast",
        answer: `Using local fallback data: tomorrow in ${city}, PM2.5 is forecast near ${tomorrow.pm25}, NO2 near ${tomorrow.no2}, and temperature near ${tomorrow.temperature} C.`,
        data: demoPredictions(city, 72),
      };
    }),
};
