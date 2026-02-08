import React from "react";

interface LegendProps {
  showConnectionTypes?: boolean;
}

export const Legend: React.FC<LegendProps> = ({ showConnectionTypes = true }) => (
  <div className="legend">
    <div className="legend-item"><div className="ldot create" />Create</div>
    <div className="legend-item"><div className="ldot update" />Update</div>
    <div className="legend-item"><div className="ldot delete" />Destroy</div>
    <div className="legend-item"><div className="ldot replace" />Replace</div>
    {showConnectionTypes && (
      <div className="legend-item" style={{ marginLeft: "auto", opacity: 0.5 }}>
        <span style={{ color: "#4caf50" }}>──</span> new &nbsp;
        <span style={{ color: "#f44336" }}>──</span> removed &nbsp;
        <span style={{ color: "#888" }}>- - -</span> unchanged &nbsp;•&nbsp;
        Scroll to zoom • Drag to pan
      </div>
    )}
  </div>
);
