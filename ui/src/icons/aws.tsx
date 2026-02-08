import React from "react";

/* AWS SVG icons — official Architecture Icon color palette */

const bg = "#232F3E";

export const AwsVpc: React.FC = () => (
  <svg viewBox="0 0 80 80"><rect x="2" y="2" width="76" height="76" rx="5" fill={bg}/><path d="M40 15v50M15 40h50" stroke="#8C4FFF" strokeWidth="1.5" opacity=".25"/><rect x="16" y="16" width="48" height="48" rx="3" fill="none" stroke="#8C4FFF" strokeWidth="2"/><path d="M40 22v8M40 50v8M22 40h8M50 40h8" stroke="#8C4FFF" strokeWidth="2"/><circle cx="40" cy="40" r="6" fill="#8C4FFF"/><text x="40" y="43" textAnchor="middle" fill="white" fontSize="7" fontWeight="bold">VPC</text></svg>
);

export const AwsSubnet: React.FC = () => (
  <svg viewBox="0 0 80 80"><rect x="2" y="2" width="76" height="76" rx="5" fill={bg}/><rect x="14" y="20" width="52" height="40" rx="3" fill="none" stroke="#8C4FFF" strokeWidth="2"/><line x1="14" y1="40" x2="66" y2="40" stroke="#8C4FFF" strokeWidth="1" strokeDasharray="4 2"/><rect x="20" y="26" width="18" height="10" rx="2" fill="#8C4FFF" opacity=".2" stroke="#8C4FFF" strokeWidth="1"/><rect x="42" y="26" width="18" height="10" rx="2" fill="#8C4FFF" opacity=".2" stroke="#8C4FFF" strokeWidth="1"/><rect x="20" y="44" width="18" height="10" rx="2" fill="#8C4FFF" opacity=".15" stroke="#8C4FFF" strokeWidth="1"/><rect x="42" y="44" width="18" height="10" rx="2" fill="#8C4FFF" opacity=".15" stroke="#8C4FFF" strokeWidth="1"/></svg>
);

export const AwsInstance: React.FC = () => (
  <svg viewBox="0 0 80 80"><rect x="2" y="2" width="76" height="76" rx="5" fill={bg}/><rect x="20" y="18" width="40" height="44" rx="3" fill="none" stroke="#ED7100" strokeWidth="2"/><rect x="26" y="24" width="28" height="20" rx="2" fill="#ED7100" opacity=".15"/><path d="M34 34a6 6 0 1112 0" stroke="#ED7100" strokeWidth="2" fill="none"/><circle cx="40" cy="28" r="2" fill="#ED7100"/><rect x="30" y="50" width="20" height="3" rx="1.5" fill="#ED7100" opacity=".5"/><rect x="30" y="55" width="14" height="2" rx="1" fill="#ED7100" opacity=".3"/></svg>
);

export const AwsSecurityGroup: React.FC = () => (
  <svg viewBox="0 0 80 80"><rect x="2" y="2" width="76" height="76" rx="5" fill={bg}/><path d="M40 12L14 26v18c0 14 11.6 27 26 30 14.4-3 26-16 26-30V26L40 12z" fill="none" stroke="#DD344C" strokeWidth="2"/><path d="M40 18L20 29v14c0 10.5 8.7 20.3 20 23 11.3-2.7 20-12.5 20-23V29L40 18z" fill="#DD344C" opacity=".1"/><path d="M33 40l5 5 10-10" stroke="#DD344C" strokeWidth="2.5" fill="none" strokeLinecap="round" strokeLinejoin="round"/></svg>
);

export const AwsDbInstance: React.FC = () => (
  <svg viewBox="0 0 80 80"><rect x="2" y="2" width="76" height="76" rx="5" fill={bg}/><ellipse cx="40" cy="22" rx="22" ry="9" fill="#C925D1" opacity=".15" stroke="#C925D1" strokeWidth="2"/><path d="M18 22v36c0 5 10 9 22 9s22-4 22-9V22" fill="none" stroke="#C925D1" strokeWidth="2"/><ellipse cx="40" cy="40" rx="22" ry="9" fill="none" stroke="#C925D1" strokeWidth="1" opacity=".3"/><ellipse cx="40" cy="58" rx="22" ry="9" fill="none" stroke="#C925D1" strokeWidth="1" opacity=".3"/><text x="40" y="42" textAnchor="middle" fill="#C925D1" fontSize="8" fontWeight="bold" opacity=".7">RDS</text></svg>
);

export const AwsRdsCluster: React.FC = () => (
  <svg viewBox="0 0 80 80"><rect x="2" y="2" width="76" height="76" rx="5" fill={bg}/><ellipse cx="40" cy="22" rx="22" ry="9" fill="#C925D1" opacity=".15" stroke="#C925D1" strokeWidth="2"/><path d="M18 22v36c0 5 10 9 22 9s22-4 22-9V22" fill="none" stroke="#C925D1" strokeWidth="2"/><circle cx="54" cy="52" r="10" fill={bg} stroke="#C925D1" strokeWidth="2"/><path d="M50 52h8M54 48v8" stroke="#C925D1" strokeWidth="1.5"/></svg>
);

