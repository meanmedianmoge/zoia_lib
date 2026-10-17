const DATABASE_NAME = "zoia-patchwork";
const DATABASE_VERSION = 2;
const PATCH_STORE = "patches";
const BANK_STORE = "banks";

function openDatabase() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(DATABASE_NAME, DATABASE_VERSION);
    request.onupgradeneeded = () => {
      const database = request.result;
      if (!database.objectStoreNames.contains(PATCH_STORE)) {
        const store = database.createObjectStore(PATCH_STORE, { keyPath: "id" });
        store.createIndex("addedAt", "addedAt");
        store.createIndex("title", "title");
      }
      if (!database.objectStoreNames.contains(BANK_STORE)) {
        const banks = database.createObjectStore(BANK_STORE, { keyPath: "id" });
        banks.createIndex("updatedAt", "updatedAt");
      }
    };
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error || new Error("Browser storage could not be opened."));
  });
}

function requestResult(request) {
  return new Promise((resolve, reject) => {
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error || new Error("Browser storage operation failed."));
  });
}

async function store(storeName, mode, callback) {
  const database = await openDatabase();
  try {
    const transaction = database.transaction(storeName, mode);
    const completion = new Promise((resolve, reject) => {
      transaction.oncomplete = resolve;
      transaction.onerror = () => reject(transaction.error || new Error("Browser storage transaction failed."));
      transaction.onabort = () => reject(transaction.error || new Error("Browser storage transaction was cancelled."));
    });
    const result = await callback(transaction.objectStore(storeName));
    await completion;
    return result;
  } finally {
    database.close();
  }
}

export function patchId(fileName, byteLength, lastModified = 0) {
  return `${fileName.toLowerCase()}::${byteLength}::${lastModified}`;
}

export async function savePatch(record) {
  return store(PATCH_STORE, "readwrite", (patches) => requestResult(patches.put(record)));
}

export async function listPatches() {
  return store(PATCH_STORE, "readonly", (patches) => requestResult(patches.getAll()));
}

export async function getPatch(id) {
  return store(PATCH_STORE, "readonly", (patches) => requestResult(patches.get(id)));
}

export async function removePatch(id) {
  return store(PATCH_STORE, "readwrite", (patches) => requestResult(patches.delete(id)));
}

export async function saveBank(record) {
  return store(BANK_STORE, "readwrite", (banks) => requestResult(banks.put(record)));
}

export async function listBanks() {
  return store(BANK_STORE, "readonly", (banks) => requestResult(banks.getAll()));
}

export async function removeBank(id) {
  return store(BANK_STORE, "readwrite", (banks) => requestResult(banks.delete(id)));
}
