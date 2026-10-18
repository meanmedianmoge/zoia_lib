function sequence(count, offset = 0, stride = 1) {
  return Array.from({ length: Number(count) || 0 }, (_, index) => offset + index * stride);
}

export function optionValues(definition, optionIndices = []) {
  return Object.entries(definition.options || {}).map(([, values], index) => values[optionIndices[index] || 0]);
}

export function configuredBlocks(typeId, definition, optionIndices = []) {
  const d = definition.blocks || []; const o = optionValues(definition, optionIndices); let ids;
  const add = (...values) => values.flat().filter((value) => Number.isInteger(value));
  switch (Number(typeId)) {
    case 0: ids = add(0, 1, 2, ...[0, 1, 2].filter((i) => o[i] === "on").map((i) => i + 3)); break;
    case 1: ids = o[0] === "left" ? [0] : o[0] === "right" ? [1] : [0, 1]; break;
    case 2: ids = add(o[1] === "left" ? [0] : o[1] === "right" ? [1] : [0, 1], o[0] === "on" ? 2 : null); break;
    case 4: ids = add(sequence(o[0]), 32, o[2] === "on" ? 33 : null, o[4] !== "off" ? [34, 35] : [], sequence(o[1], 36)); break;
    case 5: ids = add(o[3] === "tap" ? 1 : 0, o[1] === "on" ? 2 : null, o[4] === "on" ? 3 : null, o[5] === "on" ? 4 : null, 5); break;
    case 6: ids = add(0, o[0] === "on" ? 1 : null, o[1] === "on" ? 2 : null, 3, o[2] === "on" ? 4 : null, 5, o[3] === "on" ? 6 : null, o[5] === "on" ? 7 : null, o[3] === "on" ? 8 : null, 9); break;
    case 7: ids = add(0, o[0] === "stereo" ? 1 : null, 2, 3, o[0] === "stereo" ? 4 : null); break;
    case 12: ids = add(0, o[0] === "on" ? [1, 2] : [], 3); break;
    case 13: ids = add(0, o[1] === "yes" ? [2, 3] : 1, 4); break;
    case 14: ids = add(0, o[1] === "on" ? 1 : null, o[2] === "on" ? 2 : null, 3); break;
    case 16: ids = add(sequence(o[0]), 40, 41, 42); break;
    case 19: case 48: ids = add(0, o[0] === "linked" ? 1 : [2, 3], 4); break;
    case 20: ids = add(...sequence(o[1]).flatMap((i) => add(i * 4, i * 4 + 1, o[4] === "on" ? i * 4 + 2 : null, o[7] === "on" ? i * 4 + 3 : null))); break;
    case 22: ids = add(sequence(o[0]), 8); break;
    case 23: ids = add(0, o[3] === "stereo" ? 1 : null, 2, o[0] === "on" ? 3 : null, o[1] === "on" ? 4 : null, o[2] === "on" ? 5 : null, o[4] === "external" ? 6 : null, 7, o[3] === "stereo" ? 8 : null); break;
    case 24: ids = add(0, ["bell", "hi_shelf", "low_shelf"].includes(o[0]) ? 1 : null, 2, 3, 4); break;
    case 28: ids = add(0, o[0] === "yes" ? [1, 2] : [], 3); break;
    case 29: ids = add(0, o[0] === "2in->2out" ? 1 : null, o[1] === "rate" ? 2 : o[1] === "tap_tempo" ? 3 : 4, 5, 6, 7, 8, o[0] !== "1in->1out" ? 9 : null); break;
    case 30: ids = add(0, 1, 2, o[7] === "yes" ? 3 : null, 4, o[1] === "on" ? [5, 6] : [], o[5] === "yes" ? 7 : null, o[6] === "yes" ? 8 : null, 9); break;
    case 31: case 33: ids = add(sequence(o[0]), 16, 17); break;
    case 32: case 34: ids = add(0, 1, sequence(o[0], 2)); break;
    case 36: ids = add(0, o[0] === "on" ? 1 : null, 2); break;
    case 37: ids = add(0, 1, 2, o[0] === "on" ? 3 : null, 4); break;
    case 39: ids = add(o[1] === "on" ? 0 : null, 1); break;
    case 40: ids = add(0, o[2] === "stereo" ? 1 : null, 2, o[0] === "on" ? 3 : null, o[1] === "on" ? 4 : null, o[3] === "external" ? 5 : null, 6, o[2] === "stereo" ? 7 : null); break;
    case 41: ids = add(0, o[0] === "2in->2out" ? 1 : null, o[1] === "rate" ? 2 : o[1] === "tap_tempo" ? 3 : 4, 5, 6, o[0] !== "1in->1out" ? 7 : null); break;
    case 42: ids = add(0, o[0] === "stereo" ? 1 : null, 2, 3, 4, o[1] === 2 ? [5, 6] : [], 7, 8, o[0] === "stereo" ? 9 : null); break;
    case 43: ids = add(0, o[0] === "2in->2out" ? 1 : null, o[1] === "rate" ? 2 : 3, 4, 5, 6, 7, 8, o[0] !== "1in->1out" ? 9 : null); break;
    case 47: ids = add(0, 1, 2, 3, o[1] === "on" ? [4, 5] : [], 6, 7); break;
    case 49: ids = [0, 1, 3, 4, 5]; break;
    case 53: ids = o[0] === "haas" ? [0, 3, 4, 5] : [0, 1, 2, 4, 5]; break;
    case 56: ids = add(0, o[0] === "enabled" ? 1 : null); break;
    case 57: ids = add(0, o[0] === "2in->2out" ? 1 : null, 2, 3, 4); break;
    case 60: ids = add(0, 1, o[1] === "on" ? 2 : null); break;
    case 64: ids = o[0] === "mono" ? [0, 2, 4, 5] : sequence(d.length); break;
    case 67: ids = add(0, o[0] === "stereo" ? 1 : null, 2, 3, 4, 5, 6, o[0] !== "1in->1out" ? 7 : null); break;
    case 68: ids = o[0] === "mono" ? [0, 2] : sequence(d.length); break;
    case 69: ids = add(0, o[0] === "stereo" ? 1 : null, o[1] === "rate" ? 2 : o[1] === "tap_tempo" ? 3 : 4, 5, 6, 7, 8, 9, o[0] !== "1in->1out" ? 10 : null); break;
    case 70: ids = add(0, o[0] === "stereo" ? 1 : null, o[1] === "rate" ? 2 : o[1] === "tap_tempo" ? 3 : 4, 5, 6, 7, 8, o[0] !== "1in->1out" ? 9 : null); break;
    case 71: ids = add(0, o[0] === "stereo" ? 1 : null, o[1] === "rate" ? 2 : o[1] === "tap_tempo" ? 3 : 4, 5, 6, o[0] !== "1in->1out" ? 7 : null); break;
    case 72: ids = add(0, o[0] === "stereo" ? 1 : null, 2, 3, 4, 5, 6, o[0] !== "1in->1out" ? 7 : null); break;
    case 73: ids = add(0, o[1] === "off" ? 1 : 2, o[2] === "on" ? 3 : null, 4, 5); break;
    case 75: ids = add(0, o[0] === "stereo" ? 1 : null, o[1] === "rate" ? 2 : 3, 4, 5, 6, 7, 8, 9); break;
    case 76: ids = add(...sequence(o[0]).flatMap((i) => add(i * 2, o[1] === "stereo" ? i * 2 + 1 : null)), sequence(o[0], 16), o[2] === "on" ? sequence(o[0], 24) : [], 32, o[1] === "stereo" ? 33 : null); break;
    case 79: ids = add(0, o[0] === "stereo" ? 1 : null, 2, 3, 4, o[0] !== "1in->1out" ? 5 : null); break;
    case 81: ids = [o[0] === "cv" ? 0 : 1]; break;
    case 82: ids = add(0, o[0] === "enabled" ? 1 : null, o[1] === "enabled" ? 2 : null, o[2] === "enabled" ? 3 : null); break;
    case 83: ids = sequence(d.length); break;
    case 84: ids = add(0, o[1] === "enabled" ? 1 : null, o[2] === "enabled" ? 2 : null, o[3] === "enabled" ? [3, 4] : []); break;
    case 85: ids = add(0, o[0] === "on" ? [1, 2] : [], 3); break;
    case 102: ids = add(o[0] !== "disabled" ? [0, 1, 2] : [], 3, 4, o[2] === "on" ? 5 : null, 6, 7, o[3] === "on" ? [8, 9] : [], 10, 11); break;
    case 103: ids = [o[0] === "bypass" ? 0 : o[0] === "stomp aux" ? 1 : 2]; break;
    case 104: ids = add(sequence(o[0]), sequence(o[0], 8), 16); break;
    case 105: ids = add(0, o[0] !== "NOT" ? sequence(o[1] - 1, 1) : [], o[2] === "on" ? 38 : null, 39); break;
    case 106: ids = add(0, o[0] === "stereo" ? 1 : null, o[1] === "rate" ? 2 : [3, 4], 5, 6, 7, 8, o[0] === "stereo" ? 9 : null); break;
    case 107: ids = add(0, o[0] === "stereo" ? 1 : null, o[1] === "rate" ? 2 : o[1] === "tap_tempo" ? 3 : 4, 5, 6, 7, 8, o[0] !== "1in->1out" ? 9 : null); break;
    default: ids = sequence(d.length);
  }
  const blocks = ids.map((index) => d[index]).filter(Boolean);
  if (blocks.length < definition.minBlocks || blocks.length > definition.maxBlocks) throw new Error("That option combination produces an invalid module footprint.");
  return blocks;
}

export function defaultParameterRaw(definition, blocks) {
  return blocks.filter((block) => block.isParam).map((block) => {
    const normalized = Number(definition.parameterDefaults?.[block.name]) || 0;
    return Math.max(0, Math.min(65535, Math.round(normalized * 65535)));
  });
}
