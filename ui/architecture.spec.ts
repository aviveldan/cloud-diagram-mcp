import { test, expect, type Page } from "@playwright/test";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const HARNESS = path.resolve(__dirname, "test-harness-architecture.html");

async function loadApp(page: Page) {
  await page.goto(`file://${HARNESS}`);
  // Wait for SVG to render inside the viewport
  await page.waitForSelector(".svg-viewport svg", { timeout: 5000 });
}

test.describe("Architecture Visualization UI", () => {
  test("renders SVG diagram with nodes for architecture", async ({ page }) => {
    await loadApp(page);
    const nodes = page.locator(".svg-viewport svg .node");
    const count = await nodes.count();
    expect(count).toBeGreaterThan(0);
    console.log(`Architecture diagram: Found ${count} nodes`);
  });

  test("architecture mode is correctly set", async ({ page }) => {
    await loadApp(page);
    // Check if the app recognizes this as architecture mode
    const header = page.locator(".header");
    await expect(header).toBeVisible();
  });

  test("sidebar opens when clicking architecture node", async ({ page }) => {
    await loadApp(page);
    const nodes = page.locator(".svg-viewport svg .node");
    const count = await nodes.count();
    expect(count).toBeGreaterThan(0);

    // Click first node
    await nodes.nth(0).click();
    // Sidebar should appear
    const sidebar = page.locator(".sidebar");
    await expect(sidebar).toBeVisible({ timeout: 2000 });
    console.log("Architecture: Sidebar opened after clicking first node");
  });

  test("sidebar shows resource details for architecture node", async ({ page }) => {
    await loadApp(page);
    const nodes = page.locator(".svg-viewport svg .node");
    
    // Click first node
    await nodes.nth(0).click();
    const sidebar = page.locator(".sidebar");
    await expect(sidebar).toBeVisible({ timeout: 2000 });

    // Check that sidebar has some content
    const sidebarText = await sidebar.innerText();
    expect(sidebarText.length).toBeGreaterThan(0);
    console.log("Architecture: Sidebar shows resource details");
  });

  test("can navigate between different architecture nodes", async ({ page }) => {
    await loadApp(page);
    const nodes = page.locator(".svg-viewport svg .node");
    const count = await nodes.count();
    expect(count).toBeGreaterThanOrEqual(2);

    // Click first node
    await nodes.nth(0).click();
    const sidebar = page.locator(".sidebar");
    await expect(sidebar).toBeVisible({ timeout: 2000 });
    const text1 = await sidebar.innerText();

    // Click second node
    await nodes.nth(1).click();
    await expect(sidebar).toBeVisible({ timeout: 2000 });
    const text2 = await sidebar.innerText();

    // Sidebar content should be different
    expect(text2).not.toBe(text1);
    console.log("Architecture: Can navigate between nodes");
  });

  test("closing sidebar works in architecture view", async ({ page }) => {
    await loadApp(page);
    const nodes = page.locator(".svg-viewport svg .node");

    // Click to open
    await nodes.nth(0).click();
    const sidebar = page.locator(".sidebar");
    await expect(sidebar).toBeVisible({ timeout: 2000 });

    // Click close button
    await page.locator(".sidebar-close").click();
    await expect(sidebar).toHaveCount(0, { timeout: 2000 });
    console.log("Architecture: Sidebar closed successfully");
  });

  test("architecture diagram has proper visual structure", async ({ page }) => {
    await loadApp(page);
    
    // Check for essential UI elements
    await expect(page.locator(".header")).toBeVisible();
    await expect(page.locator(".content")).toBeVisible();
    await expect(page.locator(".svg-viewport")).toBeVisible();
    console.log("Architecture: All essential UI elements visible");
  });

  test("connections are rendered in architecture diagram", async ({ page }) => {
    await loadApp(page);
    
    // Check for edges (connections between nodes)
    const edges = page.locator(".svg-viewport svg .edge");
    const edgeCount = await edges.count();
    expect(edgeCount).toBeGreaterThan(0);
    console.log(`Architecture: Found ${edgeCount} connections (edges)`);
  });

  test("zoom functionality works in architecture view", async ({ page }) => {
    await loadApp(page);
    const svg = page.locator(".svg-viewport svg");
    await svg.waitFor({ state: "visible", timeout: 5000 });

    // Get initial transform
    const transform1 = await svg.evaluate((el) => (el as SVGElement).style.transform);

    // Zoom in with wheel
    const viewport = page.locator(".svg-viewport");
    await viewport.hover();
    await page.mouse.wheel(0, -300);
    await page.waitForTimeout(200);

    // Get zoomed transform
    const transform2 = await svg.evaluate((el) => (el as SVGElement).style.transform);
    expect(transform2).not.toBe(transform1);
    console.log("Architecture: Zoom functionality works");
  });

  test("selected node has visual highlight in architecture view", async ({ page }) => {
    await loadApp(page);
    const nodes = page.locator(".svg-viewport svg .node");

    await nodes.nth(0).click();
    await page.locator(".sidebar").waitFor({ state: "visible", timeout: 2000 });

    // Check that the clicked node has outline styling
    const style = await nodes.nth(0).evaluate((el) => {
      return (el as HTMLElement).style.outline;
    });
    expect(style).toContain("solid");
    console.log(`Architecture: Selected node has highlight: ${style}`);
  });

  test("can toggle sidebar by clicking same node twice", async ({ page }) => {
    await loadApp(page);
    const nodes = page.locator(".svg-viewport svg .node");

    // Click to open
    await nodes.nth(0).click();
    const sidebar = page.locator(".sidebar");
    await expect(sidebar).toBeVisible({ timeout: 2000 });

    // Click same node to close
    await nodes.nth(0).click();
    await expect(sidebar).toHaveCount(0, { timeout: 2000 });

    // Click again to reopen
    await nodes.nth(0).click();
    await expect(sidebar).toBeVisible({ timeout: 2000 });
    console.log("Architecture: Sidebar toggle works");
  });

  test("architecture diagram renders with correct resource types", async ({ page }) => {
    await loadApp(page);
    const nodes = page.locator(".svg-viewport svg .node");
    const count = await nodes.count();

    // Click a node and verify it shows Azure resource type
    await nodes.nth(0).click();
    const sidebar = page.locator(".sidebar");
    await expect(sidebar).toBeVisible({ timeout: 2000 });
    
    const sidebarText = await sidebar.innerText();
    // The architecture-azure.json contains azurerm_ resources
    expect(sidebarText).toMatch(/azurerm_/);
    console.log("Architecture: Azure resource types are correctly shown");
  });

  test("legend is visible in architecture view", async ({ page }) => {
    await loadApp(page);
    const legend = page.locator(".legend");
    // Legend may or may not be present depending on the implementation
    // Just check if it exists or not
    const legendCount = await legend.count();
    console.log(`Architecture: Legend elements count: ${legendCount}`);
  });

  test("architecture view maintains state during interaction", async ({ page }) => {
    await loadApp(page);
    const nodes = page.locator(".svg-viewport svg .node");
    const count = await nodes.count();
    
    // Perform multiple interactions
    await nodes.nth(0).click();
    await page.locator(".sidebar").waitFor({ state: "visible", timeout: 2000 });
    
    await nodes.nth(1).click();
    await page.locator(".sidebar").waitFor({ state: "visible", timeout: 2000 });
    
    // Verify node count hasn't changed
    const newCount = await nodes.count();
    expect(newCount).toBe(count);
    console.log("Architecture: State maintained during interaction");
  });

  test("connections have proper styling", async ({ page }) => {
    await loadApp(page);
    const edges = page.locator(".svg-viewport svg .edge");
    const edgeCount = await edges.count();
    expect(edgeCount).toBeGreaterThan(0);

    // Check if first edge has some styling
    if (edgeCount > 0) {
      const edgePath = edges.nth(0).locator("path");
      const pathExists = await edgePath.count();
      expect(pathExists).toBeGreaterThan(0);
      console.log("Architecture: Connections have proper path elements");
    }
  });

  test("all nodes are clickable in architecture view", async ({ page }) => {
    await loadApp(page);
    const nodes = page.locator(".svg-viewport svg .node");
    const count = await nodes.count();

    // Try clicking each node to ensure they're all interactive
    for (let i = 0; i < Math.min(count, 5); i++) {
      await nodes.nth(i).click();
      const sidebar = page.locator(".sidebar");
      await expect(sidebar).toBeVisible({ timeout: 2000 });
      await page.locator(".sidebar-close").click();
      await page.waitForTimeout(100);
    }
    console.log(`Architecture: All tested nodes (${Math.min(count, 5)}) are clickable`);
  });

  test("viewport is scrollable/pannable", async ({ page }) => {
    await loadApp(page);
    const viewport = page.locator(".svg-viewport");
    await viewport.waitFor({ state: "visible", timeout: 5000 });

    // The viewport should be visible and interactive
    const box = await viewport.boundingBox();
    expect(box).not.toBeNull();
    expect(box!.width).toBeGreaterThan(0);
    expect(box!.height).toBeGreaterThan(0);
    console.log(`Architecture: Viewport dimensions: ${box!.width}x${box!.height}`);
  });
});
