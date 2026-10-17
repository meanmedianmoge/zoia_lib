import { parsePatch } from "./parser.js";

const $ = (selector) => document.querySelector(selector);
const elements = {
  hero: $("#hero"), workspace: $("#workspace"), error: $("#error-card"), errorMessage: $("#error-message"),
  dropZone: $("#drop-zone"), input: $("#file-input"), choose: $("#choose-button"), demo: $("#demo-button"),
  reset: $("#new-file-button"), errorReset: $("#error-reset"), export: $("#export-button"), search: $("#module-search"),
  patchName: $("#patch-name"), fileName: $("#file-name"), modules: $("#module-list"), pages: $("#page-list"),
  chart: $("#strength-chart"), emptyFilter: $("#empty-filter")
};

let moduleIndex;
let currentPatch;
let currentFileName = "patch.bin";

async function getModuleIndex() {
  if (!moduleIndex) {
    const response = await fetch("./data/modules.json");
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
    return row;
  }));
  elements.emptyFilter.hidden = modules.length > 0;
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
    const response = await fetch("./sample/demo.bin");
    if (!response.ok) throw new Error("The demo patch could not be loaded.");
    await inspectBuffer(await response.arrayBuffer(), "demo_patch.bin");
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
