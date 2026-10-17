import { parsePatch } from "./parser.js?v=0.2.1";

const ASSET_VERSION = "0.2.1";

const $ = (selector) => document.querySelector(selector);
const elements = {
  hero: $("#hero"), workspace: $("#workspace"), error: $("#error-card"), errorMessage: $("#error-message"),
  dropZone: $("#drop-zone"), input: $("#file-input"), choose: $("#choose-button"), demo: $("#demo-button"),
  reset: $("#new-file-button"), errorReset: $("#error-reset"), export: $("#export-button"), search: $("#module-search"),
  patchName: $("#patch-name"), fileName: $("#file-name"), modules: $("#module-list"), pages: $("#page-list"),
  chart: $("#strength-chart"), emptyFilter: $("#empty-filter"), graph: $("#graph-canvas"),
  graphModules: $("#graph-modules"), connectionLayer: $("#connection-layer"), pageFilters: $("#page-filters"),
  dialog: $("#module-dialog")
};

let moduleIndex;
let currentPatch;
let currentFileName = "patch.bin";

async function getModuleIndex() {
  if (!moduleIndex) {
    const response = await fetch(`./data/modules.json?v=${ASSET_VERSION}`);
    if (!response.ok) throw new Error("The module catalog could not be loaded.");
    moduleIndex = await response.json();
  }
  return moduleIndex;
}

async function inspectBuffer(buffer, fileName) {
  try {
    currentPatch = parsePatch(buffer, await getModuleIndex());
    currentFileName = fileName;
    render(currentPatch);
    elements.hero.hidden = true;
    elements.error.hidden = true;
    elements.workspace.hidden = false;
    window.scrollTo({ top: 0, behavior: "smooth" });
  } catch (error) {
    elements.hero.hidden = true;
    elements.workspace.hidden = true;
    elements.error.hidden = false;
    elements.errorMessage.textContent = error instanceof Error ? error.message : "An unknown decoding error occurred.";
  }
}

async function inspectFile(file) {
  if (!file) return;
  if (!file.name.toLowerCase().endsWith(".bin")) {
    elements.hero.hidden = true;
    elements.error.hidden = false;
    elements.errorMessage.textContent = "Please choose a ZOIA .bin patch file.";
    return;
  }
  await inspectBuffer(await file.arrayBuffer(), file.name);
}

function render(patch) {
  elements.patchName.textContent = patch.name;
  elements.fileName.textContent = currentFileName;
  $("#module-count").textContent = patch.meta.moduleCount;
  $("#connection-count").textContent = patch.meta.connectionCount;
  $("#page-count").textContent = patch.meta.pageCount;
  $("#cpu-total").textContent = `${patch.meta.estimatedCpu}%`;
  elements.search.value = "";
  renderModules(patch.modules);
  elements.pages.replaceChildren(...patch.pages.map((page) => {
    const row = document.createElement("div");
    row.className = "page-item";
    row.innerHTML = `<span class="page-index">${String(page.number + 1).padStart(2, "0")}</span><b></b><span>${page.moduleCount} mod${page.moduleCount === 1 ? "" : "s"}</span>`;
    row.querySelector("b").textContent = page.name;
    return row;
  }));
  renderChart(patch.connections);
  renderVisualizer(patch);
}

function renderModules(modules) {
  elements.modules.replaceChildren(...modules.map((module) => {
    const row = document.createElement("div");
    row.className = "module-row";
    row.dataset.search = `${module.displayName} ${module.type} ${module.category}`.toLowerCase();
    row.innerHTML = `
      <span class="module-number">${String(module.number + 1).padStart(2, "0")}</span>
      <span class="module-name"><strong></strong><span></span></span>
      <span class="category"></span>
      <span class="page-num">PG ${module.page + 1}</span>
      <span class="cpu"><i class="color-dot"></i>${module.cpu}%</span>`;
    row.querySelector("strong").textContent = module.displayName;
    row.querySelector(".module-name span").textContent = module.customName ? module.type : `v${module.version}`;
    row.querySelector(".category").textContent = module.category;
    row.querySelector(".color-dot").style.background = module.colorHex;
    row.tabIndex = 0;
    row.setAttribute("role", "button");
    row.setAttribute("aria-label", `View details for ${module.displayName}`);
    row.addEventListener("click", () => showModuleDetails(module));
    row.addEventListener("keydown", (event) => { if (event.key === "Enter" || event.key === " ") showModuleDetails(module); });
    return row;
  }));
  elements.emptyFilter.hidden = modules.length > 0;
}

