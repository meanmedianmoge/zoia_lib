const COLORS = {
  1: ["Blue", "#4f6dff"], 2: ["Green", "#56a55d"], 3: ["Red", "#ef4c4c"],
  4: ["Yellow", "#e2c72d"], 5: ["Aqua", "#35bfc1"], 6: ["Magenta", "#d04aa2"],
  7: ["White", "#d8d7cf"], 8: ["Orange", "#f07a35"], 9: ["Lima", "#b6dc42"],
  10: ["Surf", "#34a487"], 11: ["Sky", "#56a5e8"], 12: ["Purple", "#7856bb"],
  13: ["Pink", "#ec78a4"], 14: ["Peach", "#f3a477"], 15: ["Mango", "#f2a91c"]
};

function cleanText(bytes) {
  const end = bytes.indexOf(0);
  const slice = end === -1 ? bytes : bytes.slice(0, end);
  return new TextDecoder("latin1").decode(slice).replace(/[\x00-\x1f]/g, "").trim();
}

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

export function parsePatch(buffer, moduleIndex) {
  assert(buffer.byteLength >= 32 && buffer.byteLength % 4 === 0, "This does not look like a complete ZOIA patch file.");
  const bytes = new Uint8Array(buffer);
  const view = new DataView(buffer);
  const wordCount = buffer.byteLength / 4;
  const word = (index) => {
    assert(Number.isInteger(index) && index >= 0 && index < wordCount, "The patch ended unexpectedly while it was being decoded.");
    return view.getInt32(index * 4, true);
  };

  const patchName = cleanText(bytes.slice(4, 20)) || "Untitled patch";
  const patchSize = word(0);
  const moduleCount = word(5);
  assert(moduleCount >= 0 && moduleCount <= 512, "The module count is outside the supported range.");

  let cursor = 6;
  const modules = [];
  for (let number = 0; number < moduleCount; number += 1) {
    const size = word(cursor);
    const typeId = word(cursor + 1);
    const version = word(cursor + 2);
    const pageRaw = word(cursor + 3);
    const headerColorId = word(cursor + 4);
    const position = word(cursor + 5);
    const parameterCount = word(cursor + 6);
    // Some valid legacy patches report a compact module size even though their
    // fixed header continues into the following words, matching the desktop parser.
    assert(size >= 1 && cursor + size <= wordCount, `Module ${number + 1} has an invalid size.`);
    assert(parameterCount >= 0 && parameterCount <= 512 && cursor + 10 + parameterCount <= wordCount, `Module ${number + 1} has invalid parameter data.`);

    const definition = moduleIndex[String(typeId)] || {};
    const nameStart = (cursor + size - 4) * 4;
    const customName = cleanText(bytes.slice(nameStart, nameStart + 16));
    const rawParameters = Array.from({ length: parameterCount }, (_, i) => word(cursor + 10 + i));
    modules.push({
      number,
      typeId,
      type: definition.name || `Unknown module ${typeId}`,
      category: definition.category || "Unknown",
      customName,
      displayName: customName || definition.name || `Unknown module ${typeId}`,
      description: definition.description || "No description is available for this module type.",
      footprint: Math.max(1, Number(definition.defaultBlocks) || 1),
      blocks: (definition.blocks || []).map((block) => ({
        ...block,
        label: block.name.replaceAll("_", " ")
      })),
      version,
      page: Math.max(0, Math.min(63, pageRaw)),
      pageOffset: (cursor + 3) * 4,
      position,
      positionOffset: (cursor + 5) * 4,
      size,
      parameterCount,
      parameters: rawParameters.map((raw, index) => ({
        name: definition.parameters?.[index] || `Parameter ${index + 1}`,
        raw,
        normalized: Math.round((raw / 65535) * 1000) / 1000,
        offset: (cursor + 10 + index) * 4
      })),
      cpu: Number(definition.cpu) || 0,
      colorId: headerColorId,
      color: COLORS[headerColorId]?.[0] || "Unknown",
      colorHex: COLORS[headerColorId]?.[1] || "#8b887d",
      headerColorOffset: (cursor + 4) * 4,
      colorOffset: null,
      nameOffset: size >= 14 && nameStart >= (cursor + 10 + parameterCount) * 4 ? nameStart : null
    });
    cursor += size;
  }

  const connectionCountOffset = cursor * 4;
  const connectionCount = word(cursor);
  assert(connectionCount >= 0 && connectionCount <= 4096, "The connection count is outside the supported range.");
  const connections = [];
  for (let i = 0; i < connectionCount; i += 1) {
    const offset = cursor + 1 + i * 5;
    connections.push({
      sourceModule: word(offset), sourceBlock: word(offset + 1),
      destinationModule: word(offset + 2), destinationBlock: word(offset + 3),
      strengthRaw: word(offset + 4), strength: Math.round(word(offset + 4) / 100),
      strengthOffset: (offset + 4) * 4
    });
  }
  cursor += 1 + connectionCount * 5;
  const connectionsEndOffset = cursor * 4;

  const storedPageCount = word(cursor);
  assert(storedPageCount >= 0 && storedPageCount <= 256, "The page count is outside the supported range.");
  const pageNames = [];
  for (let i = 0; i < storedPageCount; i += 1) {
    const start = (cursor + 1 + i * 4) * 4;
    if (i < 64) pageNames.push(cleanText(bytes.slice(start, start + 16)));
  }
  cursor += 1 + storedPageCount * 4;

  const usedPageCount = Math.min(64, Math.max(1, ...modules.map((module) => module.page + 1)));
  const pages = Array.from({ length: usedPageCount }, (_, index) => ({
    number: index,
    name: pageNames[index] || `Page ${index + 1}`,
    moduleCount: modules.filter((module) => module.page === index).length,
    nameOffset: index < storedPageCount ? (cursor - storedPageCount * 4 + index * 4) * 4 : null
  }));

  const starredCount = cursor < wordCount ? word(cursor) : 0;
  const safeStarredCount = starredCount >= 0 && starredCount < 1024 && cursor + starredCount < wordCount ? starredCount : 0;
  const starred = Array.from({ length: safeStarredCount }, (_, index) => {
    const byteOffset = (cursor + 1 + index) * 4;
    const moduleNumber = view.getInt16(byteOffset, true);
    const encodedBlock = view.getInt16(byteOffset + 2, true);
    const blockNumber = encodedBlock % 128;
    const module = modules[moduleNumber];
    const block = module?.blocks.find((candidate) => candidate.position === blockNumber);
    return {
      module: moduleNumber,
      moduleName: module?.displayName || `Module ${moduleNumber + 1}`,
      block: blockNumber,
      blockName: block?.label || `Block ${blockNumber + 1}`,
      midiCc: encodedBlock >= 128 ? Math.round(encodedBlock / 128) - 1 : null
    };
  });

  const colorStart = cursor + 1 + safeStarredCount;
  const trailingColors = colorStart + moduleCount <= Math.min(wordCount, patchSize)
    ? modules.map((_, index) => word(colorStart + index)) : [];
  const hasTrailingColors = trailingColors.length === moduleCount && trailingColors.every((colorId) => COLORS[colorId]);
  if (hasTrailingColors) {
    modules.forEach((module, index) => {
      module.colorId = trailingColors[index];
      module.color = COLORS[module.colorId][0];
      module.colorHex = COLORS[module.colorId][1];
      module.colorOffset = (colorStart + index) * 4;
    });
  }

  connections.forEach((connection) => {
    const source = modules[connection.sourceModule];
    const destination = modules[connection.destinationModule];
    connection.sourceName = source?.displayName || `Module ${connection.sourceModule + 1}`;
    connection.destinationName = destination?.displayName || `Module ${connection.destinationModule + 1}`;
    connection.sourceBlockName = source?.blocks.find((block) => block.position === connection.sourceBlock)?.label || `Block ${connection.sourceBlock + 1}`;
    connection.destinationBlockName = destination?.blocks.find((block) => block.position === connection.destinationBlock)?.label || `Block ${connection.destinationBlock + 1}`;
  });
  const totalCpu = modules.reduce((sum, module) => sum + module.cpu, 0);
  const typeNames = modules.map((module) => module.type.toLowerCase());

  return {
    name: patchName,
    nameOffset: 4,
    size: patchSize,
    byteLength: buffer.byteLength,
    modules,
    connections,
    pages,
    starred,
    sections: { connectionCountOffset, connectionsEndOffset, colorStartOffset: colorStart * 4, hasTrailingColors, dataEndOffset: Math.min(buffer.byteLength, patchSize * 4) },
    meta: {
      moduleCount: modules.length,
      connectionCount: connections.length,
      pageCount: pages.length,
      starredCount: starred.length,
      estimatedCpu: Math.round(totalCpu * 100) / 100,
      audioInputs: typeNames.filter((name) => name === "audio input").length,
      audioOutputs: typeNames.filter((name) => name === "audio output").length,
      midiModules: typeNames.filter((name) => name.includes("midi")).length
    }
  };
}
