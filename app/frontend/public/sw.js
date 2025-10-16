self.addEventListener("install", (event) => {
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") {
    return;
  }
  event.respondWith(
    caches.open("qr-label-cache").then(async (cache) => {
      const cached = await cache.match(event.request);
      if (cached) {
        return cached;
      }
      const response = await fetch(event.request);
      if (response.status === 200 && response.type === "basic") {
        cache.put(event.request, response.clone());
      }
      return response;
    })
  );
});
