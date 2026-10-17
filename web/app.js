import { parsePatch } from "./parser.js?v=0.9.1";
import { getPatch, getRevision, listBanks, listPatches, listRevisions, patchId, removeBank, removePatch, removeRevision, saveBank, savePatch, saveRevision } from "./library.js?v=0.9.1";
import { browsePatches, downloadPatchFile, getPatchDetails } from "./patchstorage.js?v=0.9.1";
import { createZip, readZip } from "./zip.js?v=0.9.1";

const ASSET_VERSION = "0.9.1";

const $ = (selector) => document.querySelector(selector);
const elements = {
  hero: $("#hero"), workspace: $("#workspace"), error: $("#error-card"), errorMessage: $("#error-message"),
  dropZone: $("#drop-zone"), input: $("#file-input"), choose: $("#choose-button"), demo: $("#demo-button"),
  reset: $("#new-file-button"), errorReset: $("#error-reset"), export: $("#export-button"), search: $("#module-search"),
  patchName: $("#patch-name"), fileName: $("#file-name"), modules: $("#module-list"), pages: $("#page-list"),
  chart: $("#strength-chart"), emptyFilter: $("#empty-filter"), graph: $("#graph-canvas"),
  graphModules: $("#graph-modules"), connectionLayer: $("#connection-layer"), pageFilters: $("#page-filters"),
  dialog: $("#module-dialog"), library: $("#library"), libraryList: $("#library-list"),
  libraryEmpty: $("#library-empty"), libraryInput: $("#library-file-input"), librarySearch: $("#library-search"),
  librarySort: $("#library-sort"), libraryStatus: $("#library-status"), browse: $("#browse"),
  patchGrid: $("#patch-grid"), browseMessage: $("#browse-message"), patchDialog: $("#patch-dialog"),
  banks: $("#banks"), bankList: $("#bank-list"), bankSlots: $("#bank-slots"), bankPatchList: $("#bank-patch-list"),
  metadataDialog: $("#metadata-dialog"), versionsDialog: $("#versions-dialog")
};

let moduleIndex;
let currentPatch;
let currentFileName = "patch.bin";
let currentBuffer;
let libraryRecords = [];
let browsePage = 1;
let browseTotalPages = 1;
let browseQuery = "";
let selectedCommunityPatch;
let bankRecords = [];
let activeBank;
let selectedBankPatchId;
let bankNameTimer;
let currentLibraryRecordId;
let metadataRecord;
let metadataRating = 0;
let versionPatchRecord;
let revisionRecords = [];
let selectedRevisionIds = new Set();

async function getModuleIndex() {
  if (!moduleIndex) {
    const response = await fetch(`./data/modules.json?v=${ASSET_VERSION}`);
    if (!response.ok) throw new Error("The module catalog could not be loaded.");
    moduleIndex = await response.json();
  }
  return moduleIndex;
}

