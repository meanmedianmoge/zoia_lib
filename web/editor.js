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

export function editModuleConfigurations(buffer, patch, configurations) {
  if (!Array.isArray(configurations) || configurations.length !== patch.modules.length) throw new Error("The module configuration list is incomplete.");
  const records = patch.modules.map((module, index) => {
    const config = configurations[index];
    if (!Number.isInteger(config.colorId) || config.colorId < 1 || config.colorId > 15) throw new Error(`Module ${index + 1} has an invalid color.`);
    if (!Number.isInteger(config.page) || config.page < 0 || config.page > 63 || !Number.isInteger(config.position) || config.position < 0 || config.position > 39) throw new Error(`Module ${index + 1} has an invalid placement.`);
    if (!Array.isArray(config.parameters) || config.parameters.some((value) => !Number.isInteger(value) || value < 0 || value > 65535)) throw new Error(`Module ${index + 1} has invalid parameter values.`);
    const savedLength = module.savedDataLength || 0; const sizeWords = 14 + config.parameters.length + savedLength / 4;
    const record = new ArrayBuffer(sizeWords * 4); const bytes = new Uint8Array(record); const view = new DataView(record);
    bytes.set(new Uint8Array(buffer, module.recordOffset, Math.min(40, module.recordLength)), 0);
    view.setInt32(0, sizeWords, true); view.setInt32(12, config.page, true); view.setInt32(16, config.headerColorId ?? config.colorId, true); view.setInt32(20, config.position, true); view.setInt32(24, config.parameters.length, true);
    bytes.fill(0, 32, 40); (config.optionIndices || []).slice(0, 8).forEach((value, optionIndex) => { bytes[32 + optionIndex] = Number(value) || 0; });
    config.parameters.forEach((value, parameterIndex) => view.setInt32((10 + parameterIndex) * 4, value, true));
    if (savedLength) bytes.set(new Uint8Array(buffer, module.savedDataOffset, savedLength), (10 + config.parameters.length) * 4);
    writeFixedText(bytes, record.byteLength - 16, config.name || module.customName || "");
    return record;
  });
  const moduleBytes = records.reduce((sum, record) => sum + record.byteLength, 0);
  const oldModuleBytes = patch.sections.connectionCountOffset - 24; const delta = moduleBytes - oldModuleBytes;
  const newEnd = patch.sections.dataEndOffset + delta;
  if (newEnd > buffer.byteLength) throw new Error("This patch has no remaining binary space for those module options.");
  const output = new ArrayBuffer(buffer.byteLength); const bytes = new Uint8Array(output); const view = new DataView(output);
  bytes.set(new Uint8Array(buffer, 0, 24), 0); let cursor = 24;
  records.forEach((record) => { bytes.set(new Uint8Array(record), cursor); cursor += record.byteLength; });
  bytes.set(new Uint8Array(buffer, patch.sections.connectionCountOffset, patch.sections.dataEndOffset - patch.sections.connectionCountOffset), cursor);
  if (patch.sections.hasTrailingColors) configurations.forEach((config, index) => view.setInt32(patch.sections.colorStartOffset + delta + index * 4, config.colorId, true));
  view.setInt32(0, newEnd / 4, true);
  return output;
}

export function insertModule(buffer, patch, { typeId, definition, page, position, colorId = 1, optionIndices = [], blocks, parameters }) {
  if (!Number.isInteger(typeId) || typeId < 0) throw new Error("Choose a valid module type.");
  if (!definition || typeof definition !== "object") throw new Error("That module definition is unavailable.");
  if (!Number.isInteger(page) || page < 0 || page > 63 || !Number.isInteger(position) || position < 0 || position > 39) throw new Error("The new module needs a valid grid position.");
  if (!Number.isInteger(colorId) || colorId < 1 || colorId > 15) throw new Error("Choose a valid ZOIA module color.");
  const activeBlocks = blocks || (definition.blocks || []).filter((block) => block.isDefault);
  const parameterValues = parameters || activeBlocks.filter((block) => block.isParam).map(() => 0);
  const sizeWords = 14 + parameterValues.length;
  const record = new ArrayBuffer(sizeWords * 4); const view = new DataView(record);
  view.setInt32(0, sizeWords, true); view.setInt32(4, typeId, true); view.setInt32(8, 1, true);
  view.setInt32(12, page, true); view.setInt32(16, colorId, true); view.setInt32(20, position, true);
  view.setInt32(24, parameterValues.length, true); view.setInt32(28, 0, true);
  const recordBytes = new Uint8Array(record);
  optionIndices.slice(0, 8).forEach((value, index) => { recordBytes[32 + index] = Number(value) || 0; });
  parameterValues.forEach((value, index) => view.setInt32((10 + index) * 4, value, true));
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