export const AwsS3Bucket: React.FC = () => (
  <svg viewBox="0 0 80 80"><rect x="2" y="2" width="76" height="76" rx="5" fill={bg}/><path d="M16 24c0-4 11-7 24-7s24 3 24 7v32c0 4-11 7-24 7S16 60 16 56V24z" fill="#277116" opacity=".12" stroke="#277116" strokeWidth="2"/><ellipse cx="40" cy="24" rx="24" ry="7" fill="#277116" opacity=".2" stroke="#277116" strokeWidth="2"/><path d="M16 38c0 4 11 7 24 7s24-3 24-7" stroke="#277116" strokeWidth="1" opacity=".35"/><text x="40" y="52" textAnchor="middle" fill="#277116" fontSize="9" fontWeight="bold" opacity=".8">S3</text></svg>
);

export const AwsLambdaFunction: React.FC = () => (
  <svg viewBox="0 0 80 80"><rect x="2" y="2" width="76" height="76" rx="5" fill={bg}/><path d="M24 60l10-28h5l8 28h-6l-5-18-8 22h10l2 4H24z" fill="#ED7100"/><text x="58" y="30" fill="#ED7100" fontSize="14" fontWeight="bold" opacity=".5">{"\u03BB"}</text></svg>
);

export const AwsElb: React.FC = () => (
  <svg viewBox="0 0 80 80"><rect x="2" y="2" width="76" height="76" rx="5" fill={bg}/><circle cx="40" cy="40" r="24" fill="none" stroke="#8C4FFF" strokeWidth="2"/><circle cx="28" cy="28" r="5" fill="#8C4FFF" opacity=".3" stroke="#8C4FFF" strokeWidth="1.5"/><circle cx="52" cy="28" r="5" fill="#8C4FFF" opacity=".3" stroke="#8C4FFF" strokeWidth="1.5"/><circle cx="40" cy="52" r="5" fill="#8C4FFF" opacity=".3" stroke="#8C4FFF" strokeWidth="1.5"/><path d="M40 34v12M34 38l6-6 6 6" stroke="#8C4FFF" strokeWidth="2" fill="none" strokeLinecap="round"/></svg>
);

export const AwsIamRole: React.FC = () => (
  <svg viewBox="0 0 80 80"><rect x="2" y="2" width="76" height="76" rx="5" fill={bg}/><circle cx="40" cy="30" r="11" fill="#DD344C" opacity=".15" stroke="#DD344C" strokeWidth="2"/><path d="M22 62c0-10 8-18 18-18s18 8 18 18" fill="#DD344C" opacity=".1" stroke="#DD344C" strokeWidth="2"/><circle cx="40" cy="28" r="4" fill="#DD344C" opacity=".5"/><path d="M36 34h8" stroke="#DD344C" strokeWidth="1.5"/></svg>
);

export const AwsRoute53Record: React.FC = () => (
  <svg viewBox="0 0 80 80"><rect x="2" y="2" width="76" height="76" rx="5" fill={bg}/><circle cx="40" cy="40" r="24" fill="none" stroke="#8C4FFF" strokeWidth="2"/><ellipse cx="40" cy="40" rx="12" ry="24" fill="none" stroke="#8C4FFF" strokeWidth="1.5" opacity=".5"/><line x1="16" y1="40" x2="64" y2="40" stroke="#8C4FFF" strokeWidth="1" opacity=".4"/><line x1="40" y1="16" x2="40" y2="64" stroke="#8C4FFF" strokeWidth="1" opacity=".4"/><text x="40" y="43" textAnchor="middle" fill="#8C4FFF" fontSize="7" fontWeight="bold">53</text></svg>
);

export const AwsCloudfront: React.FC = () => (
  <svg viewBox="0 0 80 80"><rect x="2" y="2" width="76" height="76" rx="5" fill={bg}/><circle cx="40" cy="40" r="22" fill="none" stroke="#8C4FFF" strokeWidth="2"/><circle cx="40" cy="40" r="14" fill="none" stroke="#8C4FFF" strokeWidth="1" opacity=".4"/><circle cx="40" cy="40" r="6" fill="#8C4FFF" opacity=".3"/><path d="M40 18v44M18 40h44" stroke="#8C4FFF" strokeWidth="1" opacity=".25"/></svg>
);

