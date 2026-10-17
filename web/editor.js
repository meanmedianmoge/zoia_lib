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

export function insertModule(buffer, patch, { typeId, definition, page, position, colorId = 1 }) {
  if (!Number.isInteger(typeId) || typeId < 0) throw new Error("Choose a valid module type.");
  if (!definition || typeof definition !== "object") throw new Error("That module definition is unavailable.");
  if (!Number.isInteger(page) || page < 0 || page > 63 || !Number.isInteger(position) || position < 0 || position > 39) throw new Error("The new module needs a valid grid position.");
  if (!Number.isInteger(colorId) || colorId < 1 || colorId > 15) throw new Error("Choose a valid ZOIA module color.");
  const parameters = (definition.blocks || []).filter((block) => block.isDefault && block.isParam).sort((a, b) => a.position - b.position);
  const sizeWords = 14 + parameters.length;
  const record = new ArrayBuffer(sizeWords * 4); const view = new DataView(record);
  view.setInt32(0, sizeWords, true); view.setInt32(4, typeId, true); view.setInt32(8, 1, true);
  view.setInt32(12, page, true); view.setInt32(16, colorId, true); view.setInt32(20, position, true);
  view.setInt32(24, parameters.length, true); view.setInt32(28, 0, true);
  const extraColorBytes = patch.sections.hasTrailingColors ? 4 : 0;
  const addedBytes = record.byteLength + extraColorBytes;
  const oldEnd = patch.sections.dataEndOffset; const newEnd = oldEnd + addedBytes;
  if (newEnd > buffer.byteLength) throw new Error("This patch has no remaining binary space for that module.");
  const output = new ArrayBuffer(buffer.byteLength); const bytes = new Uint8Array(output); const outputView = new DataView(output);
  bytes.set(new Uint8Array(buffer, 0, patch.sections.connectionCountOffset), 0);
  bytes.set(new Uint8Array(record), patch.sections.connectionCountOffset);
  bytes.set(new Uint8Array(buffer, patch.sections.connectionCountOffset, oldEnd - patch.sections.connectionCountOffset), patch.sections.connectionCountOffset + record.byteLength);
  if (patch.sections.hasTrailingColors) outputView.setInt32(oldEnd + record.byteLength, colorId, true);
  outputView.setInt32(20, patch.modules.length + 1, true);
  outputView.setInt32(0, newEnd / 4, true);
  return output;
}

export function editLayoutAndRoutes(buffer, patch, { modules, connections }) {
  if (!Array.isArray(modules) || modules.length !== patch.modules.length) throw new Error("The module layout is incomplete.");
  if (!Array.isArray(connections) || connections.length > 4096) throw new Error("The routing list is invalid.");
  const occupied = new Set();
  modules.forEach(({ page, position }, index) => {
    if (!Number.isInteger(page) || page < 0 || page > 63) throw new Error(`Module ${index + 1} must use a page from 1 to 64.`);
    if (!Number.isInteger(position) || position < 0 || position > 39) throw new Error(`Module ${index + 1} must use a grid position from 1 to 40.`);
    const key = `${page}:${position}`;
    if (occupied.has(key)) throw new Error(`Two modules cannot start at page ${page + 1}, position ${position + 1}.`);
    occupied.add(key);
  });
  connections.forEach((connection, index) => {
    for (const key of ["sourceModule", "sourceBlock", "destinationModule", "destinationBlock", "strengthRaw"]) if (!Number.isInteger(connection[key])) throw new Error(`Route ${index + 1} is incomplete.`);
    if (!patch.modules[connection.sourceModule] || !patch.modules[connection.destinationModule]) throw new Error(`Route ${index + 1} references a missing module.`);
    if (connection.sourceBlock < 0 || connection.destinationBlock < 0) throw new Error(`Route ${index + 1} has an invalid block.`);
    if (connection.strengthRaw < -20000 || connection.strengthRaw > 20000) throw new Error(`Route ${index + 1} must be between -200% and 200%.`);
  });
  const placed = buffer.slice(0); const placedView = new DataView(placed);
  modules.forEach(({ page, position }, index) => {
    placedView.setInt32(patch.modules[index].pageOffset, page, true);
    placedView.setInt32(patch.modules[index].positionOffset, position, true);
  });
  const { connectionCountOffset, connectionsEndOffset, dataEndOffset } = patch.sections;
  const suffix = new Uint8Array(placed, connectionsEndOffset, dataEndOffset - connectionsEndOffset);
  const newDataEnd = connectionCountOffset + 4 + connections.length * 20 + suffix.length;
  if (newDataEnd > placed.byteLength) throw new Error("The patch has no remaining space for those connections.");
  const output = new ArrayBuffer(placed.byteLength); const bytes = new Uint8Array(output); const view = new DataView(output);
  bytes.set(new Uint8Array(placed, 0, connectionCountOffset), 0);
  view.setInt32(connectionCountOffset, connections.length, true);
  connections.forEach((connection, index) => {
    const offset = connectionCountOffset + 4 + index * 20;
    view.setInt32(offset, connection.sourceModule, true); view.setInt32(offset + 4, connection.sourceBlock, true);
    view.setInt32(offset + 8, connection.destinationModule, true); view.setInt32(offset + 12, connection.destinationBlock, true);
    view.setInt32(offset + 16, connection.strengthRaw, true);
  });
  bytes.set(suffix, connectionCountOffset + 4 + connections.length * 20);
  view.setInt32(0, newDataEnd / 4, true);
  return output;
}
