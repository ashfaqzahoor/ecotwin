import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import { Bot, RefreshCw } from "lucide-react";
import AlertBanner from "./components/AlertBanner.jsx";
import CitySelector from "./components/CitySelector.jsx";
import TwinMap from "./components/Map.jsx";
import PredictionChart from "./components/PredictionChart.jsx";
import ScenarioPanel from "./components/ScenarioPanel.jsx";
import { api } from "./services/api.js";
import "./styles.css";

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { error: null };
  }

  static getDerivedStateFromError(error) {
    return { error };
  }

  render() {
    if (this.state.error) {
      return (
        <main>
          <section className="panel error-panel">
            <h1>EcoTwin-FM could not render</h1>
            <p>{this.state.error.message}</p>
          </section>
        </main>
      );
    }
    return this.props.children;
  }
}

function App() {
  const [cities, setCities] = useState({});
  const [city, setCity] = useState("Delhi");
  const [readings, setReadings] = useState([]);
  const [forecast, setForecast] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [simulated, setSimulated] = useState(null);
  const [question, setQuestion] = useState("What will be the AQI tomorrow?");
  const [answer, setAnswer] = useState("");
  const [loadError, setLoadError] = useState("");
  const [scenario, setScenario] = useState({ traffic_reduction: 20, green_cover_increase: 10, industrial_emissions_reduction: 0, public_transport_adoption: 15 });

  async function load(selectedCity = city) {
    setLoadError("");
    const results = await Promise.allSettled([api.cities(), api.sensors(selectedCity), api.predictions(selectedCity), api.alerts(selectedCity)]);
    const [cityList, live, pred, alertList] = results;
    if (cityList.status === "fulfilled") setCities(cityList.value);
    if (live.status === "fulfilled") setReadings(live.value);
    if (pred.status === "fulfilled") setForecast(pred.value);
    if (alertList.status === "fulfilled") setAlerts(alertList.value);
    const failures = results.filter((result) => result.status === "rejected");
    if (failures.length) {
      setLoadError(failures[0].reason.message);
    }
    setSimulated(null);
  }

  useEffect(() => {
    load(city).catch((error) => setLoadError(error.message));
  }, [city]);

  const latest = readings[readings.length - 1] || {};
  const cityMeta = cities[city];
  const kpis = useMemo(
    () => [
      ["PM2.5", latest.pm25, "ug/m3"],
      ["NO2", latest.no2, "ug/m3"],
      ["Temperature", latest.temperature, "C"],
      ["Energy demand", forecast[23]?.energy_demand, "MWh"],
    ],
    [latest, forecast]
  );

  async function runScenario() {
    try {
      const result = await api.simulate({ city, horizon_hours: 72, ...scenario });
      setSimulated(result.simulated);
      setAnswer("");
    } catch (error) {
      setAnswer(error.message);
    }
  }

  async function askAssistant() {
    try {
      const response = await api.ask(question, city);
      setAnswer(response.answer);
      if (response.intent === "simulation") setSimulated(response.data.simulated);
    } catch (error) {
      setAnswer(error.message);
    }
  }

  return (
    <main>
      <header className="topbar">
        <div>
          <h1>EcoTwin-FM</h1>
          <p>Environmental smart city digital twin</p>
        </div>
        <div className="controls">
          <CitySelector cities={cities} value={city} onChange={setCity} />
          <button onClick={() => load(city)} title="Refresh data">
            <RefreshCw size={16} /> Refresh
          </button>
        </div>
      </header>

      {loadError && <div className="alert warning">{loadError}</div>}
      <AlertBanner alerts={alerts} />

      <section className="kpis">
        {kpis.map(([label, value, unit]) => (
          <div className="kpi" key={label}>
            <span>{label}</span>
            <strong>{value ?? "--"}</strong>
            <small>{unit}</small>
          </div>
        ))}
      </section>

      <section className="grid">
        <TwinMap readings={readings} cityMeta={cityMeta} />
        <div className="stack">
          <section className="panel">
            <h2>72-hour forecast</h2>
            <PredictionChart data={forecast} simulated={simulated} />
          </section>
          <ScenarioPanel scenario={scenario} setScenario={setScenario} onRun={runScenario} />
        </div>
      </section>

      <section className="assistant panel">
        <h2><Bot size={18} /> Policy assistant</h2>
        <div className="ask">
          <input value={question} onChange={(event) => setQuestion(event.target.value)} />
          <button onClick={askAssistant}>Ask</button>
        </div>
        {answer && <p>{answer}</p>}
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")).render(
  <ErrorBoundary>
    <App />
  </ErrorBoundary>
);
