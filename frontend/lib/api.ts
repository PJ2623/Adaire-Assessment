export type TotalGenre = { "total-genre-sold": number };
export type RecentSale = { genre: string; "date‑sold": string };
export type GenreSummary = {
  genre: string;
  "sales‑count": number;
  "last‑sale‑date": string;
  "last‑track‑sold": string;
};
export type UnsoldGenre = { GenreId: number; Name: string };

const BASE = "http://localhost:8000";

async function fetchJson<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`);
  if (!res.ok) throw new Error(`Fetch failed for ${path}`);
  return res.json();
}

export async function getTotalGenreSold(): Promise<number> {
  const data = await fetchJson<TotalGenre>("/total-genre");
  return data["total-genre-sold"];
}

export async function getRecentSale(): Promise<RecentSale> {
  return fetchJson<RecentSale>("/recent-sale");
}

export async function getGenreSummary(): Promise<GenreSummary[]> {
  return fetchJson<GenreSummary[]>("/genre-sale-summary");
}

export async function getUnsoldGenres(): Promise<UnsoldGenre[]> {
  return fetchJson<UnsoldGenre[]>("/not-sold");
}

export async function login(
  username: string,
  password: string
): Promise<string> {
  const res = await fetch(`${BASE}/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({
      username,
      password,
    }),
  });

  if (!res.ok) {
    throw new Error(`Login failed: ${res.status} ${res.statusText}`);
  }

  const json = await res.json() as { access_token: string; token_type: string };
  return json.access_token;
}