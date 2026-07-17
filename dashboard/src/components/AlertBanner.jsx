import React from "react";
import { AlertTriangle } from "lucide-react";

export default function AlertBanner({ alerts }) {
  if (!alerts.length) return <div className="alert ok">No active WHO-threshold alerts for the selected city.</div>;
  return (
    <div className="alert warning">
      <AlertTriangle size={18} />
      <div>
        <strong>{alerts[0].severity.toUpperCase()} alert:</strong> {alerts[0].message} Peak {alerts[0].pollutant.toUpperCase()} is {alerts[0].value}.
      </div>
    </div>
  );
}
