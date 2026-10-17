const encoder = new TextEncoder();

function writeFixedText(bytes, offset, value) {
  const encoded = encoder.encode(value.trim());
  if (encoded.length > 16) throw new Error(`“${value}” is longer than the ZOIA 16-byte name limit.`);
  bytes.fill(0, offset, offset + 16);
  bytes.set(encoded, offset);
}

export function editPatchNames(buffer, patch, { patchName, pages, modules }) {
  const output = buffer.slice(0);
  const bytes = new Uint8Array(output);
  writeFixedText(bytes, patch.nameOffset, patchName || "Untitled patch");
  patch.pages.forEach((page) => {
    if (Number.isInteger(page.nameOffset)) writeFixedText(bytes, page.nameOffset, pages[page.number] ?? page.name);
  });
  patch.modules.forEach((module) => {
    if (Number.isInteger(module.nameOffset)) writeFixedText(bytes, module.nameOffset, modules[module.number] ?? module.customName);
  });
  return output;
}

export function editModuleSettings(buffer, module, { colorId, parameters }) {
  if (!Number.isInteger(colorId) || colorId < 1 || colorId > 15) throw new Error("Choose a valid ZOIA module color.");
  if (!Array.isArray(parameters) || parameters.length !== module.parameters.length) throw new Error("The saved parameter list is incomplete.");
  const output = buffer.slice(0);
  const view = new DataView(output);
  view.setInt32(module.headerColorOffset, colorId, true);
  if (Number.isInteger(module.colorOffset)) view.setInt32(module.colorOffset, colorId, true);
  parameters.forEach((value, index) => {
    const raw = Number(value);
    if (!Number.isInteger(raw) || raw < 0 || raw > 65535) throw new Error(`${module.parameters[index].name} must be a whole number from 0 to 65535.`);
    view.setInt32(module.parameters[index].offset, raw, true);
  });
  return output;
}

export function editLayoutAndRoutes(buffer, patch, { modules, strengths }) {
  if (!Array.isArray(modules) || modules.length !== patch.modules.length) throw new Error("The module layout is incomplete.");
  if (!Array.isArray(strengths) || strengths.length !== patch.connections.length) throw new Error("The routing values are incomplete.");
  const occupied = new Set();
  modules.forEach(({ page, position }, index) => {
    if (!Number.isInteger(page) || page < 0 || page > 63) throw new Error(`Module ${index + 1} must use a page from 1 to 64.`);
    if (!Number.isInteger(position) || position < 0 || position > 39) throw new Error(`Module ${index + 1} must use a grid position from 1 to 40.`);
    const key = `${page}:${position}`;
    if (occupied.has(key)) throw new Error(`Two modules cannot start at page ${page + 1}, position ${position + 1}.`);
    occupied.add(key);
  });
  strengths.forEach((value, index) => {
    if (!Number.isInteger(value) || value < -20000 || value > 20000) throw new Error(`Route ${index + 1} must be between -200% and 200%.`);
  });
  const output = buffer.slice(0); const view = new DataView(output);
  modules.forEach(({ page, position }, index) => {
    view.setInt32(patch.modules[index].pageOffset, page, true);
    view.setInt32(patch.modules[index].positionOffset, position, true);
  });
  strengths.forEach((value, index) => view.setInt32(patch.connections[index].strengthOffset, value, true));
  return output;
}
