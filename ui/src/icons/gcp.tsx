import React from "react";

/* GCP SVG icons — Google brand colors */

const bg = "#1A2332";

export const GcpComputeInstance: React.FC = () => (
  <svg viewBox="0 0 80 80"><rect x="2" y="2" width="76" height="76" rx="5" fill={bg}/><rect x="22" y="18" width="36" height="44" rx="3" fill="none" stroke="#4285F4" strokeWidth="2"/><rect x="28" y="24" width="24" height="16" rx="2" fill="#4285F4" opacity=".15"/><circle cx="40" cy="32" r="4" fill="#4285F4" opacity=".5"/><rect x="30" y="46" width="20" height="3" rx="1.5" fill="#4285F4" opacity=".4"/><rect x="30" y="52" width="14" height="3" rx="1.5" fill="#4285F4" opacity=".25"/><line x1="16" y1="30" x2="22" y2="30" stroke="#34A853" strokeWidth="2"/><line x1="16" y1="40" x2="22" y2="40" stroke="#EA4335" strokeWidth="2"/><line x1="16" y1="50" x2="22" y2="50" stroke="#FBBC04" strokeWidth="2"/><line x1="58" y1="30" x2="64" y2="30" stroke="#34A853" strokeWidth="2"/><line x1="58" y1="40" x2="64" y2="40" stroke="#EA4335" strokeWidth="2"/><line x1="58" y1="50" x2="64" y2="50" stroke="#FBBC04" strokeWidth="2"/></svg>
);

export const GcpComputeNetwork: React.FC = () => (
  <svg viewBox="0 0 80 80"><rect x="2" y="2" width="76" height="76" rx="5" fill={bg}/><rect x="14" y="14" width="52" height="52" rx="4" fill="none" stroke="#4285F4" strokeWidth="2"/><circle cx="28" cy="28" r="4" fill="#4285F4" opacity=".4" stroke="#4285F4" strokeWidth="1"/><circle cx="52" cy="28" r="4" fill="#34A853" opacity=".4" stroke="#34A853" strokeWidth="1"/><circle cx="28" cy="52" r="4" fill="#FBBC04" opacity=".4" stroke="#FBBC04" strokeWidth="1"/><circle cx="52" cy="52" r="4" fill="#EA4335" opacity=".4" stroke="#EA4335" strokeWidth="1"/><line x1="32" y1="28" x2="48" y2="28" stroke="#4285F4" strokeWidth="1.5" opacity=".5"/><line x1="28" y1="32" x2="28" y2="48" stroke="#4285F4" strokeWidth="1.5" opacity=".5"/><line x1="32" y1="52" x2="48" y2="52" stroke="#4285F4" strokeWidth="1.5" opacity=".5"/><line x1="52" y1="32" x2="52" y2="48" stroke="#4285F4" strokeWidth="1.5" opacity=".5"/></svg>
);

export const GcpSubnetwork: React.FC = () => (
  <svg viewBox="0 0 80 80"><rect x="2" y="2" width="76" height="76" rx="5" fill={bg}/><rect x="14" y="20" width="52" height="40" rx="3" fill="none" stroke="#4285F4" strokeWidth="2"/><line x1="40" y1="20" x2="40" y2="60" stroke="#4285F4" strokeWidth="1" strokeDasharray="4 2" opacity=".4"/><rect x="18" y="28" width="18" height="10" rx="2" fill="#4285F4" opacity=".12" stroke="#4285F4" strokeWidth="1"/><rect x="44" y="28" width="18" height="10" rx="2" fill="#34A853" opacity=".12" stroke="#34A853" strokeWidth="1"/></svg>
);

export const GcpStorageBucket: React.FC = () => (
  <svg viewBox="0 0 80 80"><rect x="2" y="2" width="76" height="76" rx="5" fill={bg}/><path d="M16 26c0-4 11-7 24-7s24 3 24 7v28c0 4-11 7-24 7S16 58 16 54V26z" fill="#4285F4" opacity=".08" stroke="#4285F4" strokeWidth="2"/><ellipse cx="40" cy="26" rx="24" ry="7" fill="#4285F4" opacity=".15" stroke="#4285F4" strokeWidth="1.5"/><path d="M16 38c0 4 11 7 24 7s24-3 24-7" stroke="#4285F4" strokeWidth="1" opacity=".3"/><path d="M16 50c0 4 11 7 24 7s24-3 24-7" stroke="#4285F4" strokeWidth="1" opacity=".2"/></svg>
);

export const GcpSqlInstance: React.FC = () => (
  <svg viewBox="0 0 80 80"><rect x="2" y="2" width="76" height="76" rx="5" fill={bg}/><ellipse cx="40" cy="22" rx="22" ry="8" fill="#4285F4" opacity=".12" stroke="#4285F4" strokeWidth="2"/><path d="M18 22v36c0 4.4 10 8 22 8s22-3.6 22-8V22" fill="none" stroke="#4285F4" strokeWidth="2"/><ellipse cx="40" cy="40" rx="22" ry="8" fill="none" stroke="#4285F4" strokeWidth="1" opacity=".25"/><text x="40" y="50" textAnchor="middle" fill="#4285F4" fontSize="8" fontWeight="bold" opacity=".5">SQL</text></svg>
);

export const GcpFirestore: React.FC = () => (
  <svg viewBox="0 0 80 80"><rect x="2" y="2" width="76" height="76" rx="5" fill={bg}/><path d="M28 16l12 24-12 24" stroke="#FBBC04" strokeWidth="2.5" fill="none"/><path d="M40 24l12 16-12 24" stroke="#EA4335" strokeWidth="2.5" fill="none"/></svg>
);

export const GcpForwardingRule: React.FC = () => (
  <svg viewBox="0 0 80 80"><rect x="2" y="2" width="76" height="76" rx="5" fill={bg}/><circle cx="40" cy="40" r="22" fill="none" stroke="#4285F4" strokeWidth="2"/><path d="M28 40h24M44 34l8 6-8 6" stroke="#4285F4" strokeWidth="2.5" fill="none" strokeLinecap="round" strokeLinejoin="round"/></svg>
);

export const GcpGke: React.FC = () => (
  <svg viewBox="0 0 80 80"><rect x="2" y="2" width="76" height="76" rx="5" fill={bg}/><circle cx="40" cy="40" r="22" fill="none" stroke="#4285F4" strokeWidth="2"/><circle cx="40" cy="26" r="5" fill="#4285F4" opacity=".3" stroke="#4285F4" strokeWidth="1.5"/><circle cx="28" cy="50" r="5" fill="#34A853" opacity=".3" stroke="#34A853" strokeWidth="1.5"/><circle cx="52" cy="50" r="5" fill="#EA4335" opacity=".3" stroke="#EA4335" strokeWidth="1.5"/><line x1="40" y1="31" x2="31" y2="46" stroke="#4285F4" strokeWidth="1.5" opacity=".4"/><line x1="40" y1="31" x2="49" y2="46" stroke="#4285F4" strokeWidth="1.5" opacity=".4"/><line x1="33" y1="50" x2="47" y2="50" stroke="#4285F4" strokeWidth="1.5" opacity=".4"/></svg>
);
