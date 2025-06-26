import { SERVER_URL } from "../constants";

export type APIResponse<T> = Promise<({ detail: string, ok: false } | { data: T, ok: true }) & { status: number }>;

export const authTokenKey = "authToken";

export async function sendReq<T>(
  path: string | URL,
  options?: RequestInit,
): APIResponse<T> {
  let url: string = `${SERVER_URL}${path}`;
  if (path instanceof URL) {
    url = path.toString();
  }
  if (options) {
    options.credentials = 'include'
  } else {
    options = { credentials: 'include' }
  }
  const resp = await fetch(url, options);
  const data = await resp.json();
  if (!resp.ok) {
    return { status: resp.status, ok: resp.ok, detail: data.detail };
  }
  return { data, status: resp.status, ok: resp.ok };
}

export async function GET<T>(path: string | URL): APIResponse<T> {
  return await sendReq(path);
}

export async function POST<T>(
  path: string | URL,
  data: object,
): APIResponse<T> {
  return await sendReq(path, {
    method: "POST",
    body: JSON.stringify(data),
    headers: { "Content-Type": "application/json" },
  });
}
