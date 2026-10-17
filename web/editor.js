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
  patch.pages.forEach((page) => writeFixedText(bytes, page.nameOffset, pages[page.number] ?? page.name));
  patch.modules.forEach((module) => {
    if (Number.isInteger(module.nameOffset)) writeFixedText(bytes, module.nameOffset, modules[module.number] ?? module.customName);
  });
  return output;
}
