import React, { useState, useCallback } from "react";
import type { PlanData, ResourceItem } from "../types";
import { parsePlanData } from "../types";
import { Header } from "./Header";
import { Legend } from "./Legend";
import { DetailPanel } from "./DetailPanel";
import { SvgViewer } from "./SvgViewer";
import { DiagramView } from "./DiagramView";

interface AppProps {
  planData: PlanData;
}

export const App: React.FC<AppProps> = ({ planData }) => {
  const [selectedResource, setSelectedResource] = useState<ResourceItem | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const { items, counts, connections, isArchMode } = parsePlanData(planData);

  const serverSvg = planData._server_svg || null;

  const title = isArchMode
    ? (planData.title || "Cloud Architecture")
    : "Cloud Architecture Diff";

  const subtitle = isArchMode
    ? `${items.length} resources`
    : `Terraform &mdash; ${items.length} resources &mdash; v${planData.terraform_version || "?"}`;

  const handleSelectResource = useCallback((item: ResourceItem) => {
    setSelectedResource((prev) => {
      if (prev && prev.address === item.address) {
        // Toggle off
        setSidebarOpen(false);
        return null;
      }
      // Select new
      setSidebarOpen(true);
      return item;
    });
  }, []);

  const handleCloseSidebar = useCallback(() => {
    setSidebarOpen(false);
    setSelectedResource(null);
  }, []);

  return (
    <>
      <Header title={title} subtitle={subtitle} counts={counts} />
      <div className="content">
        {serverSvg ? (
          <SvgViewer
            svgContent={serverSvg}
            items={items}
            selectedAddress={selectedResource?.address ?? null}
            onSelectResource={handleSelectResource}
          />
        ) : (
          <DiagramView
            items={items}
            connections={connections}
            onSelectResource={handleSelectResource}
          />
        )}
        {sidebarOpen && (
          <DetailPanel item={selectedResource} onClose={handleCloseSidebar} />
        )}
      </div>
      <Legend showConnectionTypes={true} />
    </>
  );
};
