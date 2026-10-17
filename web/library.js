const DATABASE_NAME = "zoia-patchwork";
const DATABASE_VERSION = 1;
const STORE_NAME = "patches";

function openDatabase() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(DATABASE_NAME, DATABASE_VERSION);
    request.onupgradeneeded = () => {
      const database = request.result;
      if (!database.objectStoreNames.contains(STORE_NAME)) {
        const store = database.createObjectStore(STORE_NAME, { keyPath: "id" });
        store.createIndex("addedAt", "addedAt");
        store.createIndex("title", "title");
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

async function store(mode, callback) {
  const database = await openDatabase();
  try {
    const transaction = database.transaction(STORE_NAME, mode);
    const completion = new Promise((resolve, reject) => {
      transaction.oncomplete = resolve;
      transaction.onerror = () => reject(transaction.error || new Error("Browser storage transaction failed."));
      transaction.onabort = () => reject(transaction.error || new Error("Browser storage transaction was cancelled."));
    });
    const result = await callback(transaction.objectStore(STORE_NAME));
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
  return store("readwrite", (patches) => requestResult(patches.put(record)));
}

export async function listPatches() {
  return store("readonly", (patches) => requestResult(patches.getAll()));
}

export async function getPatch(id) {
  return store("readonly", (patches) => requestResult(patches.get(id)));
}

export async function removePatch(id) {
  return store("readwrite", (patches) => requestResult(patches.delete(id)));
}
