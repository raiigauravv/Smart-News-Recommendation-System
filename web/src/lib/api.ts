import axios from 'axios';

export const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: 30000,
});

// Typed helpers
export type RecItem = {
  item_id: string;
  score: number;
  title?: string;
  reason?: string;
};
export async function fetchTrending(k = 20) {
  const { data } = await API.get(`/trending?k=${k}`);
  return data.items as RecItem[];
}
export async function postRecommend(
  user_id: string,
  k = 10,
  recent_clicks?: string[]
) {
  const { data } = await API.post(`/recommend`, { user_id, k, recent_clicks });
  return data.items as RecItem[];
}
export async function postRecommendHybrid(
  user_id: string,
  k = 10,
  recent_clicks?: string[]
) {
  const { data } = await API.post(`/recommend/hybrid`, {
    user_id,
    k,
    recent_clicks,
  });
  return data.items as RecItem[];
}
export async function postSearch(q: string, k = 20, category?: string) {
  const { data } = await API.post(`/search`, { q, k, category });
  return data.items as RecItem[];
}

export async function fetchCategories() {
  const { data } = await API.get(`/categories`);
  return data.categories as string[];
}
export async function postSummarize(
  title?: string,
  abstract?: string,
  max_tokens = 128
) {
  const { data } = await API.post(`/summarize`, {
    title,
    abstract,
    max_tokens,
  });
  return data.summary as string;
}

export async function postExportPdf(items: RecItem[]) {
  const res = await API.post(`/export/pdf`, { articles: items }, { responseType: "blob" });
  return res.data as Blob;
}
