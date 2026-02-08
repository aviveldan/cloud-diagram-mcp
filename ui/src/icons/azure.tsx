import React from "react";

/* Azure SVG icons — official #0078D4 palette */

const bg = "#1B1B1F";
const az = "#0078D4";

export const AzureResourceGroup: React.FC = () => (
  <svg viewBox="0 0 80 80"><rect x="2" y="2" width="76" height="76" rx="5" fill={bg}/><rect x="14" y="18" width="52" height="44" rx="4" fill="none" stroke={az} strokeWidth="2"/><rect x="14" y="18" width="52" height="12" rx="4" fill={az} opacity=".15"/><rect x="20" y="22" width="16" height="4" rx="2" fill={az} opacity=".5"/><rect x="22" y="38" width="12" height="12" rx="2" fill={az} opacity=".15" stroke={az} strokeWidth="1"/><rect x="40" y="38" width="12" height="12" rx="2" fill={az} opacity=".15" stroke={az} strokeWidth="1"/><rect x="31" y="52" width="12" height="6" rx="2" fill={az} opacity=".1" stroke={az} strokeWidth="1"/></svg>
);

export const AzureVirtualNetwork: React.FC = () => (
  <svg viewBox="0 0 80 80"><rect x="2" y="2" width="76" height="76" rx="5" fill={bg}/><rect x="14" y="14" width="52" height="52" rx="4" fill="none" stroke={az} strokeWidth="2"/><circle cx="28" cy="28" r="5" fill={az} opacity=".3" stroke={az} strokeWidth="1.5"/><circle cx="52" cy="28" r="5" fill={az} opacity=".3" stroke={az} strokeWidth="1.5"/><circle cx="28" cy="52" r="5" fill={az} opacity=".3" stroke={az} strokeWidth="1.5"/><circle cx="52" cy="52" r="5" fill={az} opacity=".3" stroke={az} strokeWidth="1.5"/><line x1="33" y1="28" x2="47" y2="28" stroke={az} strokeWidth="1.5"/><line x1="28" y1="33" x2="28" y2="47" stroke={az} strokeWidth="1.5"/><line x1="52" y1="33" x2="52" y2="47" stroke={az} strokeWidth="1.5"/><line x1="33" y1="52" x2="47" y2="52" stroke={az} strokeWidth="1.5"/><line x1="33" y1="33" x2="47" y2="47" stroke={az} strokeWidth="1" opacity=".4"/></svg>
);

export const AzureSubnet: React.FC = () => (
  <svg viewBox="0 0 80 80"><rect x="2" y="2" width="76" height="76" rx="5" fill={bg}/><rect x="14" y="20" width="52" height="40" rx="3" fill="none" stroke={az} strokeWidth="2"/><line x1="40" y1="20" x2="40" y2="60" stroke={az} strokeWidth="1" strokeDasharray="4 2" opacity=".4"/><rect x="18" y="28" width="18" height="10" rx="2" fill={az} opacity=".12" stroke={az} strokeWidth="1"/><rect x="44" y="28" width="18" height="10" rx="2" fill={az} opacity=".12" stroke={az} strokeWidth="1"/><rect x="18" y="44" width="18" height="10" rx="2" fill={az} opacity=".08" stroke={az} strokeWidth="1"/></svg>
);

export const AzureVm: React.FC = () => (
  <svg viewBox="0 0 80 80"><rect x="2" y="2" width="76" height="76" rx="5" fill={bg}/><rect x="18" y="14" width="44" height="34" rx="3" fill="none" stroke={az} strokeWidth="2"/><rect x="22" y="18" width="36" height="26" rx="1" fill={az} opacity=".1"/><path d="M32 34l8-10 8 10z" fill={az} opacity=".4"/><rect x="28" y="52" width="24" height="4" rx="2" fill={az} opacity=".4"/><line x1="40" y1="48" x2="40" y2="52" stroke={az} strokeWidth="2"/><rect x="24" y="58" width="32" height="3" rx="1.5" fill={az} opacity=".2"/></svg>
);

export const AzureLinuxVm: React.FC = () => (
  <svg viewBox="0 0 80 80"><rect x="2" y="2" width="76" height="76" rx="5" fill={bg}/><rect x="18" y="14" width="44" height="34" rx="3" fill="none" stroke={az} strokeWidth="2"/><rect x="22" y="18" width="36" height="26" rx="1" fill={az} opacity=".1"/><text x="40" y="35" textAnchor="middle" fill={az} fontSize="10" fontWeight="bold">{"\uD83D\uDC27"}</text><rect x="28" y="52" width="24" height="4" rx="2" fill={az} opacity=".4"/><line x1="40" y1="48" x2="40" y2="52" stroke={az} strokeWidth="2"/></svg>
);