export const AwsDynamodb: React.FC = () => (
  <svg viewBox="0 0 80 80"><rect x="2" y="2" width="76" height="76" rx="5" fill={bg}/><ellipse cx="40" cy="22" rx="22" ry="8" fill="#C925D1" opacity=".15" stroke="#C925D1" strokeWidth="2"/><path d="M18 22v36c0 4.4 10 8 22 8s22-3.6 22-8V22" fill="none" stroke="#C925D1" strokeWidth="2"/><path d="M26 36h28M26 44h20M26 52h24" stroke="#C925D1" strokeWidth="1.5" opacity=".4"/></svg>
);

export const AwsSqs: React.FC = () => (
  <svg viewBox="0 0 80 80"><rect x="2" y="2" width="76" height="76" rx="5" fill={bg}/><rect x="14" y="24" width="52" height="32" rx="4" fill="none" stroke="#E7157B" strokeWidth="2"/><path d="M24 36h20M24 44h14" stroke="#E7157B" strokeWidth="2" opacity=".5"/><circle cx="54" cy="40" r="4" fill="#E7157B" opacity=".4"/><path d="M18 32l4-4M18 48l4 4" stroke="#E7157B" strokeWidth="1.5" opacity=".3"/></svg>
);

export const AwsSns: React.FC = () => (
  <svg viewBox="0 0 80 80"><rect x="2" y="2" width="76" height="76" rx="5" fill={bg}/><rect x="14" y="24" width="52" height="32" rx="4" fill="none" stroke="#E7157B" strokeWidth="2"/><path d="M28 40l8-8v16z" fill="#E7157B" opacity=".6"/><path d="M40 32c8 0 14 3.6 14 8s-6 8-14 8" stroke="#E7157B" strokeWidth="2" fill="none" opacity=".5"/><path d="M42 36c4 0 8 1.8 8 4s-4 4-8 4" stroke="#E7157B" strokeWidth="1.5" fill="none" opacity=".4"/></svg>
);

export const AwsEcs: React.FC = () => (
  <svg viewBox="0 0 80 80"><rect x="2" y="2" width="76" height="76" rx="5" fill={bg}/><rect x="16" y="16" width="48" height="48" rx="4" fill="none" stroke="#ED7100" strokeWidth="2"/><rect x="22" y="22" width="14" height="14" rx="2" fill="#ED7100" opacity=".25" stroke="#ED7100" strokeWidth="1"/><rect x="44" y="22" width="14" height="14" rx="2" fill="#ED7100" opacity=".25" stroke="#ED7100" strokeWidth="1"/><rect x="22" y="44" width="14" height="14" rx="2" fill="#ED7100" opacity=".25" stroke="#ED7100" strokeWidth="1"/><rect x="44" y="44" width="14" height="14" rx="2" fill="#ED7100" opacity=".15" stroke="#ED7100" strokeWidth="1" strokeDasharray="3 2"/></svg>
);

export const AwsInternetGateway: React.FC = () => (
  <svg viewBox="0 0 80 80"><rect x="2" y="2" width="76" height="76" rx="5" fill={bg}/><circle cx="40" cy="40" r="22" fill="none" stroke="#8C4FFF" strokeWidth="2"/><path d="M40 20v40" stroke="#8C4FFF" strokeWidth="2"/><path d="M30 30l10-10 10 10" stroke="#8C4FFF" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round"/><path d="M30 50l10 10 10-10" stroke="#8C4FFF" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round"/></svg>
);

export const AwsNatGateway: React.FC = () => (
  <svg viewBox="0 0 80 80"><rect x="2" y="2" width="76" height="76" rx="5" fill={bg}/><rect x="16" y="16" width="48" height="48" rx="4" fill="none" stroke="#8C4FFF" strokeWidth="2"/><text x="40" y="46" textAnchor="middle" fill="#8C4FFF" fontSize="14" fontWeight="bold">NAT</text></svg>
);

export const AwsEbs: React.FC = () => (
  <svg viewBox="0 0 80 80"><rect x="2" y="2" width="76" height="76" rx="5" fill={bg}/><rect x="22" y="14" width="36" height="52" rx="4" fill="none" stroke="#277116" strokeWidth="2"/><rect x="28" y="22" width="24" height="6" rx="2" fill="#277116" opacity=".25"/><rect x="28" y="32" width="24" height="6" rx="2" fill="#277116" opacity=".2"/><rect x="28" y="42" width="24" height="6" rx="2" fill="#277116" opacity=".15"/></svg>
);

export const AwsSecretsManager: React.FC = () => (
  <svg viewBox="0 0 80 80"><rect x="2" y="2" width="76" height="76" rx="5" fill={bg}/><rect x="22" y="34" width="36" height="28" rx="4" fill="none" stroke="#DD344C" strokeWidth="2"/><path d="M30 34V26a10 10 0 0120 0v8" fill="none" stroke="#DD344C" strokeWidth="2"/><circle cx="40" cy="48" r="4" fill="#DD344C"/><line x1="40" y1="52" x2="40" y2="56" stroke="#DD344C" strokeWidth="2"/></svg>
);
