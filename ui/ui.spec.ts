import { test, expect, type Page } from "@playwright/test";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const HARNESS = path.resolve(__dirname, "test-harness.html");

async function loadApp(page: Page) {
  await page.goto(`file://${HARNESS}`);
  // Wait for SVG to render inside the viewport
  await page.waitForSelector(".svg-viewport svg", { timeout: 5000 });
}

function nodeSelector(index: number) {
  return `.svg-viewport svg .node >> nth=${index}`;
}

test.describe("Cloud Diagram UI", () => {
  test("renders SVG diagram with nodes", async ({ page }) => {
    await loadApp(page);
    const nodes = page.locator(".svg-viewport svg .node");
    const count = await nodes.count();
    expect(count).toBeGreaterThan(0);
    console.log(`Found ${count} clickable nodes`);
  });

  test("sidebar is closed by default", async ({ page }) => {
    await loadApp(page);
    const sidebar = page.locator(".sidebar");
    await expect(sidebar).toHaveCount(0);
  });

  test("clicking a node opens sidebar", async ({ page }) => {
    await loadApp(page);
    const nodes = page.locator(".svg-viewport svg .node");
    const count = await nodes.count();
    expect(count).toBeGreaterThan(0);

    // Click first node
    await nodes.nth(0).click();
    // Sidebar should appear
    const sidebar = page.locator(".sidebar");
    await expect(sidebar).toBeVisible({ timeout: 2000 });
    // Detail card should have content
    const card = page.locator(".detail-card");
    await expect(card).toBeVisible();
    console.log("Sidebar opened after clicking first node");
  });

  test("clicking a different node switches sidebar content", async ({ page }) => {
    await loadApp(page);
    const nodes = page.locator(".svg-viewport svg .node");
    const count = await nodes.count();
    expect(count).toBeGreaterThanOrEqual(2);

    // Click first node
    await nodes.nth(0).click();
    const sidebar = page.locator(".sidebar");
    await expect(sidebar).toBeVisible({ timeout: 2000 });

    // Capture initial sidebar text
    const text1 = await sidebar.innerText();

    // Click second node
    await nodes.nth(1).click();
    await expect(sidebar).toBeVisible({ timeout: 2000 });

    // Sidebar should still be open with different content
    const text2 = await sidebar.innerText();
    expect(text2).not.toBe(text1);
    console.log("Sidebar switched content when clicking different node");
  });

  test("clicking same node again closes sidebar", async ({ page }) => {
    await loadApp(page);
    const nodes = page.locator(".svg-viewport svg .node");

    // Click first node to open
    await nodes.nth(0).click();
    const sidebar = page.locator(".sidebar");
    await expect(sidebar).toBeVisible({ timeout: 2000 });

    // Click same node again to close
    await nodes.nth(0).click();
    await expect(sidebar).toHaveCount(0, { timeout: 2000 });
    console.log("Sidebar closed after clicking same node again");
  });

  test("sidebar close button works", async ({ page }) => {
    await loadApp(page);
    const nodes = page.locator(".svg-viewport svg .node");

    // Click to open
    await nodes.nth(0).click();
    const sidebar = page.locator(".sidebar");
    await expect(sidebar).toBeVisible({ timeout: 2000 });

    // Click close button
    await page.locator(".sidebar-close").click();
    await expect(sidebar).toHaveCount(0, { timeout: 2000 });
    console.log("Sidebar closed via close button");
  });

  test("can reopen sidebar after closing with close button", async ({ page }) => {
    await loadApp(page);
    const nodes = page.locator(".svg-viewport svg .node");

    // Open sidebar
    await nodes.nth(0).click();
    const sidebar = page.locator(".sidebar");
    await expect(sidebar).toBeVisible({ timeout: 2000 });

    // Close with button
    await page.locator(".sidebar-close").click();
    await expect(sidebar).toHaveCount(0, { timeout: 2000 });

    // Reopen by clicking another node
    await nodes.nth(1).click();
    await expect(sidebar).toBeVisible({ timeout: 2000 });
    console.log("Sidebar reopened after close button");
  });

  test("can reopen sidebar after closing by toggle", async ({ page }) => {
    await loadApp(page);
    const nodes = page.locator(".svg-viewport svg .node");

    // Open sidebar
    await nodes.nth(0).click();
    const sidebar = page.locator(".sidebar");
    await expect(sidebar).toBeVisible({ timeout: 2000 });

    // Close by clicking same node
    await nodes.nth(0).click();
    await expect(sidebar).toHaveCount(0, { timeout: 2000 });

    // Reopen by clicking same node again
    await nodes.nth(0).click();
    await expect(sidebar).toBeVisible({ timeout: 2000 });
    console.log("Sidebar reopened after toggle close");
  });

  test("can click multiple distinct nodes in sequence", async ({ page }) => {
    await loadApp(page);
    const nodes = page.locator(".svg-viewport svg .node");
    const count = await nodes.count();

    // Find nodes with distinct text labels to avoid toggle-close
    const seen = new Set<string>();
    const distinctIndices: number[] = [];
    for (let i = 0; i < count && distinctIndices.length < 4; i++) {
      const texts = await nodes.nth(i).evaluate((el) =>
        Array.from(el.querySelectorAll("text")).map((t) => t.textContent?.trim()).join("|")
      );
      const label = texts.replace(/^\[.*?\]\s*/, "");
      if (!seen.has(label)) {
        seen.add(label);
        distinctIndices.push(i);
      }
    }

    for (const idx of distinctIndices) {
      await nodes.nth(idx).click();
      const sidebar = page.locator(".sidebar");
      await expect(sidebar).toBeVisible({ timeout: 2000 });
      console.log(`Clicked node ${idx}, sidebar visible`);
    }
    console.log(`Sequential clicks on ${distinctIndices.length} distinct nodes all worked`);
  });

  test("selected node has visual highlight", async ({ page }) => {
    await loadApp(page);
    const nodes = page.locator(".svg-viewport svg .node");

    await nodes.nth(0).click();
    await page.locator(".sidebar").waitFor({ state: "visible", timeout: 2000 });

    // Check that the clicked node has outline styling
    const style = await nodes.nth(0).evaluate((el) => {
      return (el as HTMLElement).style.outline;
    });
    expect(style).toContain("solid");
    console.log(`Selected node outline: ${style}`);
  });

  test("zoom does not reset when clicking nodes", async ({ page }) => {
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

    // Click a node
    const nodes = page.locator(".svg-viewport svg .node");
    await nodes.nth(0).click();
    await page.locator(".sidebar").waitFor({ state: "visible", timeout: 2000 });

    // Transform should NOT have reset
    const transform3 = await svg.evaluate((el) => (el as SVGElement).style.transform);
    expect(transform3).toBe(transform2);
    console.log("Zoom preserved after clicking node");
  });

  test("app has minimum height of 800px", async ({ page }) => {
    await page.setViewportSize({ width: 800, height: 400 });
    await loadApp(page);

    const bodyHeight = await page.evaluate(() => document.body.offsetHeight);
    expect(bodyHeight).toBeGreaterThanOrEqual(800);
    console.log(`Body height: ${bodyHeight}px`);
  });

  test("header, content, and legend are all visible", async ({ page }) => {
    await loadApp(page);
    await expect(page.locator(".header")).toBeVisible();
    await expect(page.locator(".content")).toBeVisible();
    await expect(page.locator(".legend")).toBeVisible();
    console.log("Header, content, and legend all visible");
  });

  test("nodes with same name open correct sidebar (address-based matching)", async ({ page }) => {
    await loadApp(page);
    // Find the two "web" nodes (aws_instance.web and aws_security_group.web)
    const nodes = page.locator(".svg-viewport svg .node");
    const count = await nodes.count();

    // Build a map of title (address) to index
    const nodeInfo: { idx: number; title: string; texts: string }[] = [];
    for (let i = 0; i < count; i++) {
      const info = await nodes.nth(i).evaluate((el) => {
        const title = el.querySelector("title")?.textContent?.trim() || "";
        const texts = Array.from(el.querySelectorAll("text")).map((t) => t.textContent?.trim()).join(" ");
        return { title, texts };
      });
      nodeInfo.push({ idx: i, ...info });
    }

    const sgWeb = nodeInfo.find((n) => n.title === "aws_security_group.web");
    const instWeb = nodeInfo.find((n) => n.title === "aws_instance.web");
    expect(sgWeb).toBeDefined();
    expect(instWeb).toBeDefined();

    // Click security group "web" — sidebar should show security group type
    await nodes.nth(sgWeb!.idx).click();
    const sidebar = page.locator(".sidebar");
    await expect(sidebar).toBeVisible({ timeout: 2000 });
    const sgText = await sidebar.innerText();
    expect(sgText).toContain("aws_security_group");
    console.log(`Security group web sidebar: contains aws_security_group ✓`);

    // Click instance "web" — sidebar should switch to instance type
    await nodes.nth(instWeb!.idx).click();
    await expect(sidebar).toBeVisible({ timeout: 2000 });
    const instText = await sidebar.innerText();
    expect(instText).toContain("aws_instance");
    console.log(`Instance web sidebar: contains aws_instance ✓`);
  });
});