export const AzureStorageAccount: React.FC = () => (
  <svg viewBox="0 0 80 80"><rect x="2" y="2" width="76" height="76" rx="5" fill={bg}/><rect x="16" y="22" width="48" height="36" rx="3" fill="none" stroke={az} strokeWidth="2"/><rect x="16" y="22" width="48" height="10" rx="3" fill={az} opacity=".15"/><rect x="16" y="36" width="48" height="10" fill={az} opacity=".08"/><circle cx="56" cy="27" r="2" fill="#4caf50"/><circle cx="56" cy="41" r="2" fill="#4caf50"/><circle cx="56" cy="53" r="2" fill="#ff9800" opacity=".5"/></svg>
);

export const AzureStorageBlob: React.FC = () => (
  <svg viewBox="0 0 80 80"><rect x="2" y="2" width="76" height="76" rx="5" fill={bg}/><path d="M16 28c0-4 11-7 24-7s24 3 24 7v24c0 4-11 7-24 7S16 56 16 52V28z" fill={az} opacity=".1" stroke={az} strokeWidth="2"/><ellipse cx="40" cy="28" rx="24" ry="7" fill={az} opacity=".2"/></svg>
);

export const AzureAppService: React.FC = () => (
  <svg viewBox="0 0 80 80"><rect x="2" y="2" width="76" height="76" rx="5" fill={bg}/><circle cx="40" cy="40" r="22" fill="none" stroke={az} strokeWidth="2"/><circle cx="40" cy="40" r="22" fill={az} opacity=".08"/><path d="M30 28l20 12-20 12z" fill={az} opacity=".6"/></svg>
);

export const AzureFunctionApp: React.FC = () => (
  <svg viewBox="0 0 80 80"><rect x="2" y="2" width="76" height="76" rx="5" fill={bg}/><path d="M40 14L18 28v24l22 14 22-14V28L40 14z" fill={az} opacity=".1" stroke={az} strokeWidth="2"/><path d="M32 52l6-16h4l-3 10h6l-10 12 3-8h-6z" fill={az}/></svg>
);

export const AzureSqlServer: React.FC = () => (
  <svg viewBox="0 0 80 80"><rect x="2" y="2" width="76" height="76" rx="5" fill={bg}/><ellipse cx="40" cy="22" rx="22" ry="8" fill={az} opacity=".15" stroke={az} strokeWidth="2"/><path d="M18 22v36c0 4.4 10 8 22 8s22-3.6 22-8V22" fill="none" stroke={az} strokeWidth="2"/><text x="40" y="50" textAnchor="middle" fill={az} fontSize="9" fontWeight="bold" opacity=".6">SQL</text></svg>
);

export const AzureCosmosDb: React.FC = () => (
  <svg viewBox="0 0 80 80"><rect x="2" y="2" width="76" height="76" rx="5" fill={bg}/><circle cx="40" cy="40" r="22" fill="none" stroke={az} strokeWidth="2"/><ellipse cx="40" cy="40" rx="22" ry="10" fill="none" stroke={az} strokeWidth="1.5" transform="rotate(30 40 40)" opacity=".5"/><ellipse cx="40" cy="40" rx="22" ry="10" fill="none" stroke={az} strokeWidth="1.5" transform="rotate(-30 40 40)" opacity=".5"/><circle cx="40" cy="40" r="5" fill={az} opacity=".4"/></svg>
);

export const AzureNsg: React.FC = () => (
  <svg viewBox="0 0 80 80"><rect x="2" y="2" width="76" height="76" rx="5" fill={bg}/><path d="M40 12L14 26v18c0 14 11.6 27 26 30 14.4-3 26-16 26-30V26L40 12z" fill={az} opacity=".08" stroke={az} strokeWidth="2"/><path d="M33 40l5 5 10-10" stroke={az} strokeWidth="2.5" fill="none" strokeLinecap="round" strokeLinejoin="round"/></svg>
);

export const AzureLb: React.FC = () => (
  <svg viewBox="0 0 80 80"><rect x="2" y="2" width="76" height="76" rx="5" fill={bg}/><circle cx="40" cy="40" r="22" fill="none" stroke={az} strokeWidth="2"/><path d="M40 24v10" stroke={az} strokeWidth="2"/><path d="M30 46l10-8 10 8" stroke={az} strokeWidth="2" fill="none"/><circle cx="30" cy="52" r="4" fill={az} opacity=".3" stroke={az} strokeWidth="1"/><circle cx="50" cy="52" r="4" fill={az} opacity=".3" stroke={az} strokeWidth="1"/></svg>
);

export const AzureAppGateway: React.FC = () => (
  <svg viewBox="0 0 80 80"><rect x="2" y="2" width="76" height="76" rx="5" fill={bg}/><rect x="14" y="14" width="52" height="52" rx="4" fill="none" stroke={az} strokeWidth="2"/><path d="M14 40h18l8-10 8 10h18" stroke={az} strokeWidth="2" fill="none"/><circle cx="40" cy="40" r="4" fill={az}/></svg>
);
