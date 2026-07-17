import React from "react";
import { Play } from "lucide-react";

const sliders = [
  ["traffic_reduction", "Traffic reduction"],
  ["green_cover_increase", "Green cover"],
  ["industrial_emissions_reduction", "Industrial reduction"],
  ["public_transport_adoption", "Public transport"],
];

export default function ScenarioPanel({ scenario, setScenario, onRun }) {
  return (
    <section className="panel">
      <div className="panel-title">
        <h2>Policy simulation</h2>
        <button onClick={onRun} title="Run simulation">
          <Play size={16} /> Run
        </button>
      </div>
      {sliders.map(([key, label]) => (
        <label className="slider" key={key}>
          <span>
            {label} <b>{scenario[key]}%</b>
          </span>
          <input type="range" min="0" max="100" value={scenario[key]} onChange={(event) => setScenario({ ...scenario, [key]: Number(event.target.value) })} />
        </label>
      ))}
    </section>
  );
}
