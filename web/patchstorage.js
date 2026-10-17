const API_ROOT = "https://patchstorage.com/api/beta";

async function request(url, options = {}) {
  const response = await fetch(url, { credentials: "omit", ...options });
  if (!response.ok) throw new Error(`PatchStorage returned ${response.status}.`);
  return response;
}

export async function browsePatches({ page = 1, search = "", order = "desc" } = {}) {
  const url = new URL(`${API_ROOT}/patches/`);
  url.searchParams.set("page", String(page));
  url.searchParams.set("per_page", "12");
  url.searchParams.set("platforms", "3003");
  url.searchParams.set("order", order);
  url.searchParams.set("orderby", search ? "relevance" : "date");
  if (search) url.searchParams.set("search", search);
  const response = await request(url);
  return {
    patches: await response.json(),
    total: Number(response.headers.get("X-WP-Total")) || 0,
    totalPages: Number(response.headers.get("X-WP-TotalPages")) || 1
  };
}

export async function getPatchDetails(id) {
  const response = await request(`${API_ROOT}/patches/${id}/`);
  return response.json();
}

export async function downloadPatchFile(url) {
  const response = await request(url);
  return response.arrayBuffer();
}
