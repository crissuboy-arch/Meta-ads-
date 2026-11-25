// Service worker minimo: so o necessario para o navegador considerar o app
// instalavel (PWA). Estrategia: network-first com fallback pro cache do
// "app shell" (so a pagina principal), sem cache agressivo de API.
const CACHE = "ofensiva-trafego-ia-shell-v1";
const SHELL = ["/"];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE).then((cache) => cache.addAll(SHELL)).catch(() => {})
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (url.pathname.startsWith("/api/")) return; // nunca cachear API/dados do usuario

  event.respondWith(
    fetch(req)
      .then((res) => {
        if (req.mode === "navigate" && res.ok) {
          const copy = res.clone();
          caches.open(CACHE).then((cache) => cache.put("/", copy)).catch(() => {});
        }
        return res;
      })
      .catch(() => caches.match(req.mode === "navigate" ? "/" : req))
  );
});
