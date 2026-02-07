#!/usr/bin/env python3
"""
Cloud Diff MCP Server
FastMCP server that visualizes Terraform plan changes as an interactive MCP App.

Uses the MCP Apps pattern:
- Tool linked to a ui:// resource via ToolUI
- HTML resource with the @modelcontextprotocol/ext-apps JS SDK
- Tool returns structured plan data; the UI renders it client-side
"""

from __future__ import annotations

import json
from typing import Any

from fastmcp import FastMCP
from fastmcp.server.apps import ResourceCSP, ResourceUI, ToolUI

mcp = FastMCP("cloud-diff-mcp")

VIEW_URI = "ui://cloud-diff/visualization"


# ---------------------------------------------------------------------------
# Embedded HTML — receives tool result via ext-apps SDK, renders client-side
# ---------------------------------------------------------------------------

EMBEDDED_VIEW_HTML: str = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="color-scheme" content="light dark">
  <style>
    *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
    html, body { height: 100%; overflow: hidden; background: transparent; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      color: #e0e0e0; display: flex; flex-direction: column;
    }
    /* ---- Header ---- */
    .header {
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
      color: white; padding: 10px 16px; flex-shrink: 0;
      display: flex; align-items: center; gap: 12px;
      border-bottom: 1px solid #333;
    }
    .header-logo { display: flex; align-items: center; gap: 8px; }
    .header-logo svg { width: 22px; height: 22px; }
    .header h1 { font-size: 15px; font-weight: 700; }
    .header p  { opacity: .7; font-size: 11px; margin-top: 1px; }
    .summary-inline {
      margin-left: auto; display: flex; gap: 12px; font-size: 11px; font-weight: 600;
    }
    .summary-inline span { display: flex; align-items: center; gap: 4px; }
    /* ---- Main content ---- */
    .content { flex: 1; display: flex; overflow: hidden; }
    .canvas-wrap {
      flex: 1; min-width: 0; padding: 16px; overflow: auto; position: relative;
      background: #111 radial-gradient(circle at 1px 1px, rgba(255,255,255,.03) 1px, transparent 0);
      background-size: 20px 20px;
    }
    .arch-diagram { position: relative; padding-bottom: 20px; }
    /* ---- Sidebar ---- */
    .sidebar {
      width: 280px; flex-shrink: 0; padding: 14px; overflow-y: auto;
      background: #161616; border-left: 1px solid #2a2a2a;
    }
    .placeholder { text-align: center; padding: 40px 10px; color: #444; }
    .placeholder svg { width: 40px; height: 40px; opacity: .25; margin-bottom: 8px; }
    .placeholder p { font-size: 12px; }
    /* ---- Cluster ---- */
    .cluster {
      border: 1px solid rgba(255,255,255,.08); border-radius: 10px;
      padding: 10px 12px; margin-bottom: 12px;
      background: rgba(255,255,255,.015);
    }
    .cluster-header {
      display: flex; align-items: center; gap: 6px;
      margin-bottom: 10px; padding-bottom: 6px;
      border-bottom: 1px solid rgba(255,255,255,.06);
    }
    .cluster-header .cl-icon { width: 16px; height: 16px; opacity: .7; }
    .cluster-header .cl-icon svg { width: 100%; height: 100%; }
    .cluster-header .cl-title {
      font-size: 10px; text-transform: uppercase; letter-spacing: .8px;
      color: #777; font-weight: 700;
    }
    .cluster-resources { display: flex; flex-wrap: wrap; gap: 8px; }
    /* ---- Resource card ---- */
    .res-card {
      width: 100px; display: flex; flex-direction: column; align-items: center;
      padding: 10px 6px 8px; border-radius: 8px; cursor: pointer;
      transition: all .15s; border: 1.5px solid transparent;
      background: rgba(25,25,35,.8); position: relative;
    }
    .res-card:hover { background: rgba(50,50,65,.9); transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,0,0,.4); }
    .res-card.selected { border-color: #667eea; background: rgba(102,126,234,.1); }
    .res-card .res-icon { width: 40px; height: 40px; margin-bottom: 6px; }
    .res-card .res-icon svg { width: 100%; height: 100%; }
    .res-card .res-name { font-size: 10px; font-weight: 600; text-align: center; line-height: 1.2; color: #ddd; word-break: break-word; }
    .res-card .res-type { font-size: 9px; color: #666; font-family: monospace; text-align: center; margin-top: 2px; }
    .res-card .action-dot {
      position: absolute; top: 5px; right: 5px;
      width: 8px; height: 8px; border-radius: 50%;
    }
    .action-dot.create  { background: #4caf50; box-shadow: 0 0 4px #4caf50; }
    .action-dot.delete  { background: #f44336; box-shadow: 0 0 4px #f44336; }
    .action-dot.update  { background: #ff9800; box-shadow: 0 0 4px #ff9800; }
    .action-dot.replace { background: #9c27b0; box-shadow: 0 0 4px #9c27b0; }
    .action-tag {
      font-size: 8px; font-weight: 700; text-transform: uppercase;
      padding: 1px 5px; border-radius: 4px; margin-top: 4px; letter-spacing: .3px;
    }
    .action-tag.create  { background: #1b5e20; color: #a5d6a7; }
    .action-tag.delete  { background: #b71c1c; color: #ef9a9a; }
    .action-tag.update  { background: #e65100; color: #ffcc80; }
    .action-tag.replace { background: #4a148c; color: #ce93d8; }
    /* ---- Connection arrows ---- */
    .conn-svg {
      position: absolute; top: 0; left: 0;
      pointer-events: none; z-index: 0; overflow: visible;
    }
    .conn-svg path {
      fill: none; stroke-width: 1.5; stroke-dasharray: 5 3;
      marker-end: url(#arr);
    }
    /* ---- Server SVG mode ---- */
    .svg-viewport {
      width: 100%; height: 100%; overflow: hidden;
      cursor: grab; position: relative;
    }
    .svg-viewport:active { cursor: grabbing; }
    .svg-viewport svg { display: block; transform-origin: 0 0; }
    .svg-viewport svg .node { cursor: pointer; }
    .svg-viewport svg .node:hover { filter: brightness(1.15); }
    .zoom-controls {
      position: absolute; bottom: 12px; right: 12px;
      display: flex; flex-direction: column; gap: 3px; z-index: 10;
    }
    .zoom-btn {
      width: 32px; height: 32px; border: 1px solid #444; border-radius: 5px;
      background: rgba(30,30,40,.9); color: #ccc; font-size: 16px;
      cursor: pointer; display: flex; align-items: center; justify-content: center;
    }
    .zoom-btn:hover { background: rgba(60,60,80,.95); color: #fff; border-color: #667eea; }
    .zoom-pct { text-align: center; font-size: 9px; color: #666; }
    /* ---- Detail card ---- */
    .detail-card {
      background: #1e1e1e; border-radius: 8px; padding: 14px;
      border-left: 3px solid #667eea;
    }
    .detail-card.create  { border-left-color: #4caf50; }
    .detail-card.delete  { border-left-color: #f44336; }
    .detail-card.update  { border-left-color: #ff9800; }
    .detail-card.replace { border-left-color: #9c27b0; }
    .detail-card h3 { font-size: 14px; margin-bottom: 2px; display: flex; align-items: center; gap: 6px; }
    .detail-card h3 svg { width: 20px; height: 20px; flex-shrink: 0; }
    .detail-card .dtype { font-size: 10px; color: #666; font-family: monospace; margin-bottom: 10px; }
    .section-title { font-size: 10px; font-weight: 700; color: #888; margin: 12px 0 6px; text-transform: uppercase; letter-spacing: .4px; }
    .prop { background: #151515; padding: 6px 10px; border-radius: 5px; margin-bottom: 4px; font-size: 11px; }
    .prop .key { font-weight: 600; color: #bbb; }
    .prop .old { color: #ef5350; text-decoration: line-through; font-size: 10px; }
    .prop .new { color: #66bb6a; font-size: 10px; }
    .prop .val { color: #90caf9; font-family: monospace; word-break: break-all; font-size: 10px; }
    /* ---- Legend ---- */
    .legend {
      display: flex; gap: 14px; padding: 6px 16px;
      background: #111; border-top: 1px solid #2a2a2a;
      font-size: 10px; flex-shrink: 0; color: #777;
    }
    .legend-item { display: flex; align-items: center; gap: 4px; }
    .ldot { width: 7px; height: 7px; border-radius: 50%; }
    .ldot.create  { background: #4caf50; }
    .ldot.delete  { background: #f44336; }
    .ldot.update  { background: #ff9800; }
    .ldot.replace { background: #9c27b0; }
    /* ---- Loading ---- */
    .waiting { display: flex; align-items: center; justify-content: center; height: 100%; color: #666; font-size: 13px; flex-direction: column; gap: 10px; }
    .waiting svg { width: 36px; height: 36px; opacity: .25; animation: pulse 2s infinite; }
    @keyframes pulse { 0%,100%{opacity:.15} 50%{opacity:.4} }
  </style>
</head>
<body>
  <div id="app-root" class="waiting">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M2 15s2-4 5-4c1.5 0 2.5 1 3 2 .5-3 2-6 5-6s5 3 5 6-3 6-5 6H7c-3 0-5-2-5-4z"/></svg>
    Waiting for plan data&hellip;
  </div>

  <script type="module">
    import { App } from "https://unpkg.com/@modelcontextprotocol/ext-apps@0.4.0/app-with-deps";

    const root = document.getElementById('app-root');
    const app  = new App({ name: "Cloud Diff", version: "3.0.0" });

    /* ================================================================
       Official-style Cloud Provider SVG Icons
       AWS: uses official Architecture Icon color palette
         - Compute #ED7100, Networking #8C4FFF, Database #C925D1,
         - Storage #277116, Security #DD344C, App Integration #E7157B
       Azure: #0078D4 primary, icon shapes match Azure Architecture Icons
       GCP: #4285F4 / #34A853 / #FBBC04 / #EA4335
       ================================================================ */

    const ICONS = {
      /* ===== AWS Icons (official palette) ===== */
      aws_vpc: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#232F3E"/>
        <path d="M40 15v50M15 40h50" stroke="#8C4FFF" stroke-width="1.5" opacity=".25"/>
        <rect x="16" y="16" width="48" height="48" rx="3" fill="none" stroke="#8C4FFF" stroke-width="2"/>
        <path d="M40 22v8M40 50v8M22 40h8M50 40h8" stroke="#8C4FFF" stroke-width="2"/>
        <circle cx="40" cy="40" r="6" fill="#8C4FFF"/>
        <text x="40" y="43" text-anchor="middle" fill="white" font-size="7" font-weight="bold">VPC</text>
      </svg>`,
      aws_subnet: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#232F3E"/>
        <rect x="14" y="20" width="52" height="40" rx="3" fill="none" stroke="#8C4FFF" stroke-width="2"/>
        <line x1="14" y1="40" x2="66" y2="40" stroke="#8C4FFF" stroke-width="1" stroke-dasharray="4 2"/>
        <rect x="20" y="26" width="18" height="10" rx="2" fill="#8C4FFF" opacity=".2" stroke="#8C4FFF" stroke-width="1"/>
        <rect x="42" y="26" width="18" height="10" rx="2" fill="#8C4FFF" opacity=".2" stroke="#8C4FFF" stroke-width="1"/>
        <rect x="20" y="44" width="18" height="10" rx="2" fill="#8C4FFF" opacity=".15" stroke="#8C4FFF" stroke-width="1"/>
        <rect x="42" y="44" width="18" height="10" rx="2" fill="#8C4FFF" opacity=".15" stroke="#8C4FFF" stroke-width="1"/>
      </svg>`,
      aws_instance: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#232F3E"/>
        <rect x="20" y="18" width="40" height="44" rx="3" fill="none" stroke="#ED7100" stroke-width="2"/>
        <rect x="26" y="24" width="28" height="20" rx="2" fill="#ED7100" opacity=".15"/>
        <path d="M34 34a6 6 0 1112 0" stroke="#ED7100" stroke-width="2" fill="none"/>
        <circle cx="40" cy="28" r="2" fill="#ED7100"/>
        <rect x="30" y="50" width="20" height="3" rx="1.5" fill="#ED7100" opacity=".5"/>
        <rect x="30" y="55" width="14" height="2" rx="1" fill="#ED7100" opacity=".3"/>
      </svg>`,
      aws_security_group: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#232F3E"/>
        <path d="M40 12L14 26v18c0 14 11.6 27 26 30 14.4-3 26-16 26-30V26L40 12z" fill="none" stroke="#DD344C" stroke-width="2"/>
        <path d="M40 18L20 29v14c0 10.5 8.7 20.3 20 23 11.3-2.7 20-12.5 20-23V29L40 18z" fill="#DD344C" opacity=".1"/>
        <path d="M33 40l5 5 10-10" stroke="#DD344C" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>`,
      aws_db_instance: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#232F3E"/>
        <ellipse cx="40" cy="22" rx="22" ry="9" fill="#C925D1" opacity=".15" stroke="#C925D1" stroke-width="2"/>
        <path d="M18 22v36c0 5 10 9 22 9s22-4 22-9V22" fill="none" stroke="#C925D1" stroke-width="2"/>
        <ellipse cx="40" cy="40" rx="22" ry="9" fill="none" stroke="#C925D1" stroke-width="1" opacity=".3"/>
        <ellipse cx="40" cy="58" rx="22" ry="9" fill="none" stroke="#C925D1" stroke-width="1" opacity=".3"/>
        <text x="40" y="42" text-anchor="middle" fill="#C925D1" font-size="8" font-weight="bold" opacity=".7">RDS</text>
      </svg>`,
      aws_rds_cluster: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#232F3E"/>
        <ellipse cx="40" cy="22" rx="22" ry="9" fill="#C925D1" opacity=".15" stroke="#C925D1" stroke-width="2"/>
        <path d="M18 22v36c0 5 10 9 22 9s22-4 22-9V22" fill="none" stroke="#C925D1" stroke-width="2"/>
        <circle cx="54" cy="52" r="10" fill="#232F3E" stroke="#C925D1" stroke-width="2"/>
        <path d="M50 52h8M54 48v8" stroke="#C925D1" stroke-width="1.5"/>
      </svg>`,
      aws_s3_bucket: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#232F3E"/>
        <path d="M16 24c0-4 11-7 24-7s24 3 24 7v32c0 4-11 7-24 7S16 60 16 56V24z" fill="#277116" opacity=".12" stroke="#277116" stroke-width="2"/>
        <ellipse cx="40" cy="24" rx="24" ry="7" fill="#277116" opacity=".2" stroke="#277116" stroke-width="2"/>
        <path d="M16 38c0 4 11 7 24 7s24-3 24-7" stroke="#277116" stroke-width="1" opacity=".35"/>
        <text x="40" y="52" text-anchor="middle" fill="#277116" font-size="9" font-weight="bold" opacity=".8">S3</text>
      </svg>`,
      aws_lambda_function: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#232F3E"/>
        <path d="M24 60l10-28h5l8 28h-6l-5-18-8 22h10l2 4H24z" fill="#ED7100"/>
        <text x="58" y="30" fill="#ED7100" font-size="14" font-weight="bold" opacity=".5">\\u03BB</text>
      </svg>`,
      aws_elb: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#232F3E"/>
        <circle cx="40" cy="40" r="24" fill="none" stroke="#8C4FFF" stroke-width="2"/>
        <circle cx="28" cy="28" r="5" fill="#8C4FFF" opacity=".3" stroke="#8C4FFF" stroke-width="1.5"/>
        <circle cx="52" cy="28" r="5" fill="#8C4FFF" opacity=".3" stroke="#8C4FFF" stroke-width="1.5"/>
        <circle cx="40" cy="52" r="5" fill="#8C4FFF" opacity=".3" stroke="#8C4FFF" stroke-width="1.5"/>
        <path d="M40 34v12M34 38l6-6 6 6" stroke="#8C4FFF" stroke-width="2" fill="none" stroke-linecap="round"/>
      </svg>`,
      aws_iam_role: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#232F3E"/>
        <circle cx="40" cy="30" r="11" fill="#DD344C" opacity=".15" stroke="#DD344C" stroke-width="2"/>
        <path d="M22 62c0-10 8-18 18-18s18 8 18 18" fill="#DD344C" opacity=".1" stroke="#DD344C" stroke-width="2"/>
        <circle cx="40" cy="28" r="4" fill="#DD344C" opacity=".5"/>
        <path d="M36 34h8" stroke="#DD344C" stroke-width="1.5"/>
      </svg>`,
      aws_route53_record: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#232F3E"/>
        <circle cx="40" cy="40" r="24" fill="none" stroke="#8C4FFF" stroke-width="2"/>
        <ellipse cx="40" cy="40" rx="12" ry="24" fill="none" stroke="#8C4FFF" stroke-width="1.5" opacity=".5"/>
        <line x1="16" y1="40" x2="64" y2="40" stroke="#8C4FFF" stroke-width="1" opacity=".4"/>
        <line x1="40" y1="16" x2="40" y2="64" stroke="#8C4FFF" stroke-width="1" opacity=".4"/>
        <text x="40" y="43" text-anchor="middle" fill="#8C4FFF" font-size="7" font-weight="bold">53</text>
      </svg>`,
      aws_cloudfront_distribution: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#232F3E"/>
        <circle cx="40" cy="40" r="22" fill="none" stroke="#8C4FFF" stroke-width="2"/>
        <circle cx="40" cy="40" r="14" fill="none" stroke="#8C4FFF" stroke-width="1" opacity=".4"/>
        <circle cx="40" cy="40" r="6" fill="#8C4FFF" opacity=".3"/>
        <path d="M40 18v44M18 40h44" stroke="#8C4FFF" stroke-width="1" opacity=".25"/>
      </svg>`,
      aws_dynamodb_table: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#232F3E"/>
        <ellipse cx="40" cy="22" rx="22" ry="8" fill="#C925D1" opacity=".15" stroke="#C925D1" stroke-width="2"/>
        <path d="M18 22v36c0 4.4 10 8 22 8s22-3.6 22-8V22" fill="none" stroke="#C925D1" stroke-width="2"/>
        <path d="M26 36h28M26 44h20M26 52h24" stroke="#C925D1" stroke-width="1.5" opacity=".4"/>
      </svg>`,
      aws_sqs_queue: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#232F3E"/>
        <rect x="14" y="24" width="52" height="32" rx="4" fill="none" stroke="#E7157B" stroke-width="2"/>
        <path d="M24 36h20M24 44h14" stroke="#E7157B" stroke-width="2" opacity=".5"/>
        <circle cx="54" cy="40" r="4" fill="#E7157B" opacity=".4"/>
        <path d="M18 32l4-4M18 48l4 4" stroke="#E7157B" stroke-width="1.5" opacity=".3"/>
      </svg>`,
      aws_sns_topic: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#232F3E"/>
        <rect x="14" y="24" width="52" height="32" rx="4" fill="none" stroke="#E7157B" stroke-width="2"/>
        <path d="M28 40l8-8v16z" fill="#E7157B" opacity=".6"/>
        <path d="M40 32c8 0 14 3.6 14 8s-6 8-14 8" stroke="#E7157B" stroke-width="2" fill="none" opacity=".5"/>
        <path d="M42 36c4 0 8 1.8 8 4s-4 4-8 4" stroke="#E7157B" stroke-width="1.5" fill="none" opacity=".4"/>
      </svg>`,
      aws_ecs_cluster: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#232F3E"/>
        <rect x="16" y="16" width="48" height="48" rx="4" fill="none" stroke="#ED7100" stroke-width="2"/>
        <rect x="22" y="22" width="14" height="14" rx="2" fill="#ED7100" opacity=".25" stroke="#ED7100" stroke-width="1"/>
        <rect x="44" y="22" width="14" height="14" rx="2" fill="#ED7100" opacity=".25" stroke="#ED7100" stroke-width="1"/>
        <rect x="22" y="44" width="14" height="14" rx="2" fill="#ED7100" opacity=".25" stroke="#ED7100" stroke-width="1"/>
        <rect x="44" y="44" width="14" height="14" rx="2" fill="#ED7100" opacity=".15" stroke="#ED7100" stroke-width="1" stroke-dasharray="3 2"/>
      </svg>`,
      aws_internet_gateway: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#232F3E"/>
        <circle cx="40" cy="40" r="22" fill="none" stroke="#8C4FFF" stroke-width="2"/>
        <path d="M40 20v40" stroke="#8C4FFF" stroke-width="2"/>
        <path d="M30 30l10-10 10 10" stroke="#8C4FFF" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M30 50l10 10 10-10" stroke="#8C4FFF" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>`,
      aws_nat_gateway: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#232F3E"/>
        <rect x="16" y="16" width="48" height="48" rx="4" fill="none" stroke="#8C4FFF" stroke-width="2"/>
        <text x="40" y="46" text-anchor="middle" fill="#8C4FFF" font-size="14" font-weight="bold">NAT</text>
      </svg>`,
      aws_ebs_volume: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#232F3E"/>
        <rect x="22" y="14" width="36" height="52" rx="4" fill="none" stroke="#277116" stroke-width="2"/>
        <rect x="28" y="22" width="24" height="6" rx="2" fill="#277116" opacity=".25"/>
        <rect x="28" y="32" width="24" height="6" rx="2" fill="#277116" opacity=".2"/>
        <rect x="28" y="42" width="24" height="6" rx="2" fill="#277116" opacity=".15"/>
      </svg>`,
      aws_secretsmanager_secret: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#232F3E"/>
        <rect x="22" y="34" width="36" height="28" rx="4" fill="none" stroke="#DD344C" stroke-width="2"/>
        <path d="M30 34V26a10 10 0 0120 0v8" fill="none" stroke="#DD344C" stroke-width="2"/>
        <circle cx="40" cy="48" r="4" fill="#DD344C"/>
        <line x1="40" y1="52" x2="40" y2="56" stroke="#DD344C" stroke-width="2"/>
      </svg>`,

      /* ===== Azure Icons (official #0078D4 + category colors) ===== */
      azurerm_resource_group: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#1B1B1F"/>
        <rect x="14" y="18" width="52" height="44" rx="4" fill="none" stroke="#0078D4" stroke-width="2"/>
        <rect x="14" y="18" width="52" height="12" rx="4" fill="#0078D4" opacity=".15"/>
        <rect x="20" y="22" width="16" height="4" rx="2" fill="#0078D4" opacity=".5"/>
        <rect x="22" y="38" width="12" height="12" rx="2" fill="#0078D4" opacity=".15" stroke="#0078D4" stroke-width="1"/>
        <rect x="40" y="38" width="12" height="12" rx="2" fill="#0078D4" opacity=".15" stroke="#0078D4" stroke-width="1"/>
        <rect x="31" y="52" width="12" height="6" rx="2" fill="#0078D4" opacity=".1" stroke="#0078D4" stroke-width="1"/>
      </svg>`,
      azurerm_virtual_network: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#1B1B1F"/>
        <rect x="14" y="14" width="52" height="52" rx="4" fill="none" stroke="#0078D4" stroke-width="2"/>
        <circle cx="28" cy="28" r="5" fill="#0078D4" opacity=".3" stroke="#0078D4" stroke-width="1.5"/>
        <circle cx="52" cy="28" r="5" fill="#0078D4" opacity=".3" stroke="#0078D4" stroke-width="1.5"/>
        <circle cx="28" cy="52" r="5" fill="#0078D4" opacity=".3" stroke="#0078D4" stroke-width="1.5"/>
        <circle cx="52" cy="52" r="5" fill="#0078D4" opacity=".3" stroke="#0078D4" stroke-width="1.5"/>
        <line x1="33" y1="28" x2="47" y2="28" stroke="#0078D4" stroke-width="1.5"/>
        <line x1="28" y1="33" x2="28" y2="47" stroke="#0078D4" stroke-width="1.5"/>
        <line x1="52" y1="33" x2="52" y2="47" stroke="#0078D4" stroke-width="1.5"/>
        <line x1="33" y1="52" x2="47" y2="52" stroke="#0078D4" stroke-width="1.5"/>
        <line x1="33" y1="33" x2="47" y2="47" stroke="#0078D4" stroke-width="1" opacity=".4"/>
      </svg>`,
      azurerm_subnet: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#1B1B1F"/>
        <rect x="14" y="20" width="52" height="40" rx="3" fill="none" stroke="#0078D4" stroke-width="2"/>
        <line x1="40" y1="20" x2="40" y2="60" stroke="#0078D4" stroke-width="1" stroke-dasharray="4 2" opacity=".4"/>
        <rect x="18" y="28" width="18" height="10" rx="2" fill="#0078D4" opacity=".12" stroke="#0078D4" stroke-width="1"/>
        <rect x="44" y="28" width="18" height="10" rx="2" fill="#0078D4" opacity=".12" stroke="#0078D4" stroke-width="1"/>
        <rect x="18" y="44" width="18" height="10" rx="2" fill="#0078D4" opacity=".08" stroke="#0078D4" stroke-width="1"/>
      </svg>`,
      azurerm_virtual_machine: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#1B1B1F"/>
        <rect x="18" y="14" width="44" height="34" rx="3" fill="none" stroke="#0078D4" stroke-width="2"/>
        <rect x="22" y="18" width="36" height="26" rx="1" fill="#0078D4" opacity=".1"/>
        <path d="M32 34l8-10 8 10z" fill="#0078D4" opacity=".4"/>
        <rect x="28" y="52" width="24" height="4" rx="2" fill="#0078D4" opacity=".4"/>
        <line x1="40" y1="48" x2="40" y2="52" stroke="#0078D4" stroke-width="2"/>
        <rect x="24" y="58" width="32" height="3" rx="1.5" fill="#0078D4" opacity=".2"/>
      </svg>`,
      azurerm_linux_virtual_machine: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#1B1B1F"/>
        <rect x="18" y="14" width="44" height="34" rx="3" fill="none" stroke="#0078D4" stroke-width="2"/>
        <rect x="22" y="18" width="36" height="26" rx="1" fill="#0078D4" opacity=".1"/>
        <text x="40" y="35" text-anchor="middle" fill="#0078D4" font-size="10" font-weight="bold">\\u{1F427}</text>
        <rect x="28" y="52" width="24" height="4" rx="2" fill="#0078D4" opacity=".4"/>
        <line x1="40" y1="48" x2="40" y2="52" stroke="#0078D4" stroke-width="2"/>
      </svg>`,
      azurerm_storage_account: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#1B1B1F"/>
        <rect x="16" y="22" width="48" height="36" rx="3" fill="none" stroke="#0078D4" stroke-width="2"/>
        <rect x="16" y="22" width="48" height="10" rx="3" fill="#0078D4" opacity=".15"/>
        <rect x="16" y="36" width="48" height="10" fill="#0078D4" opacity=".08"/>
        <circle cx="56" cy="27" r="2" fill="#4caf50"/>
        <circle cx="56" cy="41" r="2" fill="#4caf50"/>
        <circle cx="56" cy="53" r="2" fill="#ff9800" opacity=".5"/>
      </svg>`,
      azurerm_storage_blob: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#1B1B1F"/>
        <path d="M16 28c0-4 11-7 24-7s24 3 24 7v24c0 4-11 7-24 7S16 56 16 52V28z" fill="#0078D4" opacity=".1" stroke="#0078D4" stroke-width="2"/>
        <ellipse cx="40" cy="28" rx="24" ry="7" fill="#0078D4" opacity=".2"/>
      </svg>`,
      azurerm_app_service: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#1B1B1F"/>
        <circle cx="40" cy="40" r="22" fill="none" stroke="#0078D4" stroke-width="2"/>
        <circle cx="40" cy="40" r="22" fill="#0078D4" opacity=".08"/>
        <path d="M30 28l20 12-20 12z" fill="#0078D4" opacity=".6"/>
      </svg>`,
      azurerm_function_app: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#1B1B1F"/>
        <path d="M40 14L18 28v24l22 14 22-14V28L40 14z" fill="#0078D4" opacity=".1" stroke="#0078D4" stroke-width="2"/>
        <path d="M32 52l6-16h4l-3 10h6l-10 12 3-8h-6z" fill="#0078D4"/>
      </svg>`,
      azurerm_mssql_server: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#1B1B1F"/>
        <ellipse cx="40" cy="22" rx="22" ry="8" fill="#0078D4" opacity=".15" stroke="#0078D4" stroke-width="2"/>
        <path d="M18 22v36c0 4.4 10 8 22 8s22-3.6 22-8V22" fill="none" stroke="#0078D4" stroke-width="2"/>
        <text x="40" y="50" text-anchor="middle" fill="#0078D4" font-size="9" font-weight="bold" opacity=".6">SQL</text>
      </svg>`,
      azurerm_mssql_database: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#1B1B1F"/>
        <ellipse cx="40" cy="22" rx="22" ry="8" fill="#0078D4" opacity=".15" stroke="#0078D4" stroke-width="2"/>
        <path d="M18 22v36c0 4.4 10 8 22 8s22-3.6 22-8V22" fill="none" stroke="#0078D4" stroke-width="2"/>
        <text x="40" y="50" text-anchor="middle" fill="#0078D4" font-size="9" font-weight="bold" opacity=".6">SQL</text>
      </svg>`,
      azurerm_cosmosdb_account: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#1B1B1F"/>
        <circle cx="40" cy="40" r="22" fill="none" stroke="#0078D4" stroke-width="2"/>
        <ellipse cx="40" cy="40" rx="22" ry="10" fill="none" stroke="#0078D4" stroke-width="1.5" transform="rotate(30 40 40)" opacity=".5"/>
        <ellipse cx="40" cy="40" rx="22" ry="10" fill="none" stroke="#0078D4" stroke-width="1.5" transform="rotate(-30 40 40)" opacity=".5"/>
        <circle cx="40" cy="40" r="5" fill="#0078D4" opacity=".4"/>
      </svg>`,
      azurerm_network_security_group: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#1B1B1F"/>
        <path d="M40 12L14 26v18c0 14 11.6 27 26 30 14.4-3 26-16 26-30V26L40 12z" fill="#0078D4" opacity=".08" stroke="#0078D4" stroke-width="2"/>
        <path d="M33 40l5 5 10-10" stroke="#0078D4" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>`,
      azurerm_lb: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#1B1B1F"/>
        <circle cx="40" cy="40" r="22" fill="none" stroke="#0078D4" stroke-width="2"/>
        <path d="M40 24v10" stroke="#0078D4" stroke-width="2"/>
        <path d="M30 46l10-8 10 8" stroke="#0078D4" stroke-width="2" fill="none"/>
        <circle cx="30" cy="52" r="4" fill="#0078D4" opacity=".3" stroke="#0078D4" stroke-width="1"/>
        <circle cx="50" cy="52" r="4" fill="#0078D4" opacity=".3" stroke="#0078D4" stroke-width="1"/>
      </svg>`,
      azurerm_application_gateway: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#1B1B1F"/>
        <rect x="14" y="14" width="52" height="52" rx="4" fill="none" stroke="#0078D4" stroke-width="2"/>
        <path d="M14 40h18l8-10 8 10h18" stroke="#0078D4" stroke-width="2" fill="none"/>
        <circle cx="40" cy="40" r="4" fill="#0078D4"/>
      </svg>`,

      /* ===== GCP Icons ===== */
      google_compute_instance: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#1A2332"/>
        <rect x="22" y="18" width="36" height="44" rx="3" fill="none" stroke="#4285F4" stroke-width="2"/>
        <rect x="28" y="24" width="24" height="16" rx="2" fill="#4285F4" opacity=".15"/>
        <circle cx="40" cy="32" r="4" fill="#4285F4" opacity=".5"/>
        <rect x="30" y="46" width="20" height="3" rx="1.5" fill="#4285F4" opacity=".4"/>
        <rect x="30" y="52" width="14" height="3" rx="1.5" fill="#4285F4" opacity=".25"/>
        <line x1="16" y1="30" x2="22" y2="30" stroke="#34A853" stroke-width="2"/>
        <line x1="16" y1="40" x2="22" y2="40" stroke="#EA4335" stroke-width="2"/>
        <line x1="16" y1="50" x2="22" y2="50" stroke="#FBBC04" stroke-width="2"/>
        <line x1="58" y1="30" x2="64" y2="30" stroke="#34A853" stroke-width="2"/>
        <line x1="58" y1="40" x2="64" y2="40" stroke="#EA4335" stroke-width="2"/>
        <line x1="58" y1="50" x2="64" y2="50" stroke="#FBBC04" stroke-width="2"/>
      </svg>`,
      google_compute_network: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#1A2332"/>
        <rect x="14" y="14" width="52" height="52" rx="4" fill="none" stroke="#4285F4" stroke-width="2"/>
        <circle cx="28" cy="28" r="4" fill="#4285F4" opacity=".4" stroke="#4285F4" stroke-width="1"/>
        <circle cx="52" cy="28" r="4" fill="#34A853" opacity=".4" stroke="#34A853" stroke-width="1"/>
        <circle cx="28" cy="52" r="4" fill="#FBBC04" opacity=".4" stroke="#FBBC04" stroke-width="1"/>
        <circle cx="52" cy="52" r="4" fill="#EA4335" opacity=".4" stroke="#EA4335" stroke-width="1"/>
        <line x1="32" y1="28" x2="48" y2="28" stroke="#4285F4" stroke-width="1.5" opacity=".5"/>
        <line x1="28" y1="32" x2="28" y2="48" stroke="#4285F4" stroke-width="1.5" opacity=".5"/>
        <line x1="32" y1="52" x2="48" y2="52" stroke="#4285F4" stroke-width="1.5" opacity=".5"/>
        <line x1="52" y1="32" x2="52" y2="48" stroke="#4285F4" stroke-width="1.5" opacity=".5"/>
      </svg>`,
      google_compute_subnetwork: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#1A2332"/>
        <rect x="14" y="20" width="52" height="40" rx="3" fill="none" stroke="#4285F4" stroke-width="2"/>
        <line x1="40" y1="20" x2="40" y2="60" stroke="#4285F4" stroke-width="1" stroke-dasharray="4 2" opacity=".4"/>
        <rect x="18" y="28" width="18" height="10" rx="2" fill="#4285F4" opacity=".12" stroke="#4285F4" stroke-width="1"/>
        <rect x="44" y="28" width="18" height="10" rx="2" fill="#34A853" opacity=".12" stroke="#34A853" stroke-width="1"/>
      </svg>`,
      google_storage_bucket: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#1A2332"/>
        <path d="M16 26c0-4 11-7 24-7s24 3 24 7v28c0 4-11 7-24 7S16 58 16 54V26z" fill="#4285F4" opacity=".08" stroke="#4285F4" stroke-width="2"/>
        <ellipse cx="40" cy="26" rx="24" ry="7" fill="#4285F4" opacity=".15" stroke="#4285F4" stroke-width="1.5"/>
        <path d="M16 38c0 4 11 7 24 7s24-3 24-7" stroke="#4285F4" stroke-width="1" opacity=".3"/>
        <path d="M16 50c0 4 11 7 24 7s24-3 24-7" stroke="#4285F4" stroke-width="1" opacity=".2"/>
      </svg>`,
      google_sql_database_instance: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#1A2332"/>
        <ellipse cx="40" cy="22" rx="22" ry="8" fill="#4285F4" opacity=".12" stroke="#4285F4" stroke-width="2"/>
        <path d="M18 22v36c0 4.4 10 8 22 8s22-3.6 22-8V22" fill="none" stroke="#4285F4" stroke-width="2"/>
        <ellipse cx="40" cy="40" rx="22" ry="8" fill="none" stroke="#4285F4" stroke-width="1" opacity=".25"/>
        <text x="40" y="50" text-anchor="middle" fill="#4285F4" font-size="8" font-weight="bold" opacity=".5">SQL</text>
      </svg>`,
      google_firestore_database: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#1A2332"/>
        <path d="M28 16l12 24-12 24" stroke="#FBBC04" stroke-width="2.5" fill="none"/>
        <path d="M40 24l12 16-12 24" stroke="#EA4335" stroke-width="2.5" fill="none"/>
      </svg>`,
      google_compute_forwarding_rule: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#1A2332"/>
        <circle cx="40" cy="40" r="22" fill="none" stroke="#4285F4" stroke-width="2"/>
        <path d="M28 40h24M44 34l8 6-8 6" stroke="#4285F4" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>`,
      google_container_cluster: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#1A2332"/>
        <circle cx="40" cy="40" r="22" fill="none" stroke="#4285F4" stroke-width="2"/>
        <circle cx="40" cy="26" r="5" fill="#4285F4" opacity=".3" stroke="#4285F4" stroke-width="1.5"/>
        <circle cx="28" cy="50" r="5" fill="#34A853" opacity=".3" stroke="#34A853" stroke-width="1.5"/>
        <circle cx="52" cy="50" r="5" fill="#EA4335" opacity=".3" stroke="#EA4335" stroke-width="1.5"/>
        <line x1="40" y1="31" x2="31" y2="46" stroke="#4285F4" stroke-width="1.5" opacity=".4"/>
        <line x1="40" y1="31" x2="49" y2="46" stroke="#4285F4" stroke-width="1.5" opacity=".4"/>
        <line x1="33" y1="50" x2="47" y2="50" stroke="#4285F4" stroke-width="1.5" opacity=".4"/>
      </svg>`,

      /* ---- Fallback ---- */
      _default: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="76" height="76" rx="5" fill="#222230"/>
        <rect x="18" y="18" width="44" height="44" rx="6" fill="none" stroke="#666" stroke-width="2"/>
        <circle cx="40" cy="34" r="7" fill="#666" opacity=".2" stroke="#666" stroke-width="1.5"/>
        <rect x="28" y="48" width="24" height="6" rx="3" fill="#666" opacity=".2"/>
      </svg>`,
    };

    /* Provider logo for cluster headers */
    const PROV_LOGO = {
      aws: `<svg viewBox="0 0 40 28" xmlns="http://www.w3.org/2000/svg"><rect width="40" height="28" rx="4" fill="#232F3E"/><path d="M12.5 18.5c3.5 1 7.5 1.5 11 .5" stroke="#FF9900" stroke-width="1.5" fill="none" stroke-linecap="round"/><path d="M27 16c1.5-1 2-2 2.5-1" stroke="#FF9900" stroke-width="1.5" fill="none" stroke-linecap="round"/><path d="M8 16l2-6h1l2 6M9.5 14h3" stroke="#FF9900" stroke-width="1" fill="none"/><path d="M15 10l1.5 4.5L18 10" stroke="#FF9900" stroke-width="1" fill="none"/><path d="M20 16l2-6h1l2 6M21.5 14h3" stroke="#FF9900" stroke-width="1" fill="none"/></svg>`,
      azurerm: `<svg viewBox="0 0 40 28" xmlns="http://www.w3.org/2000/svg"><rect width="40" height="28" rx="4" fill="#1B1B1F"/><path d="M12 22l7-18h3l-4 12h8L14 22z" fill="#0078D4"/><path d="M26 8h6v3h-6z" fill="#50e6ff" opacity=".5" rx="1"/><path d="M26 13h4v3h-4z" fill="#0078D4" opacity=".5" rx="1"/></svg>`,
      google: `<svg viewBox="0 0 40 28" xmlns="http://www.w3.org/2000/svg"><rect width="40" height="28" rx="4" fill="#1A2332"/><circle cx="14" cy="14" r="6" fill="none" stroke="#4285F4" stroke-width="2"/><path d="M18.2 18.2l3.5 3.5" stroke="#EA4335" stroke-width="2" stroke-linecap="round"/><text x="28" y="18" fill="#4285F4" font-size="8" font-weight="bold">G</text></svg>`,
    };

    /* Category grouping */
    const CATS = {
      networking: { label: 'Networking', types: ['vpc','subnet','virtual_network','network_security_group','security_group','internet_gateway','nat_gateway','route53','cloudfront','elb','lb','alb','compute_network','compute_subnetwork','load_balancer','application_gateway','dns_zone','forwarding_rule'] },
      compute: { label: 'Compute', types: ['instance','virtual_machine','linux_virtual_machine','windows_virtual_machine','lambda_function','ecs_cluster','ecs_service','app_service','function_app','compute_instance','container_group','container_cluster','gke','app_engine'] },
      database: { label: 'Database', types: ['db_instance','rds_cluster','dynamodb_table','elasticache','sql_database','cosmosdb','mssql','sql_database_instance','firestore'] },
      storage: { label: 'Storage', types: ['s3_bucket','ebs_volume','efs','storage_account','storage_blob','storage_container','storage_bucket','gcs'] },
      security: { label: 'Security & Identity', types: ['iam_role','iam_user','iam_policy','secretsmanager','waf','managed_identity','user_assigned_identity'] },
      messaging: { label: 'Messaging', types: ['sqs_queue','sns_topic','kinesis'] },
    };

    function categorize(t) {
      const l = t.toLowerCase();
      for (const [c, i] of Object.entries(CATS)) { if (i.types.some(x => l.includes(x))) return c; }
      return 'other';
    }
    function iconFor(t) { return ICONS[t] || ICONS._default; }
    function classify(a) {
      if (a.includes('create') && a.includes('delete')) return 'replace';
      if (a.includes('delete')) return 'delete';
      if (a.includes('create')) return 'create';
      if (a.includes('update')) return 'update';
      return 'no-op';
    }
    function provOf(t) {
      if (t.startsWith('aws_')) return 'aws';
      if (t.startsWith('azurerm_')) return 'azurerm';
      if (t.startsWith('google_')) return 'google';
      return 'other';
    }
    function esc(s) { const d = document.createElement('div'); d.textContent = String(s); return d.innerHTML; }
    function cardId(addr) { return 'c_' + addr.replace(/[^a-zA-Z0-9]/g, '_'); }

    /* ========== RENDER ========== */
    function render(planData) {
      const changes = planData.resource_changes || [];
      const depMap = (planData.configuration?.root_module?.resources || [])
        .reduce((m, r) => { m[r.address] = r.depends_on || []; return m; }, {});
      const counts = { create: 0, delete: 0, update: 0, replace: 0 };
      const items = changes.map(r => {
        const action = classify(r.change.actions);
        if (counts[action] !== undefined) counts[action]++;
        return { address: r.address, type: r.type, name: r.name,
                 action, before: r.change.before, after: r.change.after,
                 deps: depMap[r.address] || [] };
      });

      const serverSvg = planData._server_svg || null;

      const sp = [];
      if (counts.create)  sp.push(`<span><span class="ldot create"></span>${counts.create} create</span>`);
      if (counts.update)  sp.push(`<span><span class="ldot update"></span>${counts.update} update</span>`);
      if (counts.delete)  sp.push(`<span><span class="ldot delete"></span>${counts.delete} destroy</span>`);
      if (counts.replace) sp.push(`<span><span class="ldot replace"></span>${counts.replace} replace</span>`);

      /* ---- Server SVG mode (official cloud icons via Graphviz) ---- */
      if (serverSvg) {
        root.className = '';
        root.innerHTML = `
          <div class="header">
            <div class="header-logo">
              <svg viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="1.5"><path d="M2 15s2-4 5-4c1.5 0 2.5 1 3 2 .5-3 2-6 5-6s5 3 5 6-3 6-5 6H7c-3 0-5-2-5-4z"/></svg>
              <div><h1>Cloud Architecture Diff</h1>
              <p>Terraform &mdash; ${items.length} resources &mdash; v${planData.terraform_version||'?'}</p></div>
            </div>
            <div class="summary-inline">${sp.join('')}</div>
          </div>
          <div class="content">
            <div class="canvas-wrap" id="canvas" style="position:relative">
              <div class="svg-viewport" id="svgViewport">${serverSvg}</div>
              <div class="zoom-controls">
                <button class="zoom-btn" id="zoomInBtn">+</button>
                <div class="zoom-pct" id="zoomPct">100%</div>
                <button class="zoom-btn" id="zoomOutBtn">&minus;</button>
                <button class="zoom-btn" id="zoomFitBtn" style="font-size:12px">&#x229e;</button>
              </div>
            </div>
            <div class="sidebar">
              <div class="placeholder" id="detail">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <rect x="3" y="3" width="18" height="18" rx="3"/><path d="M9 9h6M9 13h4"/>
                </svg>
                <p>Click a resource to view<br>configuration &amp; changes</p>
              </div>
            </div>
          </div>
          <div class="legend">
            <div class="legend-item"><div class="ldot create"></div>Create</div>
            <div class="legend-item"><div class="ldot update"></div>Update</div>
            <div class="legend-item"><div class="ldot delete"></div>Destroy</div>
            <div class="legend-item"><div class="ldot replace"></div>Replace</div>
            <div class="legend-item" style="margin-left:auto;opacity:.5">Scroll to zoom &bull; Drag to pan</div>
          </div>`;

        /* Set up SVG zoom & pan */
        const vp = document.getElementById('svgViewport');
        const svgNode = vp ? vp.querySelector('svg') : null;
        if (svgNode) {
          /* Fix SVG sizing: use viewBox, remove fixed dimensions */
          let vb = svgNode.getAttribute('viewBox');
          if (!vb) {
            const w = parseFloat(svgNode.getAttribute('width')) || 800;
            const h = parseFloat(svgNode.getAttribute('height')) || 600;
            svgNode.setAttribute('viewBox', '0 0 ' + w + ' ' + h);
          }
          svgNode.removeAttribute('width');
          svgNode.removeAttribute('height');
          svgNode.style.width = '100%';
          svgNode.style.height = '100%';

          let sc = 1, px = 0, py = 0, panning = false, sx = 0, sy = 0;
          function applyTx() {
            svgNode.style.transform = 'translate('+px+'px,'+py+'px) scale('+sc+')';
            const pctEl = document.getElementById('zoomPct');
            if (pctEl) pctEl.textContent = Math.round(sc*100)+'%';
          }
          function fitSvg() {
            const vb2 = svgNode.getAttribute('viewBox');
            if (!vb2) return;
            const p = vb2.split(/[\s,]+/).map(Number);
            const cr = vp.getBoundingClientRect();
            sc = Math.min(cr.width/p[2], cr.height/p[3]) * 0.92;
            px = (cr.width - p[2]*sc)/2;
            py = (cr.height - p[3]*sc)/2;
            applyTx();
          }
          document.getElementById('zoomInBtn').onclick = () => { sc = Math.min(sc*1.25,5); applyTx(); };
          document.getElementById('zoomOutBtn').onclick = () => { sc = Math.max(sc/1.25,0.2); applyTx(); };
          document.getElementById('zoomFitBtn').onclick = fitSvg;
          vp.addEventListener('wheel', e => {
            e.preventDefault();
            const r = vp.getBoundingClientRect();
            const mx = e.clientX-r.left, my = e.clientY-r.top;
            const old = sc;
            sc = e.deltaY<0 ? Math.min(sc*1.1,5) : Math.max(sc/1.1,0.2);
            px = mx-(mx-px)*(sc/old); py = my-(my-py)*(sc/old);
            applyTx();
          }, {passive:false});
          vp.addEventListener('mousedown', e => {
            if (e.target.closest('.node')) return;
            panning=true; sx=e.clientX-px; sy=e.clientY-py;
          });
          window.addEventListener('mousemove', e => { if(!panning)return; px=e.clientX-sx; py=e.clientY-sy; applyTx(); });
          window.addEventListener('mouseup', () => { panning=false; });
          setTimeout(fitSvg, 50);
          window.addEventListener('resize', () => setTimeout(fitSvg, 100));

          /* Make SVG .node groups clickable for detail panel */
          const lookup = Object.fromEntries(items.map(i => [i.address, i]));
          svgNode.querySelectorAll('.node').forEach(g => {
            let matched = null;
            g.querySelectorAll('text').forEach(t => {
              const raw = t.textContent.trim().replace(/[\u2728\ud83d\uddd1\ufe0f\ud83d\udcdd\ud83d\udd04]/g, '').trim();
              if (!matched) {
                for (const it of items) {
                  if (it.name === raw || it.address.includes(raw)) { matched = it; break; }
                }
              }
            });
            if (matched) {
              g.style.cursor = 'pointer';
              g.addEventListener('click', e => {
                e.stopPropagation();
                svgNode.querySelectorAll('.node').forEach(n => { n.style.filter=''; });
                g.style.filter = 'brightness(1.3) drop-shadow(0 0 8px rgba(102,126,234,.6))';
                showDetail(matched);
              });
            }
          });
        }
        return;
      }

      /* ---- Fallback: client-side card rendering ---- */
      const groups = {};
      items.forEach(it => {
        const p = provOf(it.type), c = categorize(it.type);
        if (!groups[p]) groups[p] = {};
        if (!groups[p][c]) groups[p][c] = [];
        groups[p][c].push(it);
      });

      let clustersHTML = '';
      for (const [prov, cats] of Object.entries(groups)) {
        for (const [cat, list] of Object.entries(cats)) {
          const lbl = CATS[cat]?.label || 'Resources';
          const logo = PROV_LOGO[prov] || '';
          clustersHTML += `<div class="cluster">
            <div class="cluster-header">
              <span class="cl-icon">${logo}</span>
              <span class="cl-title">${lbl}</span>
            </div>
            <div class="cluster-resources">
              ${list.map(it => `<div class="res-card" data-addr="${it.address}" id="${cardId(it.address)}">
                <div class="action-dot ${it.action}"></div>
                <div class="res-icon">${iconFor(it.type)}</div>
                <div class="res-name">${esc(it.name)}</div>
                <div class="res-type">${esc(it.type)}</div>
                <div class="action-tag ${it.action}">${it.action}</div>
              </div>`).join('')}
            </div>
          </div>`;
        }
      }

      root.className = '';
      root.innerHTML = `
        <div class="header">
          <div class="header-logo">
            <svg viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="1.5"><path d="M2 15s2-4 5-4c1.5 0 2.5 1 3 2 .5-3 2-6 5-6s5 3 5 6-3 6-5 6H7c-3 0-5-2-5-4z"/></svg>
            <div><h1>Cloud Architecture Diff</h1>
            <p>Terraform &mdash; ${items.length} resources &mdash; v${planData.terraform_version||'?'}</p></div>
          </div>
          <div class="summary-inline">${sp.join('')}</div>
        </div>
        <div class="content">
          <div class="canvas-wrap" id="canvas">
            <div class="arch-diagram" id="arch">
              ${clustersHTML}
            </div>
            <svg class="conn-svg" id="connSvg">
              <defs>
                <marker id="arr" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
                  <polygon points="0 0, 8 3, 0 6" fill="rgba(130,160,255,.55)"/>
                </marker>
              </defs>
            </svg>
          </div>
          <div class="sidebar">
            <div class="placeholder" id="detail">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <rect x="3" y="3" width="18" height="18" rx="3"/><path d="M9 9h6M9 13h4"/>
              </svg>
              <p>Click a resource to view<br>configuration &amp; changes</p>
            </div>
          </div>
        </div>
        <div class="legend">
          <div class="legend-item"><div class="ldot create"></div>Create</div>
          <div class="legend-item"><div class="ldot update"></div>Update</div>
          <div class="legend-item"><div class="ldot delete"></div>Destroy</div>
          <div class="legend-item"><div class="ldot replace"></div>Replace</div>
          <div class="legend-item" style="margin-left:auto;opacity:.5">&#8675; dashed = dependency</div>
        </div>`;

      /* Draw connections after layout settles */
      setTimeout(() => drawConnections(items), 80);
      const canvasEl = document.getElementById('canvas');
      canvasEl.addEventListener('scroll', () => drawConnections(items));
      window.addEventListener('resize', () => drawConnections(items));

      /* Click handling */
      const lookup = Object.fromEntries(items.map(i => [i.address, i]));
      root.querySelectorAll('.res-card').forEach(el => {
        el.addEventListener('click', () => {
          root.querySelectorAll('.res-card.selected').forEach(n => n.classList.remove('selected'));
          el.classList.add('selected');
          showDetail(lookup[el.dataset.addr]);
        });
      });
    }

    /* ========== CURVED DEPENDENCY CONNECTIONS ========== */
    function drawConnections(items) {
      const svg = document.getElementById('connSvg');
      const canvas = document.getElementById('canvas');
      const arch = document.getElementById('arch');
      if (!svg || !canvas || !arch) return;

      /* Size SVG to cover full scrollable area */
      const archRect = arch.getBoundingClientRect();
      const canvasRect = canvas.getBoundingClientRect();
      const w = Math.max(arch.scrollWidth, canvas.scrollWidth);
      const h = Math.max(arch.scrollHeight, canvas.scrollHeight);
      svg.setAttribute('width', w);
      svg.setAttribute('height', h);
      svg.style.width = w + 'px';
      svg.style.height = h + 'px';

      /* Clear old paths (keep defs) */
      svg.querySelectorAll('path').forEach(p => p.remove());

      const scrollL = canvas.scrollLeft;
      const scrollT = canvas.scrollTop;

      items.forEach(item => {
        (item.deps || []).forEach(dep => {
          const fromEl = document.getElementById(cardId(dep));
          const toEl   = document.getElementById(cardId(item.address));
          if (!fromEl || !toEl) return;

          const fr = fromEl.getBoundingClientRect();
          const tr = toEl.getBoundingClientRect();

          /* Convert to canvas-relative coords (accounting for scroll) */
          const x1 = fr.left - canvasRect.left + scrollL + fr.width / 2;
          const y1 = fr.top  - canvasRect.top  + scrollT + fr.height;
          const x2 = tr.left - canvasRect.left + scrollL + tr.width / 2;
          const y2 = tr.top  - canvasRect.top  + scrollT;

          /* Choose best connection points */
          let sx, sy, ex, ey;
          const dx = Math.abs(x2 - x1);
          const dy = Math.abs(y2 - y1);

          if (dy > fr.height * 0.6) {
            /* Vertical: bottom of source -> top of target */
            sx = x1; sy = y1;
            ex = x2; ey = y2;
          } else {
            /* Horizontal: right/left side */
            if (x2 > x1) {
              sx = fr.left - canvasRect.left + scrollL + fr.width;
              sy = fr.top  - canvasRect.top  + scrollT + fr.height / 2;
              ex = tr.left - canvasRect.left + scrollL;
              ey = tr.top  - canvasRect.top  + scrollT + tr.height / 2;
            } else {
              sx = fr.left - canvasRect.left + scrollL;
              sy = fr.top  - canvasRect.top  + scrollT + fr.height / 2;
              ex = tr.left - canvasRect.left + scrollL + tr.width;
              ey = tr.top  - canvasRect.top  + scrollT + tr.height / 2;
            }
          }

          /* Cubic bezier curve */
          const midY = (sy + ey) / 2;
          const cpOffset = Math.min(Math.abs(ey - sy) * 0.5, 60);
          const cp1y = sy + cpOffset;
          const cp2y = ey - cpOffset;

          const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
          path.setAttribute('d', `M${sx},${sy} C${sx},${cp1y} ${ex},${cp2y} ${ex},${ey}`);
          path.setAttribute('stroke', 'rgba(130,160,255,.4)');
          svg.appendChild(path);
        });
      });
    }

    /* ========== DETAIL PANEL ========== */
    function showDetail(item) {
      const panel = document.getElementById('detail');
      const lbl = {create:'Creating',delete:'Destroying',update:'Updating',replace:'Replacing'}[item.action]||item.action;
      let body = '';

      if (item.action === 'create' && item.after) {
        body += '<div class="section-title">New Configuration</div>' + propsHTML(item.after);
      } else if (item.action === 'delete' && item.before) {
        body += '<div class="section-title">Removed Configuration</div>' + propsHTML(item.before);
      } else if ((item.action === 'update' || item.action === 'replace') && item.before && item.after) {
        body += '<div class="section-title">Changes</div>';
        const keys = new Set([...Object.keys(item.before||{}), ...Object.keys(item.after||{})]);
        for (const k of keys) {
          const bv = JSON.stringify((item.before||{})[k]??null,null,2);
          const av = JSON.stringify((item.after||{})[k]??null,null,2);
          if (bv !== av) body += `<div class="prop"><div class="key">${esc(k)}</div><div class="old">\\u2212 ${esc(bv)}</div><div class="new">+ ${esc(av)}</div></div>`;
        }
      }
      if (item.deps?.length) {
        body += '<div class="section-title">Dependencies</div>';
        body += item.deps.map(d=>`<div class="prop"><span class="val">${esc(d)}</span></div>`).join('');
      }

      panel.innerHTML = `<div class="detail-card ${item.action}">
        <h3>${iconFor(item.type)} ${esc(item.name)}</h3>
        <div class="dtype">${esc(item.address)}</div>
        <div class="action-tag ${item.action}" style="display:inline-block;margin-bottom:10px">${lbl}</div>
        ${body}
      </div>`;
      const ic = panel.querySelector('h3 svg');
      if (ic) { ic.style.width='20px'; ic.style.height='20px'; ic.style.flexShrink='0'; }
    }

    function propsHTML(obj) {
      return Object.entries(obj).filter(([,v])=>v!==null)
        .map(([k,v])=>`<div class="prop"><span class="key">${esc(k)}</span> <span class="val">${esc(JSON.stringify(v,null,2))}</span></div>`).join('');
    }

    /* ========== EXT-APPS WIRING ========== */
    app.ontoolresult = ({ content }) => {
      const text = content?.find(c => c.type === 'text');
      if (text) {
        try { render(JSON.parse(text.text)); }
        catch(e) { root.textContent = 'Error: ' + e.message; }
      }
    };
    function handleCtx(ctx) {
      if (ctx.safeAreaInsets) {
        document.body.style.paddingTop    = ctx.safeAreaInsets.top + 'px';
        document.body.style.paddingRight  = ctx.safeAreaInsets.right + 'px';
        document.body.style.paddingBottom = ctx.safeAreaInsets.bottom + 'px';
        document.body.style.paddingLeft   = ctx.safeAreaInsets.left + 'px';
      }
    }
    app.onhostcontextchanged = handleCtx;
    await app.connect();
    const ctx = app.getHostContext();
    if (ctx) handleCtx(ctx);
  </script>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Tool — returns structured plan data; the UI resource renders it
# ---------------------------------------------------------------------------

@mcp.tool(ui=ToolUI(resource_uri=VIEW_URI))
def visualize_tf_diff(plan: str) -> str:
    """
    Visualize Terraform plan changes as an interactive cloud architecture diagram.

    Generates an MCP App with clickable resources showing configuration details
    and before/after comparisons. Operates entirely offline without cloud credentials.

    Args:
        plan: Terraform plan JSON as a string (from `terraform show -json tfplan`)

    Returns:
        The parsed plan data as JSON for the MCP App UI to render
    """
    try:
        plan_data = json.loads(plan)
    except json.JSONDecodeError as e:
        return json.dumps({"error": f"Invalid JSON: {e}"})

    if "resource_changes" not in plan_data:
        return json.dumps({"error": "Invalid Terraform plan — missing 'resource_changes'."})

    # Try to generate SVG server-side with official cloud provider icons
    try:
        from cloud_diff_mcp.visualizer_hierarchical import generate_svg
        from cloud_diff_mcp.svg_embedder import embed_icons_in_svg_content
        svg = generate_svg(plan_data)
        svg = embed_icons_in_svg_content(svg)
        # Remove surrogate characters that break UTF-8 JSON serialisation
        svg = svg.encode("utf-8", errors="surrogatepass").decode("utf-8", errors="replace")
        plan_data["_server_svg"] = svg
    except Exception:
        pass  # Fall back to client-side icon rendering

    result = json.dumps(plan_data, ensure_ascii=True)
    # Belt-and-suspenders: strip any surviving surrogate code points that
    # would cause PydanticSerializationError in the MCP stdio transport.
    result = result.encode("utf-8", errors="surrogatepass").decode("utf-8", errors="replace")
    return result


# ---------------------------------------------------------------------------
# UI Resource — serves the interactive HTML viewer
# ---------------------------------------------------------------------------

@mcp.resource(
    VIEW_URI,
    ui=ResourceUI(
        csp=ResourceCSP(resource_domains=["https://unpkg.com"]),
    ),
)
def visualization_view() -> str:
    """Interactive Terraform plan viewer — renders tool results as architecture diagrams."""
    return EMBEDDED_VIEW_HTML


def main() -> None:
    """Main entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