function renderVisualizer(patch) {
  const pageWidth = 910;
  const canvasWidth = Math.max(1080, patch.pages.length * pageWidth);
  const canvasHeight = 560;
  elements.graph.style.width = `${canvasWidth}px`;
  elements.graph.style.height = `${canvasHeight}px`;
  elements.connectionLayer.setAttribute("viewBox", `0 0 ${canvasWidth} ${canvasHeight}`);

  const positions = new Map();
  const cards = patch.modules.map((module) => {
    const gridPosition = Math.max(0, module.position);
    const column = gridPosition % 8;
    const row = Math.min(4, Math.floor(gridPosition / 8));
    const x = module.page * pageWidth + 34 + column * 108;
    const y = 62 + row * 96;
    positions.set(module.number, { x: x + 47, y: y + 31 });
    const card = document.createElement("button");
    card.type = "button";
    card.className = "graph-module";
    card.dataset.page = String(module.page);
    card.style.cssText = `left:${x}px;top:${y}px;--module-color:${module.colorHex}`;
    card.innerHTML = `<span class="graph-index"></span><strong></strong><small></small>`;
    card.querySelector(".graph-index").textContent = String(module.number + 1).padStart(2, "0");
    card.querySelector("strong").textContent = module.displayName;
    card.querySelector("small").textContent = module.category;
    card.addEventListener("click", () => showModuleDetails(module));
    return card;
  });
  elements.graphModules.replaceChildren(...cards);

  const namespace = "http://www.w3.org/2000/svg";
  const pageGuides = patch.pages.map((page) => {
    const group = document.createElementNS(namespace, "g");
    group.classList.add("page-guide");
    group.dataset.page = String(page.number);
    const rect = document.createElementNS(namespace, "rect");
    rect.setAttribute("x", String(page.number * pageWidth + 12));
    rect.setAttribute("y", "18");
    rect.setAttribute("width", String(pageWidth - 24));
    rect.setAttribute("height", "520");
    const label = document.createElementNS(namespace, "text");
    label.setAttribute("x", String(page.number * pageWidth + 32));
    label.setAttribute("y", "43");
    label.textContent = `${String(page.number + 1).padStart(2, "0")}  ${page.name}`;
    group.append(rect, label);
    return group;
  });
  const paths = patch.connections.map((connection, index) => {
    const source = positions.get(connection.sourceModule);
    const destination = positions.get(connection.destinationModule);
    if (!source || !destination) return null;
    const path = document.createElementNS(namespace, "path");
    const bend = Math.max(42, Math.abs(destination.x - source.x) * .42);
    path.setAttribute("d", `M ${source.x} ${source.y} C ${source.x + bend} ${source.y}, ${destination.x - bend} ${destination.y}, ${destination.x} ${destination.y}`);
    path.setAttribute("class", "connection-path");
    path.dataset.sourcePage = String(patch.modules[connection.sourceModule]?.page ?? -1);
    path.dataset.destinationPage = String(patch.modules[connection.destinationModule]?.page ?? -1);
    path.style.setProperty("--route-delay", `${(index % 12) * 35}ms`);
    const title = document.createElementNS(namespace, "title");
    title.textContent = `${patch.modules[connection.sourceModule]?.displayName || "Module"} → ${patch.modules[connection.destinationModule]?.displayName || "Module"} · ${connection.strength}%`;
    path.append(title);
    return path;
  }).filter(Boolean);
  elements.connectionLayer.replaceChildren(...pageGuides, ...paths);

  const filterButtons = [{ number: -1, name: "All pages" }, ...patch.pages].map((page, index) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `page-filter${index === 0 ? " active" : ""}`;
    button.textContent = page.number === -1 ? page.name : String(page.number + 1).padStart(2, "0");
    button.title = page.name;
    button.addEventListener("click", () => filterGraph(page.number, button));
    return button;
  });
  elements.pageFilters.replaceChildren(...filterButtons);
  $("#visible-module-count").textContent = `${patch.modules.length} modules`;
}

function filterGraph(pageNumber, activeButton) {
  elements.pageFilters.querySelectorAll("button").forEach((button) => button.classList.toggle("active", button === activeButton));
  elements.graphModules.querySelectorAll(".graph-module").forEach((module) => {
    module.hidden = pageNumber >= 0 && Number(module.dataset.page) !== pageNumber;
  });
  elements.connectionLayer.querySelectorAll(".connection-path").forEach((path) => {
    path.hidden = pageNumber >= 0 && Number(path.dataset.sourcePage) !== pageNumber && Number(path.dataset.destinationPage) !== pageNumber;
  });
  elements.connectionLayer.querySelectorAll(".page-guide").forEach((guide) => {
    guide.classList.toggle("muted", pageNumber >= 0 && Number(guide.dataset.page) !== pageNumber);
  });
  const visible = pageNumber < 0 ? currentPatch.modules.length : currentPatch.modules.filter((module) => module.page === pageNumber).length;
  $("#visible-module-count").textContent = `${visible} module${visible === 1 ? "" : "s"}`;
  if (pageNumber >= 0) document.querySelector(".graph-scroll").scrollTo({ left: pageNumber * 910, behavior: "smooth" });
}

