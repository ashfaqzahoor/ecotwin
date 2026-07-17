import React from "react";
import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

export default function PredictionChart({ data, simulated }) {
  const chartData = data.slice(0, 72).map((row, index) => ({
    hour: row.horizon_hours,
    pm25: row.pm25,
    no2: row.no2,
    temp: row.temperature,
    simulatedPm25: simulated?.[index]?.pm25,
  }));

  return (
    <div className="chart-wrap">
      <ResponsiveContainer width="100%" height={280}>
        <LineChart data={chartData}>
          <XAxis dataKey="hour" tickLine={false} />
          <YAxis tickLine={false} width={42} />
          <Tooltip />
          <Line type="monotone" dataKey="pm25" stroke="#2563eb" strokeWidth={2} dot={false} name="PM2.5 baseline" />
          <Line type="monotone" dataKey="no2" stroke="#7c3aed" strokeWidth={2} dot={false} name="NO2" />
          <Line type="monotone" dataKey="temp" stroke="#dc2626" strokeWidth={2} dot={false} name="Temperature" />
          {simulated && <Line type="monotone" dataKey="simulatedPm25" stroke="#059669" strokeWidth={2} dot={false} name="PM2.5 simulated" />}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
