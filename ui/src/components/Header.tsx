import React from "react";
import type { ActionCounts } from "../types";

const CloudLogo: React.FC = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="1.5">
    <path d="M2 15s2-4 5-4c1.5 0 2.5 1 3 2 .5-3 2-6 5-6s5 3 5 6-3 6-5 6H7c-3 0-5-2-5-4z"/>
  </svg>
);

interface HeaderProps {
  title: string;
  subtitle: string;
  counts: ActionCounts;
}

export const Header: React.FC<HeaderProps> = ({ title, subtitle, counts }) => (
  <div className="header">
    <div className="header-logo">
      <CloudLogo />
      <div>
        <h1>{title}</h1>
        <p dangerouslySetInnerHTML={{ __html: subtitle }} />
      </div>
    </div>
    <div className="summary-inline">
      {counts.create > 0 && <span><span className="ldot create" />{counts.create} create</span>}
      {counts.update > 0 && <span><span className="ldot update" />{counts.update} update</span>}
      {counts.delete > 0 && <span><span className="ldot delete" />{counts.delete} destroy</span>}
      {counts.replace > 0 && <span><span className="ldot replace" />{counts.replace} replace</span>}
    </div>
  </div>
);