async function inspectBuffer(buffer, fileName, { persist = false, lastModified = 0, recordId, displayTitle } = {}) {
  try {
    currentPatch = parsePatch(buffer, await getModuleIndex());
    currentFileName = fileName;
    currentBuffer = buffer;
    currentLibraryRecordId = recordId;
    render(currentPatch);
    if (displayTitle) elements.patchName.textContent = displayTitle;
    elements.hero.hidden = true;
    elements.library.hidden = true;
    elements.browse.hidden = true;
    elements.banks.hidden = true;
    elements.error.hidden = true;
    elements.workspace.hidden = false;
    if (persist) {
      try {
        const record = makeLibraryRecord(currentPatch, buffer, fileName, lastModified);
        await savePatch(record);
        currentLibraryRecordId = record.id;
        await refreshLibrary();
      } catch (storageError) {
        console.warn("Patch opened, but could not be saved to the local library.", storageError);
      }
    }
    $("#edit-metadata-button").disabled = !currentLibraryRecordId;
    $("#versions-button").disabled = !currentLibraryRecordId;
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
  const extension = file.name.toLowerCase().split(".").pop();
  if (!isAllowedPatchFile(file.name)) {
    elements.hero.hidden = true;
    elements.error.hidden = false;
    elements.errorMessage.textContent = "Please choose a ZOIA .bin patch or a .zip archive.";
    return;
  }
  if (extension === "zip") {
    try {
      const count = await importZipBuffer(await file.arrayBuffer(), { lastModified: file.lastModified });
      showLibrary();
      elements.libraryStatus.textContent = `Imported ${count} patch${count === 1 ? "" : "es"} from ${file.name}`;
    } catch (error) {
      elements.hero.hidden = true; elements.error.hidden = false; elements.errorMessage.textContent = error.message;
    }
    return;
  }
  await inspectBuffer(await file.arrayBuffer(), file.name, { persist: true, lastModified: file.lastModified });
}

function isAllowedPatchFile(fileName) {
  const lower = fileName.toLowerCase();
  return lower.endsWith(".bin") || lower.endsWith(".zip");
}

async function saveBinToLibrary(buffer, fileName, { lastModified = 0, metadata = {} } = {}) {
  const patch = parsePatch(buffer, await getModuleIndex());
  await savePatch(makeLibraryRecord(patch, buffer, fileName, lastModified, metadata));
  return patch;
}

async function importZipBuffer(buffer, { lastModified = 0, metadata = {}, refresh = true } = {}) {
  const entries = await readZip(buffer, { extensions: [".bin"] });
  let imported = 0;
  const failures = [];
  for (const entry of entries) {
    try {
      await saveBinToLibrary(entry.data.buffer, entry.name, { lastModified, metadata });
      imported += 1;
    } catch (error) {
      failures.push(`${entry.name}: ${error.message}`);
    }
  }
  if (!imported) throw new Error(`No valid ZOIA binaries were found in the ZIP. ${failures.join(" ")}`);
  if (refresh) await refreshLibrary();
  return imported;
}

function makeLibraryRecord(patch, buffer, fileName, lastModified = 0, metadata = {}) {
  const now = new Date().toISOString();
  const details = {
    title: metadata.title || patch.name,
    content: metadata.content || "",
    author: typeof metadata.author === "string" ? metadata.author : metadata.author?.name || "",
    revision: String(metadata.revision || "1"),
    rating: Number(metadata.rating) || 0,
    categories: (metadata.categories || []).map((item) => typeof item === "string" ? item : item.name).filter(Boolean),
    tags: (metadata.tags || []).map((item) => typeof item === "string" ? item : item.name).filter(Boolean),
    link: metadata.link || metadata.url || "",
    created_at: metadata.created_at || now,
    updated_at: metadata.updated_at || now,
    remote_id: metadata.id || null
  };
  return {
    id: patchId(fileName, buffer.byteLength, lastModified),
    fileName,
    title: details.title,
    addedAt: Date.now(),
    lastModified,
    byteLength: buffer.byteLength,
    buffer,
    summary: { ...patch.meta },
    metadata: details
  };
}

async function refreshLibrary() {
  try {
    libraryRecords = await listPatches();
    $("#library-count").textContent = String(libraryRecords.length);
    renderLibrary();
  } catch (error) {
    libraryRecords = [];
    elements.libraryStatus.textContent = "Storage unavailable";
    elements.libraryEmpty.querySelector("strong").textContent = "Browser storage is unavailable";
    elements.libraryEmpty.querySelector("p").textContent = "Your browser may be blocking IndexedDB in this context.";
    elements.libraryEmpty.hidden = false;
  }
}

function renderLibrary() {
  const query = elements.librarySearch.value.trim().toLowerCase();
  const sort = elements.librarySort.value;
  const records = libraryRecords.filter((record) => `${record.title} ${record.fileName}`.toLowerCase().includes(query));
  records.sort((a, b) => {
    if (sort === "title-asc") return a.title.localeCompare(b.title);
    if (sort === "modules-desc") return b.summary.moduleCount - a.summary.moduleCount;
    if (sort === "cpu-desc") return b.summary.estimatedCpu - a.summary.estimatedCpu;
    return b.addedAt - a.addedAt;
  });
  elements.libraryStatus.textContent = `${records.length} patch${records.length === 1 ? "" : "es"}`;
  elements.libraryEmpty.hidden = libraryRecords.length > 0;
  elements.libraryList.replaceChildren(...records.map((record) => {
    const row = document.createElement("article");
    row.className = "library-row";
    row.innerHTML = `
      <button class="library-title" type="button"><span class="library-patch-icon"><i></i><i></i><i></i><i></i></span><span><strong></strong><small></small></span></button>
      <span class="library-stat"></span><span class="library-stat"></span><span class="library-stat"></span><span class="library-date"></span>
      <span class="library-actions"><button type="button" data-action="edit" title="Edit patch details">✎</button><button type="button" data-action="export" title="Download original binary">↓</button><button type="button" data-action="remove" title="Remove from library">×</button></span>`;
    row.querySelector(".library-title strong").textContent = record.title;
    row.querySelector(".library-title small").textContent = record.fileName;
    const stats = row.querySelectorAll(".library-stat");
    stats[0].textContent = record.summary.moduleCount;
    stats[1].textContent = record.summary.pageCount;
    stats[2].textContent = `${record.summary.estimatedCpu}%`;
    row.querySelector(".library-date").textContent = new Intl.DateTimeFormat(undefined, { month: "short", day: "numeric", year: "numeric" }).format(record.addedAt);
    row.querySelector(".library-title").addEventListener("click", () => openLibraryPatch(record.id));
    row.querySelector('[data-action="edit"]').addEventListener("click", () => openMetadataEditor(record));
    row.querySelector('[data-action="export"]').addEventListener("click", () => downloadBinary(record));
    row.querySelector('[data-action="remove"]').addEventListener("click", () => deleteLibraryPatch(record));
    return row;
  }));
  if (libraryRecords.length && !records.length) {
    const noResults = document.createElement("p");
    noResults.className = "library-no-results";
    noResults.textContent = "No patches match that search.";
    elements.libraryList.append(noResults);
  }
}

async function openLibraryPatch(id) {
  const record = await getPatch(id);
  if (record) await inspectBuffer(record.buffer, record.fileName, { recordId: record.id, displayTitle: record.title });
}

function downloadBinary(record) {
  const link = document.createElement("a");
  link.href = URL.createObjectURL(new Blob([record.buffer], { type: "application/octet-stream" }));
  link.download = record.fileName;
  link.click();
  URL.revokeObjectURL(link.href);
}

async function deleteLibraryPatch(record) {
  if (!window.confirm(`Remove “${record.title}” from this browser library? The original file on your device will not be affected.`)) return;
  const revisions = await listRevisions(record.id);
  await Promise.all(revisions.map((revision) => removeRevision(revision.id)));
  await removePatch(record.id);
  await refreshLibrary();
}

function metadataFor(record) {
  const now = new Date().toISOString();
  return record.metadata || {
    title: record.title, content: "", author: "", revision: "1", rating: 0,
    categories: [], tags: [], link: "", created_at: now, updated_at: now, remote_id: null
  };
}

function openMetadataEditor(record) {
  metadataRecord = record;
  const metadata = metadataFor(record);
  $("#metadata-binary-name").textContent = `Binary: ${record.fileName}`;
  $("#metadata-title").value = metadata.title || record.title;
  $("#metadata-author").value = typeof metadata.author === "string" ? metadata.author : metadata.author?.name || "";
  $("#metadata-revision").value = metadata.revision || "";
  $("#metadata-source").value = metadata.link || "";
  $("#metadata-categories").value = (metadata.categories || []).map((item) => typeof item === "string" ? item : item.name).join(", ");
  $("#metadata-tags").value = (metadata.tags || []).map((item) => typeof item === "string" ? item : item.name).join(", ");
  $("#metadata-notes").value = metadata.content || "";
  metadataRating = Math.max(0, Math.min(5, Number(metadata.rating) || 0));
  renderRating();
  $("#metadata-save-status").textContent = "Stored only in this browser";
  if (!elements.metadataDialog.open) elements.metadataDialog.showModal();
}

function renderRating() {
  $("#metadata-rating").replaceChildren(...Array.from({ length: 5 }, (_, index) => {
    const value = index + 1;
    const button = document.createElement("button");
    button.type = "button";
    button.className = value <= metadataRating ? "active" : "";
    button.textContent = "★";
    button.setAttribute("aria-label", `${value} star${value === 1 ? "" : "s"}`);
    button.addEventListener("click", () => { metadataRating = metadataRating === value ? 0 : value; renderRating(); });
    return button;
  }));
}

function splitMetadataList(value) {
  return [...new Set(value.split(",").map((item) => item.trim()).filter(Boolean))];
}

function collectMetadata() {
  const previous = metadataFor(metadataRecord);
  return {
    ...previous,
    title: $("#metadata-title").value.trim(),
    author: $("#metadata-author").value.trim(),
    revision: $("#metadata-revision").value.trim(),
    rating: metadataRating,
    link: $("#metadata-source").value.trim(),
    categories: splitMetadataList($("#metadata-categories").value),
    tags: splitMetadataList($("#metadata-tags").value),
    content: $("#metadata-notes").value,
    updated_at: new Date().toISOString()
  };
}

function sidecarJson(record, metadata = metadataFor(record)) {
  return {
    id: metadata.remote_id || 0,
    link: metadata.link || "",
    created_at: metadata.created_at,
    updated_at: metadata.updated_at,
    title: metadata.title,
    content: metadata.content,
    revision: metadata.revision,
    rating: metadata.rating,
    author: { name: metadata.author || "" },
    categories: metadata.categories.map((name) => ({ name })),
    tags: metadata.tags.map((name) => ({ name })),
    files: [{ id: 0, filesize: record.byteLength, filename: record.fileName }]
  };
}

function downloadJson(data, fileName) {
  const link = document.createElement("a");
  link.href = URL.createObjectURL(new Blob([JSON.stringify(data, null, 2)], { type: "application/json" }));
  link.download = fileName;
  link.click(); URL.revokeObjectURL(link.href);
}

async function saveMetadata(event) {
  event.preventDefault();
  if (!metadataRecord) return;
  const metadata = collectMetadata();
  if (!metadata.title) return;
  metadataRecord = { ...metadataRecord, title: metadata.title, metadata };
  await savePatch(metadataRecord);
  if (currentLibraryRecordId === metadataRecord.id) elements.patchName.textContent = metadata.title;
  $("#metadata-save-status").textContent = "Saved ✓";
  await refreshLibrary();
  setTimeout(() => elements.metadataDialog.close(), 350);
}

async function importMetadataFile(file) {
  if (!file || !metadataRecord) return;
  try {
    const data = JSON.parse(await file.text());
    if (!data || typeof data !== "object") throw new Error("Expected a JSON object.");
    const merged = { ...metadataFor(metadataRecord), ...data };
    merged.author = typeof data.author === "string" ? data.author : data.author?.name || "";
    merged.categories = (data.categories || []).map((item) => typeof item === "string" ? item : item.name).filter(Boolean);
    merged.tags = (data.tags || []).map((item) => typeof item === "string" ? item : item.name).filter(Boolean);
    merged.remote_id = data.remote_id || data.id || null;
    metadataRecord = { ...metadataRecord, metadata: merged };
    openMetadataEditor(metadataRecord);
    $("#metadata-save-status").textContent = "Imported—review and save";
  } catch (error) {
    $("#metadata-save-status").textContent = `Import failed: ${error.message}`;
  } finally {
    $("#metadata-import-input").value = "";
  }
}

async function bufferHash(buffer) {
  const digest = await crypto.subtle.digest("SHA-256", buffer);
  return [...new Uint8Array(digest)].map((byte) => byte.toString(16).padStart(2, "0")).join("");
}

function compactAnalysis(patch) {
  return {
    name: patch.name,
    meta: { ...patch.meta },
    pages: patch.pages.map((page) => ({ ...page })),
    modules: patch.modules.map((module) => ({
      number: module.number, typeId: module.typeId, displayName: module.displayName,
      type: module.type, page: module.page, position: module.position, version: module.version,
      parameters: module.parameters.map((parameter) => parameter.raw)
    })),
    connections: patch.connections.map((connection) => ({
      sourceModule: connection.sourceModule, sourceBlock: connection.sourceBlock,
      destinationModule: connection.destinationModule, destinationBlock: connection.destinationBlock,
      strengthRaw: connection.strengthRaw
    }))
  };
}

async function openVersionHistory(recordId = currentLibraryRecordId) {
  if (!recordId) return;
  versionPatchRecord = await getPatch(recordId);
  if (!versionPatchRecord) return;
  $("#versions-patch-name").textContent = `${versionPatchRecord.title} · ${versionPatchRecord.fileName}`;
  selectedRevisionIds = new Set();
  $("#comparison-results").hidden = true;
  $("#comparison-empty").hidden = false;
  await refreshRevisions();
  elements.versionsDialog.showModal();
}

async function refreshRevisions() {
  revisionRecords = (await listRevisions(versionPatchRecord.id)).sort((a, b) => b.createdAt - a.createdAt);
  $("#versions-count").textContent = `${revisionRecords.length} snapshot${revisionRecords.length === 1 ? "" : "s"}`;
  $("#compare-versions").disabled = selectedRevisionIds.size !== 2;
  const timeline = $("#revision-timeline");
  timeline.replaceChildren(...revisionRecords.map((revision) => {
    const item = document.createElement("article");
    item.className = `revision-item${selectedRevisionIds.has(revision.id) ? " selected" : ""}`;
    item.innerHTML = `
      <label class="revision-select"><input type="checkbox"><i></i></label>
      <div class="revision-copy"><strong></strong><time></time><p></p><div class="revision-metrics"></div></div>
      <div class="revision-actions"><button type="button" data-action="binary" title="Export binary">.bin</button><button type="button" data-action="json" title="Export metadata">.json</button><button type="button" data-action="restore">Restore</button><button type="button" data-action="delete" title="Delete snapshot">×</button></div>`;
    const checkbox = item.querySelector("input"); checkbox.checked = selectedRevisionIds.has(revision.id);
    item.querySelector("strong").textContent = revision.label;
    item.querySelector("time").textContent = new Intl.DateTimeFormat(undefined, { dateStyle: "medium", timeStyle: "short" }).format(revision.createdAt);
    item.querySelector("p").textContent = revision.note || "No snapshot note.";
    item.querySelector(".revision-metrics").textContent = `${revision.analysis.meta.moduleCount} modules · ${revision.analysis.meta.connectionCount} routes · ${revision.analysis.meta.estimatedCpu}% CPU`;
    checkbox.addEventListener("change", () => toggleRevisionSelection(revision.id, checkbox.checked));
    item.querySelector('[data-action="binary"]').addEventListener("click", () => downloadRevisionBinary(revision));
    item.querySelector('[data-action="json"]').addEventListener("click", () => downloadJson(sidecarJson(versionPatchRecord, revision.metadata), `${versionPatchRecord.fileName.replace(/\.bin$/i, "")}_${safeBankName(revision.label)}.json`));
    item.querySelector('[data-action="restore"]').addEventListener("click", () => restoreRevision(revision));
    item.querySelector('[data-action="delete"]').addEventListener("click", () => deleteRevision(revision));
    return item;
  }));
  if (!revisionRecords.length) {
    const empty = document.createElement("div"); empty.className = "revision-empty";
    empty.innerHTML = "<strong>No snapshots yet</strong><p>Save the current binary above to begin its history.</p>";
    timeline.append(empty);
  }
}

function toggleRevisionSelection(id, checked) {
  if (checked && selectedRevisionIds.size >= 2) return refreshRevisions();
  if (checked) selectedRevisionIds.add(id); else selectedRevisionIds.delete(id);
  refreshRevisions();
}

async function createSnapshot(event) {
  event.preventDefault();
  if (!versionPatchRecord) return;
  const hash = await bufferHash(versionPatchRecord.buffer);
  const revision = {
    id: `${versionPatchRecord.id}::${hash}`,
    patchId: versionPatchRecord.id,
    hash,
    label: $("#snapshot-label").value.trim(),
    note: $("#snapshot-note").value.trim(),
    createdAt: Date.now(),
    buffer: versionPatchRecord.buffer,
    metadata: structuredClone(metadataFor(versionPatchRecord)),
    analysis: compactAnalysis(parsePatch(versionPatchRecord.buffer, await getModuleIndex()))
  };
  if (revisionRecords.some((existing) => existing.hash === hash)) {
    $("#versions-status").textContent = "That binary is already in this patch’s history.";
    return;
  }
  try {
    await saveRevision(revision);
    $("#snapshot-form").reset();
    $("#versions-status").textContent = `Saved “${revision.label}” ✓`;
    await refreshRevisions();
  } catch (error) {
    $("#versions-status").textContent = error.name === "ConstraintError" ? "That binary is already in this patch’s history." : `Snapshot failed: ${error.message}`;
  }
}

function downloadRevisionBinary(revision) {
  const link = document.createElement("a");
  link.href = URL.createObjectURL(new Blob([revision.buffer], { type: "application/octet-stream" }));
  link.download = versionPatchRecord.fileName.replace(/\.bin$/i, `_${safeBankName(revision.label)}.bin`);
  link.click(); URL.revokeObjectURL(link.href);
}

async function restoreRevision(revision) {
  if (!window.confirm(`Restore “${revision.label}” as the current binary? The existing snapshots will remain available.`)) return;
  const parsed = parsePatch(revision.buffer, await getModuleIndex());
  versionPatchRecord = {
    ...versionPatchRecord,
    buffer: revision.buffer,
    byteLength: revision.buffer.byteLength,
    summary: { ...parsed.meta },
    metadata: structuredClone(revision.metadata),
    title: revision.metadata.title || versionPatchRecord.title
  };
  await savePatch(versionPatchRecord);
  await refreshLibrary();
  if (currentLibraryRecordId === versionPatchRecord.id) await inspectBuffer(revision.buffer, versionPatchRecord.fileName, { recordId: versionPatchRecord.id, displayTitle: versionPatchRecord.title });
  $("#versions-status").textContent = `Restored “${revision.label}” ✓`;
}

async function deleteRevision(revision) {
  if (!window.confirm(`Delete snapshot “${revision.label}”? This cannot be undone.`)) return;
  await removeRevision(revision.id); selectedRevisionIds.delete(revision.id); await refreshRevisions();
  $("#versions-status").textContent = "Snapshot deleted.";
}

function connectionKey(connection) {
  return `${connection.sourceModule}.${connection.sourceBlock}>${connection.destinationModule}.${connection.destinationBlock}@${connection.strengthRaw}`;
}

function compareSelectedRevisions() {
  const selected = revisionRecords.filter((revision) => selectedRevisionIds.has(revision.id)).sort((a, b) => a.createdAt - b.createdAt);
  if (selected.length !== 2) return;
  const [from, to] = selected;
  const before = new Map(from.analysis.modules.map((module) => [module.number, module]));
  const after = new Map(to.analysis.modules.map((module) => [module.number, module]));
  const added = [...after.keys()].filter((number) => !before.has(number)).map((number) => after.get(number));
  const removed = [...before.keys()].filter((number) => !after.has(number)).map((number) => before.get(number));
  const changed = [...after.keys()].filter((number) => {
    if (!before.has(number)) return false;
    const a = before.get(number); const b = after.get(number);
    return a.typeId !== b.typeId || a.page !== b.page || a.position !== b.position || a.version !== b.version || JSON.stringify(a.parameters) !== JSON.stringify(b.parameters);
  }).map((number) => ({ before: before.get(number), after: after.get(number) }));
  const fromRoutes = new Set(from.analysis.connections.map(connectionKey));
  const toRoutes = new Set(to.analysis.connections.map(connectionKey));
  const routesAdded = [...toRoutes].filter((route) => !fromRoutes.has(route)).length;
  const routesRemoved = [...fromRoutes].filter((route) => !toRoutes.has(route)).length;
  $("#comparison-from").textContent = from.label; $("#comparison-to").textContent = to.label;
  const summary = [
    [to.analysis.meta.moduleCount - from.analysis.meta.moduleCount, "Modules"],
    [to.analysis.meta.connectionCount - from.analysis.meta.connectionCount, "Routes"],
    [Math.round((to.analysis.meta.estimatedCpu - from.analysis.meta.estimatedCpu) * 100) / 100, "CPU"],
    [to.analysis.meta.pageCount - from.analysis.meta.pageCount, "Pages"]
  ];
  $("#comparison-summary").replaceChildren(...summary.map(([delta, label]) => {
    const item = document.createElement("span"); item.className = delta > 0 ? "positive" : delta < 0 ? "negative" : "";
    item.innerHTML = `<strong></strong><small></small>`; item.querySelector("strong").textContent = `${delta > 0 ? "+" : ""}${delta}${label === "CPU" ? "%" : ""}`; item.querySelector("small").textContent = label; return item;
  }));
  const groups = [
    ["Added modules", added.map((module) => module.displayName)],
    ["Removed modules", removed.map((module) => module.displayName)],
    ["Changed modules", changed.map(({ after: module }) => module.displayName)],
    ["Routing", [`${routesAdded} added`, `${routesRemoved} removed`]]
  ];
  $("#comparison-changes").replaceChildren(...groups.map(([title, items]) => {
    const group = document.createElement("section"); group.innerHTML = `<h4></h4><div></div>`; group.querySelector("h4").textContent = title;
    group.querySelector("div").replaceChildren(...(items.length ? items : ["None"]).map((value) => { const item = document.createElement("span"); item.textContent = value; return item; })); return group;
  }));
  $("#comparison-empty").hidden = true; $("#comparison-results").hidden = false;
}

async function refreshBanks() {
  try {
    bankRecords = (await listBanks()).sort((a, b) => b.updatedAt - a.updatedAt);
    $("#bank-count").textContent = String(bankRecords.length);
    if (activeBank) activeBank = bankRecords.find((bank) => bank.id === activeBank.id);
    renderBankList();
    renderActiveBank();
  } catch (error) {
    $("#bank-save-status").textContent = "Bank storage unavailable";
  }
}

async function showBanks() {
  elements.hero.hidden = true;
  elements.library.hidden = true;
  elements.browse.hidden = true;
  elements.workspace.hidden = true;
  elements.error.hidden = true;
  elements.banks.hidden = false;
  await refreshLibrary();
  await refreshBanks();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

async function createBank() {
  const name = window.prompt("Name this ZOIA bank:", `Bank ${bankRecords.length + 1}`)?.trim();
  if (!name) return;
  const now = Date.now();
  activeBank = { id: crypto.randomUUID(), name, createdAt: now, updatedAt: now, slots: Array(64).fill(null) };
  await saveBank(activeBank);
  await refreshBanks();
}

function renderBankList() {
  elements.bankList.replaceChildren(...bankRecords.map((bank) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `bank-list-item${activeBank?.id === bank.id ? " active" : ""}`;
    const filled = bank.slots.filter(Boolean).length;
    button.innerHTML = `<span class="bank-mini-grid"></span><span><strong></strong><small></small></span>`;
    button.querySelector("strong").textContent = bank.name;
    button.querySelector("small").textContent = `${filled} of 64 slots`;
    button.querySelector(".bank-mini-grid").replaceChildren(...Array.from({ length: 4 }, (_, index) => {
      const dot = document.createElement("i");
      dot.classList.toggle("filled", index < Math.ceil(filled / 16));
      return dot;
    }));
    button.addEventListener("click", () => { activeBank = bank; selectedBankPatchId = undefined; renderBankList(); renderActiveBank(); });
    return button;
  }));
}

function renderActiveBank() {
  const hasBank = Boolean(activeBank);
  $("#bank-empty").hidden = hasBank;
  $("#bank-content").hidden = !hasBank;
  if (!hasBank) return;
  $("#bank-name").value = activeBank.name;
  renderBankSlots();
  renderBankPalette();
  renderBankHealth();
}

function renderBankSlots() {
  const patches = new Map(libraryRecords.map((record) => [record.id, record]));
  const duplicateIds = new Set(activeBank.slots.filter((id, index, slots) => id && slots.indexOf(id) !== index));
  elements.bankSlots.replaceChildren(...activeBank.slots.map((patchRecordId, index) => {
    const record = patches.get(patchRecordId);
    const row = document.createElement("div");
    row.className = `bank-slot${record ? " filled" : ""}${patchRecordId && !record ? " missing" : ""}${duplicateIds.has(patchRecordId) ? " duplicate" : ""}`;
    row.dataset.slot = String(index);
    row.innerHTML = `<span class="slot-number"></span><button class="slot-patch" type="button"><strong></strong><small></small></button><span class="slot-state"></span><button class="slot-clear" type="button" aria-label="Clear slot">×</button>`;
    row.querySelector(".slot-number").textContent = String(index).padStart(3, "0");
    row.querySelector(".slot-patch strong").textContent = record?.title || (patchRecordId ? "Missing library patch" : "Empty slot");
    row.querySelector(".slot-patch small").textContent = record ? bankFileName(index, record) : "Drop or select a patch";
    row.querySelector(".slot-state").textContent = duplicateIds.has(patchRecordId) ? "Duplicate" : record ? "Ready" : patchRecordId ? "Missing" : "Empty";
    row.querySelector(".slot-clear").hidden = !patchRecordId;
    row.querySelector(".slot-clear").addEventListener("click", () => assignBankSlot(index, null));
    row.querySelector(".slot-patch").addEventListener("click", () => {
      if (selectedBankPatchId) assignBankSlot(index, selectedBankPatchId);
      else if (record) inspectBuffer(record.buffer, record.fileName);
    });
    if (record) {
      row.draggable = true;
      row.addEventListener("dragstart", (event) => event.dataTransfer.setData("application/x-zoia-slot", String(index)));
    }
    row.addEventListener("dragover", (event) => { event.preventDefault(); row.classList.add("drag-over"); });
    row.addEventListener("dragleave", () => row.classList.remove("drag-over"));
    row.addEventListener("drop", (event) => {
      event.preventDefault(); row.classList.remove("drag-over");
      const sourceSlot = event.dataTransfer.getData("application/x-zoia-slot");
      const patchIdValue = event.dataTransfer.getData("application/x-zoia-patch");
      if (sourceSlot !== "") moveBankSlot(Number(sourceSlot), index);
      else if (patchIdValue) assignBankSlot(index, patchIdValue);
    });
    return row;
  }));
}

function renderBankPalette() {
  const query = $("#bank-patch-search").value.trim().toLowerCase();
  const matches = libraryRecords.filter((record) => `${record.title} ${record.fileName}`.toLowerCase().includes(query));
  elements.bankPatchList.replaceChildren(...matches.map((record) => {
    const button = document.createElement("button");
    button.type = "button";
    button.draggable = true;
    button.className = `bank-patch${selectedBankPatchId === record.id ? " selected" : ""}`;
    button.innerHTML = `<span class="library-patch-icon"><i></i><i></i><i></i><i></i></span><span><strong></strong><small></small></span>`;
    button.querySelector("strong").textContent = record.title;
    button.querySelector("small").textContent = `${record.summary.moduleCount} modules · ${record.summary.estimatedCpu}% CPU`;
    button.addEventListener("click", () => {
      selectedBankPatchId = selectedBankPatchId === record.id ? undefined : record.id;
      $("#selected-bank-patch").textContent = selectedBankPatchId ? `${record.title} selected` : "No patch selected";
      renderBankPalette();
    });
    button.addEventListener("dragstart", (event) => event.dataTransfer.setData("application/x-zoia-patch", record.id));
    return button;
  }));
  if (!matches.length) {
    const empty = document.createElement("p"); empty.className = "palette-empty";
    empty.textContent = libraryRecords.length ? "No matching patches." : "Import patches into your local library first.";
    elements.bankPatchList.append(empty);
  }
}

async function persistActiveBank(message = "Saved locally") {
  if (!activeBank) return;
  activeBank.updatedAt = Date.now();
  await saveBank(activeBank);
  $("#bank-save-status").textContent = message;
  bankRecords = (await listBanks()).sort((a, b) => b.updatedAt - a.updatedAt);
  renderBankList();
}

async function assignBankSlot(index, patchRecordId) {
  activeBank.slots[index] = patchRecordId;
  renderBankSlots(); renderBankHealth();
  await persistActiveBank(`Slot ${String(index).padStart(3, "0")} saved`);
}

async function moveBankSlot(source, destination) {
  if (source === destination) return;
  [activeBank.slots[source], activeBank.slots[destination]] = [activeBank.slots[destination], activeBank.slots[source]];
  renderBankSlots(); renderBankHealth();
  await persistActiveBank(`Moved slot ${String(source).padStart(3, "0")} → ${String(destination).padStart(3, "0")}`);
}

function renderBankHealth() {
  const filled = activeBank.slots.filter(Boolean);
  const duplicates = filled.length - new Set(filled).size;
  const missing = filled.filter((id) => !libraryRecords.some((record) => record.id === id)).length;
  $("#bank-health").innerHTML = `<span class="health-ready"><b>${filled.length}</b> ready</span><span><b>${64 - filled.length}</b> empty</span><span class="${duplicates ? "health-warning" : ""}"><b>${duplicates}</b> duplicates</span><span class="${missing ? "health-error" : ""}"><b>${missing}</b> missing</span>`;
}

function safeBankName(value) {
  return value.normalize("NFKD").replace(/[^a-zA-Z0-9 _-]/g, "").trim().replace(/\s+/g, "_").slice(0, 32) || "zoia_bank";
}

function bankFileName(slot, record) {
  const title = safeBankName(record.title).toLowerCase().slice(0, 20);
  return `${String(slot).padStart(3, "0")}_zoia_${title}.bin`;
}

function bankFiles() {
  const patches = new Map(libraryRecords.map((record) => [record.id, record]));
  return activeBank.slots.flatMap((id, slot) => {
    const record = patches.get(id);
    return record ? [{ name: bankFileName(slot, record), data: new Uint8Array(record.buffer) }] : [];
  });
}

async function importBankZip(file) {
  if (!file?.name.toLowerCase().endsWith(".zip")) throw new Error("Choose a .zip bank archive.");
  const entries = await readZip(await file.arrayBuffer(), { extensions: [".bin"] });
  const name = file.name.replace(/\.zip$/i, "").replace(/[_-]+/g, " ").trim();
  await importBankEntries(entries, name, file.lastModified, "ZIP");
}

async function importBankFolder(files) {
  const bins = [...files].filter((file) => file.name.toLowerCase().endsWith(".bin"));
  if (!bins.length) throw new Error("The selected folder does not contain any .bin patches.");
  const entries = await Promise.all(bins.map(async (file) => ({ name: file.name, data: new Uint8Array(await file.arrayBuffer()) })));
  const relativePath = bins[0].webkitRelativePath || "";
  const name = relativePath.split("/")[0].replace(/[_-]+/g, " ").trim();
  await importBankEntries(entries, name, Math.max(...bins.map((file) => file.lastModified || 0)), "folder");
}

async function importBankEntries(entries, bankName, lastModified, sourceLabel) {
  const catalog = await getModuleIndex();
  const slots = Array(64).fill(null);
  const failures = [];
  let imported = 0;

  for (const entry of entries) {
    const match = entry.name.match(/^(\d{3})_/);
    const slot = match ? Number(match[1]) : -1;
    if (slot < 0 || slot > 63) { failures.push(`${entry.name}: no 000–063 slot prefix`); continue; }
    if (slots[slot]) { failures.push(`${entry.name}: slot ${match[1]} is already filled`); continue; }
    try {
      const buffer = entry.data.buffer.slice(entry.data.byteOffset, entry.data.byteOffset + entry.data.byteLength);
      const patch = parsePatch(buffer, catalog);
      const record = makeLibraryRecord(patch, buffer, entry.name, lastModified);
      await savePatch(record);
      slots[slot] = record.id;
      imported += 1;
    } catch (error) {
      failures.push(`${entry.name}: ${error.message}`);
    }
  }

  if (!imported) throw new Error("No valid numbered ZOIA patches were found. Bank filenames must begin with slots 000 through 063.");
  const now = Date.now();
  const name = bankName || `Imported bank ${bankRecords.length + 1}`;
  activeBank = { id: crypto.randomUUID(), name, createdAt: now, updatedAt: now, slots };
  await saveBank(activeBank);
  await refreshLibrary();
  await refreshBanks();
  $("#bank-save-status").textContent = failures.length
    ? `Imported ${imported} patches · skipped ${failures.length}`
    : `Imported ${imported} patches from ${sourceLabel}`;
}

function exportBankZip() {
  const files = bankFiles();
  if (!files.length) { window.alert("Add at least one patch before exporting this bank."); return; }
  const link = document.createElement("a");
  link.href = URL.createObjectURL(createZip(files));
  link.download = `${safeBankName(activeBank.name)}.zip`;
  link.click(); URL.revokeObjectURL(link.href);
  $("#bank-save-status").textContent = `Exported ${files.length} patches as ZIP`;
}

async function exportBankFolder() {
  if (!("showDirectoryPicker" in window)) { window.alert("Direct folder export is not supported in this browser. Use Export ZIP instead."); return; }
  const files = bankFiles();
  if (!files.length) { window.alert("Add at least one patch before exporting this bank."); return; }
  try {
    const root = await window.showDirectoryPicker({ mode: "readwrite" });
    const folder = await root.getDirectoryHandle(safeBankName(activeBank.name), { create: true });
    for (const file of files) {
      const handle = await folder.getFileHandle(file.name, { create: true });
      const writable = await handle.createWritable(); await writable.write(file.data); await writable.close();
    }
    $("#bank-save-status").textContent = `Wrote ${files.length} patches to folder`;
  } catch (error) {
    if (error.name !== "AbortError") $("#bank-save-status").textContent = `Folder export failed: ${error.message}`;
  }
}

function showLibrary() {
  elements.hero.hidden = true;
  elements.browse.hidden = true;
  elements.banks.hidden = true;
  elements.workspace.hidden = true;
  elements.error.hidden = true;
  elements.library.hidden = false;
  refreshLibrary();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function showBrowse() {
  elements.hero.hidden = true;
  elements.library.hidden = true;
  elements.banks.hidden = true;
  elements.workspace.hidden = true;
  elements.error.hidden = true;
  elements.browse.hidden = false;
  if (!elements.patchGrid.children.length) loadBrowseResults();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

async function loadBrowseResults() {
  elements.browseMessage.hidden = false;
  elements.browseMessage.className = "browse-message loading";
  elements.browseMessage.textContent = "Loading community patches…";
  elements.patchGrid.setAttribute("aria-busy", "true");
  try {
    const result = await browsePatches({ page: browsePage, search: browseQuery });
    browseTotalPages = result.totalPages;
    $("#browse-result-count").textContent = `${result.total.toLocaleString()} result${result.total === 1 ? "" : "s"}`;
    $("#browse-page-label").textContent = `Page ${browsePage} of ${browseTotalPages}`;
    $("#browse-previous").disabled = browsePage <= 1;
    $("#browse-next").disabled = browsePage >= browseTotalPages;
    elements.patchGrid.replaceChildren(...result.patches.map(renderCommunityCard));
    elements.browseMessage.hidden = result.patches.length > 0;
    if (!result.patches.length) {
      elements.browseMessage.className = "browse-message";
      elements.browseMessage.textContent = "No patches matched that search.";
    }
  } catch (error) {
    elements.patchGrid.replaceChildren();
    elements.browseMessage.hidden = false;
    elements.browseMessage.className = "browse-message error";
    elements.browseMessage.textContent = `PatchStorage could not be reached. ${error.message}`;
  } finally {
    elements.patchGrid.removeAttribute("aria-busy");
  }
}

function renderCommunityCard(patch) {
  const card = document.createElement("article");
  card.className = "community-card";
  card.innerHTML = `
    <button class="community-art" type="button" aria-label="View patch details"></button>
    <div class="community-body">
      <div class="community-category"></div>
      <button class="community-title" type="button"></button>
      <p class="community-author"></p>
      <p class="community-excerpt"></p>
      <div class="community-footer"><span></span><span></span><span></span></div>
    </div>`;
  const art = card.querySelector(".community-art");
  if (patch.artwork?.thumbnail_url) {
    const image = document.createElement("img");
    image.src = patch.artwork.thumbnail_url;
    image.alt = "";
    image.loading = "lazy";
    art.append(image);
  } else {
    art.classList.add("art-placeholder");
    art.textContent = "ZOIA";
  }
  card.querySelector(".community-category").textContent = patch.categories?.[0]?.name || "Patch";
  card.querySelector(".community-title").textContent = patch.title;
  card.querySelector(".community-author").textContent = `by ${patch.author?.name || "Unknown"}`;
  card.querySelector(".community-excerpt").textContent = patch.excerpt || "No description provided.";
  const stats = card.querySelectorAll(".community-footer span");
  stats[0].textContent = `↓ ${Number(patch.download_count || 0).toLocaleString()}`;
  stats[1].textContent = `♡ ${Number(patch.like_count || 0).toLocaleString()}`;
  stats[2].textContent = `v${patch.revision || "—"}`;
  [art, card.querySelector(".community-title")].forEach((button) => button.addEventListener("click", () => openCommunityPatch(patch.id)));
  return card;
}

async function openCommunityPatch(id) {
  selectedCommunityPatch = undefined;
  $("#download-status").textContent = "Loading patch details…";
  $("#patch-dialog-title").textContent = "Loading…";
  $("#patch-dialog-save").disabled = true;
  elements.patchDialog.showModal();
  try {
    const patch = await getPatchDetails(id);
    selectedCommunityPatch = patch;
    $("#patch-dialog-title").textContent = patch.title;
    $("#patch-dialog-category").textContent = patch.categories?.[0]?.name || "Community patch";
    $("#patch-dialog-byline").textContent = `by ${patch.author?.name || "Unknown"} · Revision ${patch.revision || "—"}`;
    $("#patch-dialog-content").textContent = patch.content || patch.excerpt || "No description provided.";
    $("#patch-dialog-external").href = patch.url;
    $("#patch-dialog-stats").replaceChildren(...[
      [`${Number(patch.download_count || 0).toLocaleString()}`, "Downloads"],
      [`${Number(patch.like_count || 0).toLocaleString()}`, "Likes"],
      [`${Number(patch.view_count || 0).toLocaleString()}`, "Views"]
    ].map(([value, label]) => {
      const item = document.createElement("span"); item.innerHTML = `<strong></strong><small></small>`;
      item.querySelector("strong").textContent = value; item.querySelector("small").textContent = label;
      return item;
    }));
    $("#patch-dialog-tags").replaceChildren(...(patch.tags || []).slice(0, 10).map((tag) => {
      const item = document.createElement("span"); item.textContent = tag.name; return item;
    }));
    const art = $("#patch-dialog-art");
    art.replaceChildren();
    if (patch.artwork?.url) {
      const image = document.createElement("img"); image.src = patch.artwork.url; image.alt = ""; art.append(image);
    } else {
      art.textContent = "ZOIA"; art.classList.add("art-placeholder");
    }
    $("#patch-dialog-save").disabled = false;
    $("#download-status").textContent = "";
  } catch (error) {
    $("#download-status").textContent = `Could not load details. ${error.message}`;
  }
}

async function saveCommunityPatch() {
  if (!selectedCommunityPatch) return;
  const button = $("#patch-dialog-save");
  const file = selectedCommunityPatch.files?.find((candidate) => isAllowedPatchFile(candidate.filename || ""));
  if (!file) {
    $("#download-status").textContent = "This upload does not include a compatible .bin or .zip file.";
    return;
  }
  button.disabled = true;
  button.textContent = "Downloading…";
  try {
    const buffer = await downloadPatchFile(file.url);
    const modified = Date.parse(selectedCommunityPatch.updated_at) || 0;
    let count = 1;
    let patch;
    if (file.filename.toLowerCase().endsWith(".zip")) {
      count = await importZipBuffer(buffer, { lastModified: modified, metadata: selectedCommunityPatch });
    } else {
      patch = await saveBinToLibrary(buffer, file.filename, { lastModified: modified, metadata: selectedCommunityPatch });
      await refreshLibrary();
    }
    button.textContent = "Saved to library ✓";
    $("#download-status").textContent = file.filename.toLowerCase().endsWith(".zip") ? `${count} patches from the ZIP are ready in your local library.` : `${patch.name} is ready in your local library.`;
  } catch (error) {
    button.disabled = false;
    button.textContent = "Try again";
    $("#download-status").textContent = `The patch could not be saved. ${error.message}`;
  }
}

async function importLibraryFiles(files) {
  const validFiles = [...files].filter((file) => isAllowedPatchFile(file.name));
  if (!validFiles.length) return;
  elements.libraryStatus.textContent = `Importing 0 of ${validFiles.length}…`;
  const catalog = await getModuleIndex();
  let imported = 0;
  let processed = 0;
  for (const file of validFiles) {
    try {
      const buffer = await file.arrayBuffer();
      if (file.name.toLowerCase().endsWith(".zip")) imported += await importZipBuffer(buffer, { lastModified: file.lastModified, refresh: false });
      else {
        const patch = parsePatch(buffer, catalog);
        await savePatch(makeLibraryRecord(patch, buffer, file.name, file.lastModified));
        imported += 1;
      }
    } catch (error) {
      console.warn(`Could not import ${file.name}`, error);
    }
    processed += 1;
    elements.libraryStatus.textContent = `Processing ${processed} of ${validFiles.length}…`;
  }
  elements.libraryInput.value = "";
  await refreshLibrary();
  elements.libraryStatus.textContent = `Imported ${imported} patch${imported === 1 ? "" : "es"}.`;
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
  renderInspector(patch);
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
    card.innerHTML = `<span class="graph-index"></span><strong></strong><small></small><span class="footprint" aria-label="Default module footprint"></span>`;
    card.querySelector(".graph-index").textContent = String(module.number + 1).padStart(2, "0");
    card.querySelector("strong").textContent = module.displayName;
    card.querySelector("small").textContent = module.category;
    card.querySelector(".footprint").replaceChildren(...Array.from({ length: Math.min(8, module.footprint) }, () => document.createElement("i")));
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
    path.tabIndex = 0;
    path.setAttribute("role", "button");
    const title = document.createElementNS(namespace, "title");
    title.textContent = `${patch.modules[connection.sourceModule]?.displayName || "Module"} → ${patch.modules[connection.destinationModule]?.displayName || "Module"} · ${connection.strength}%`;
    path.append(title);
    path.addEventListener("click", () => selectRoute(path, connection));
    path.addEventListener("keydown", (event) => { if (event.key === "Enter" || event.key === " ") selectRoute(path, connection); });
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

function renderInspector(patch) {
  const metadata = [
    ["File size", `${(patch.byteLength / 1024).toFixed(0)} KB`],
    ["Audio I/O", `${patch.meta.audioInputs} in · ${patch.meta.audioOutputs} out`],
    ["MIDI modules", patch.meta.midiModules],
    ["Starred", patch.meta.starredCount]
  ];
  $("#patch-metadata").replaceChildren(...metadata.flatMap(([label, value]) => {
    const term = document.createElement("dt"); term.textContent = label;
    const detail = document.createElement("dd"); detail.textContent = String(value);
    return [term, detail];
  }));
  const stars = patch.starred.slice(0, 8).map((star) => {
    const item = document.createElement("button");
    item.type = "button";
    item.className = "starred-item";
    item.innerHTML = `<span>★</span><b></b><small></small>`;
    item.querySelector("b").textContent = star.moduleName;
    item.querySelector("small").textContent = `${star.blockName}${star.midiCc === null ? "" : ` · CC ${star.midiCc}`}`;
    item.addEventListener("click", () => {
      const module = patch.modules[star.module];
      if (module) showModuleDetails(module);
    });
    return item;
  });
  if (!stars.length) {
    const empty = document.createElement("p");
    empty.className = "inspector-empty";
    empty.textContent = "No starred parameters in this patch.";
    stars.push(empty);
  }
  $("#starred-list").replaceChildren(...stars);
  $("#route-title").textContent = "Select a connection line";
  $("#route-blocks").textContent = "Its source, destination, and strength will appear here.";
}

function selectRoute(path, connection) {
  elements.connectionLayer.querySelectorAll(".connection-path").forEach((item) => item.classList.toggle("selected", item === path));
  $("#route-title").textContent = `${connection.sourceName} → ${connection.destinationName}`;
  $("#route-blocks").textContent = `${connection.sourceBlockName} → ${connection.destinationBlockName} · ${connection.strength}% strength`;
  $("#route-inspector").classList.add("has-route");
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
  $("#block-count").textContent = `${module.blocks.length} available`;
  $("#block-list").replaceChildren(...module.blocks.map((block) => {
    const item = document.createElement("div");
    item.className = `block-item ${block.type || "block"}`;
    item.innerHTML = `<i></i><span></span><small></small>`;
    item.querySelector("span").textContent = block.label;
    item.querySelector("small").textContent = block.type?.replaceAll("_", " ") || "block";
    return item;
  }));
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
  elements.library.hidden = true;
  elements.browse.hidden = true;
  elements.banks.hidden = true;
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
$("#library-nav").addEventListener("click", showLibrary);
$("#browse-nav").addEventListener("click", showBrowse);
$("#banks-nav").addEventListener("click", showBanks);
$("#library-home").addEventListener("click", reset);
$("#browse-home").addEventListener("click", reset);
$("#banks-home").addEventListener("click", reset);
[$("#library-import"), $("#library-empty-import")].forEach((button) => button.addEventListener("click", () => elements.libraryInput.click()));
elements.libraryInput.addEventListener("change", () => importLibraryFiles(elements.libraryInput.files || []));
elements.librarySearch.addEventListener("input", renderLibrary);
elements.librarySort.addEventListener("change", renderLibrary);
$("#browse-form").addEventListener("submit", (event) => {
  event.preventDefault(); browseQuery = $("#browse-search").value.trim(); browsePage = 1; loadBrowseResults();
});
$("#browse-previous").addEventListener("click", () => { if (browsePage > 1) { browsePage -= 1; loadBrowseResults(); window.scrollTo({ top: 180, behavior: "smooth" }); } });
$("#browse-next").addEventListener("click", () => { if (browsePage < browseTotalPages) { browsePage += 1; loadBrowseResults(); window.scrollTo({ top: 180, behavior: "smooth" }); } });
$("#patch-dialog-close").addEventListener("click", () => elements.patchDialog.close());
$("#patch-dialog-save").addEventListener("click", saveCommunityPatch);
elements.patchDialog.addEventListener("close", () => { $("#patch-dialog-save").textContent = "Add to local library"; $("#patch-dialog-art").classList.remove("art-placeholder"); });
$("#edit-metadata-button").addEventListener("click", async () => {
  if (!currentLibraryRecordId) return;
  const record = await getPatch(currentLibraryRecordId);
  if (record) openMetadataEditor(record);
});
$("#versions-button").addEventListener("click", () => openVersionHistory());
$("#versions-dialog-close").addEventListener("click", () => elements.versionsDialog.close());
$("#snapshot-form").addEventListener("submit", createSnapshot);
$("#compare-versions").addEventListener("click", compareSelectedRevisions);
$("#metadata-dialog-close").addEventListener("click", () => elements.metadataDialog.close());
$("#metadata-form").addEventListener("submit", saveMetadata);
$("#metadata-import").addEventListener("click", () => $("#metadata-import-input").click());
$("#metadata-import-input").addEventListener("change", () => importMetadataFile($("#metadata-import-input").files?.[0]));
$("#metadata-export").addEventListener("click", () => {
  if (!metadataRecord) return;
  const metadata = collectMetadata();
  downloadJson(sidecarJson(metadataRecord, metadata), `${metadataRecord.fileName.replace(/\.bin$/i, "")}.json`);
});
[$("#new-bank"), $("#empty-new-bank")].forEach((button) => button.addEventListener("click", createBank));
$("#import-bank").addEventListener("click", () => $("#bank-import-input").click());
$("#import-bank-folder").addEventListener("click", () => $("#bank-folder-input").click());
$("#bank-import-input").addEventListener("change", async () => {
  const input = $("#bank-import-input");
  const button = $("#import-bank");
  if (!input.files?.[0]) return;
  button.disabled = true; button.textContent = "Importing…";
  try {
    await importBankZip(input.files[0]);
    button.textContent = "Bank imported ✓";
  } catch (error) {
    window.alert(`The bank could not be imported. ${error.message}`);
    button.textContent = "Import ZIP";
  } finally {
    button.disabled = false; input.value = "";
    setTimeout(() => { button.textContent = "Import ZIP"; }, 1800);
  }
});
$("#bank-folder-input").addEventListener("change", async () => {
  const input = $("#bank-folder-input");
  const button = $("#import-bank-folder");
  if (!input.files?.length) return;
  button.disabled = true; button.textContent = "Importing…";
  try {
    await importBankFolder(input.files);
    button.textContent = "Bank imported ✓";
  } catch (error) {
    window.alert(`The bank could not be imported. ${error.message}`);
    button.textContent = "Import folder";
  } finally {
    button.disabled = false; input.value = "";
    setTimeout(() => { button.textContent = "Import folder"; }, 1800);
  }
});
$("#bank-patch-search").addEventListener("input", renderBankPalette);
$("#bank-name").addEventListener("input", () => {
  if (!activeBank) return;
  activeBank.name = $("#bank-name").value.trim() || "Untitled bank";
  clearTimeout(bankNameTimer);
  $("#bank-save-status").textContent = "Saving…";
  bankNameTimer = setTimeout(() => persistActiveBank("Bank name saved"), 450);
});
$("#export-bank-zip").addEventListener("click", exportBankZip);
$("#export-bank-folder").addEventListener("click", exportBankFolder);
$("#delete-bank").addEventListener("click", async () => {
  if (!activeBank || !window.confirm(`Delete “${activeBank.name}”? Its patches will remain in the local library.`)) return;
  await removeBank(activeBank.id); activeBank = undefined; selectedBankPatchId = undefined; await refreshBanks();
});
refreshLibrary();
refreshBanks();
