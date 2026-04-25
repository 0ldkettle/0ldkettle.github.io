// Service Worker for Goose Clicker PWA.
// Strategy:
//   - Network-first for navigation/HTML so iOS PWA picks up updates instantly
//     when online, with cache fallback for offline use.
//   - Cache-first for static assets (images, audio, manifest).
//   - Always-fresh for version.txt so the displayed build hash matches reality.
const CACHE = 'goose-clicker-v68';
const ASSETS = [
  './',
  './index.html',
  './manifest.webmanifest',
  './icon-192.png',
  './icon-512.png',
  './icon-maskable-192.png',
  './icon-maskable-512.png',
  './apple-touch-icon.png',
  './apple-touch-icon-120.png',
  './apple-touch-icon-152.png',
  './apple-touch-icon-167.png',
  './apple-touch-icon-180.png',
  './favicon.png',
  './assets/goose.png',
  './assets/goose_body.png',
  './assets/goose_body_quack.png',
  './assets/honk.ogg',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE).then((cache) => cache.addAll(ASSETS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

// True for the top-level page request a PWA issues when launching from the
// home screen — we want this to always try the network first so updates reach
// iOS standalone mode.
function isNavigationRequest(req) {
  if (req.mode === 'navigate') return true;
  if (req.method !== 'GET') return false;
  const accept = req.headers.get('accept') || '';
  return accept.includes('text/html');
}

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);

  // Always bypass cache for version.txt (live build-hash lookup).
  if (url.pathname.endsWith('/version.txt')) {
    event.respondWith(fetch(req).catch(() => new Response('', { status: 200 })));
    return;
  }

  // Network-first for HTML/navigation so iOS PWA picks up updates.
  if (isNavigationRequest(req)) {
    event.respondWith(
      fetch(req)
        .then((res) => {
          if (res && res.ok && url.origin === self.location.origin) {
            const clone = res.clone();
            caches.open(CACHE).then((cache) => cache.put(req, clone));
          }
          return res;
        })
        .catch(() => caches.match(req).then((c) => c || caches.match('./index.html')))
    );
    return;
  }

  // Cache-first for other same-origin assets.
  event.respondWith(
    caches.match(req).then((cached) => {
      if (cached) return cached;
      return fetch(req)
        .then((res) => {
          if (res.ok && url.origin === self.location.origin) {
            const clone = res.clone();
            caches.open(CACHE).then((cache) => cache.put(req, clone));
          }
          return res;
        })
        .catch(() => cached);
    })
  );
});

// Allow the page to tell the waiting SW to activate immediately.
self.addEventListener('message', (event) => {
  if (event.data === 'SKIP_WAITING') self.skipWaiting();
});