function showModuleDetails(module) {
  $("#dialog-color").style.background = module.colorHex;
  $("#dialog-category").textContent = module.category;
  $("#dialog-name").textContent = module.displayName;
  $("#dialog-type").textContent = module.customName ? `${module.type} · Custom label` : `Module ${module.number + 1} · ${module.color}`;
  $("#dialog-description").textContent = module.description;
  const facts = [
    ["Page", `${module.page + 1}`], ["Grid position", `${module.position + 1}`],
    ["Version", `${module.version}`], ["Estimated CPU", `${module.cpu}%`]
  ];
  $("#module-facts").replaceChildren(...facts.flatMap(([label, value]) => {
    const term = document.createElement("dt"); term.textContent = label;
    const detail = document.createElement("dd"); detail.textContent = value;
    return [term, detail];
  }));
  $("#parameter-count").textContent = `${module.parameters.length} saved`;
  $("#parameter-list").replaceChildren(...module.parameters.map((parameter) => {
    const row = document.createElement("div");
    row.className = "parameter-row";
    row.innerHTML = `<span></span><div class="parameter-meter"><i></i></div><code></code>`;
    row.querySelector("span").textContent = parameter.name.replaceAll("_", " ");
    row.querySelector("i").style.width = `${Math.max(0, Math.min(100, parameter.normalized * 100))}%`;
    row.querySelector("code").textContent = parameter.normalized.toFixed(3);
    return row;
  }));
  if (!module.parameters.length) {
    const empty = document.createElement("p"); empty.className = "no-parameters"; empty.textContent = "This module has no saved parameters.";
    $("#parameter-list").append(empty);
  }
  elements.dialog.showModal();
}

function renderChart(connections) {
  const buckets = Array(10).fill(0);
  connections.forEach(({ strength }) => {
    const bucket = Math.max(0, Math.min(9, Math.floor(Math.abs(strength) / 10)));
    buckets[bucket] += 1;
  });
  const max = Math.max(1, ...buckets);
  elements.chart.replaceChildren(...buckets.map((count, index) => {
    const item = document.createElement("div");
    item.className = "bar-wrap";
    item.title = `${count} connection${count === 1 ? "" : "s"} between ${index * 10}% and ${index === 9 ? "100+" : (index + 1) * 10 + "%"}`;
    item.innerHTML = `<div class="bar" style="height:${Math.max(2, count / max * 100)}%"></div><small>${index * 10}</small>`;
    return item;
  }));
}

function reset() {
  currentPatch = undefined;
  elements.input.value = "";
  elements.workspace.hidden = true;
  elements.error.hidden = true;
  elements.hero.hidden = false;
  window.scrollTo({ top: 0, behavior: "smooth" });
}

elements.choose.addEventListener("click", () => elements.input.click());
elements.dropZone.addEventListener("click", (event) => { if (!event.target.closest("button")) elements.input.click(); });
elements.input.addEventListener("change", () => inspectFile(elements.input.files?.[0]));
elements.demo.addEventListener("click", async () => {
  try {
    const response = await fetch(`./sample/demo.bin?v=${ASSET_VERSION}`);
    if (!response.ok) throw new Error("The demo patch could not be loaded.");
    await inspectBuffer(await response.arrayBuffer(), "000_zoia_Juniper.bin");
  } catch (error) {
    elements.hero.hidden = true;
    elements.error.hidden = false;
    elements.errorMessage.textContent = error.message;
  }
});
[elements.reset, elements.errorReset].forEach((button) => button.addEventListener("click", reset));
["dragenter", "dragover"].forEach((name) => elements.dropZone.addEventListener(name, (event) => {
  event.preventDefault(); elements.dropZone.classList.add("dragging");
}));
["dragleave", "drop"].forEach((name) => elements.dropZone.addEventListener(name, (event) => {
  event.preventDefault(); elements.dropZone.classList.remove("dragging");
}));
elements.dropZone.addEventListener("drop", (event) => inspectFile(event.dataTransfer?.files?.[0]));
elements.search.addEventListener("input", () => {
  const query = elements.search.value.trim().toLowerCase();
  let visible = 0;
  elements.modules.querySelectorAll(".module-row").forEach((row) => {
    row.hidden = !row.dataset.search.includes(query);
    if (!row.hidden) visible += 1;
  });
  elements.emptyFilter.hidden = visible > 0;
});
elements.export.addEventListener("click", () => {
  if (!currentPatch) return;
  const blob = new Blob([JSON.stringify(currentPatch, null, 2)], { type: "application/json" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = `${currentFileName.replace(/\.bin$/i, "")}.json`;
  link.click();
  URL.revokeObjectURL(link.href);
});
document.querySelectorAll(".view-tab").forEach((tab) => tab.addEventListener("click", () => {
  document.querySelectorAll(".view-tab").forEach((item) => item.classList.toggle("active", item === tab));
  $("#inventory-view").hidden = tab.dataset.view !== "inventory";
  $("#visualizer-view").hidden = tab.dataset.view !== "visualizer";
}));
$("#dialog-close").addEventListener("click", () => elements.dialog.close());
elements.dialog.addEventListener("click", (event) => {
  const rect = elements.dialog.getBoundingClientRect();
  if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) elements.dialog.close();
});
