const CACHE_NAME = 'static-cache';

const FILES_TO_CACHE = [
  '/cache/index.html',
  '/cache/arch.html',
  '/cache/layout-static.html',
  '/cache/tables.html',
  '/cache/layout-sidenav-light.html',
  '/cache/troubleshooting.html',
  '/cache/styles.css',
  '/cache/404.html',
  '/static/images/arquitectura.png',
  '/static/images/price1.png',
  '/static/images/price2.png',
  '/static/images/price3.png',
  '/static/images/price4.png',
  '/static/images/price5.png',
  '/static/images/price6.png',
  '/static/images/price7.png',
];

self.addEventListener('install', (evt) => {
  console.log('[ServiceWorker] Install');
  evt.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[ServiceWorker] Pre-caching offline page');
      return cache.addAll(FILES_TO_CACHE);
    })
  );

  self.skipWaiting();
});

self.addEventListener('activate', (evt) => {
  console.log('[ServiceWorker] Activate');
  evt.waitUntil(
    caches.keys().then((keyList) => {
      return Promise.all(keyList.map((key) => {
        if (key !== CACHE_NAME) {
          console.log('[ServiceWorker] Removing old cache', key);
          return caches.delete(key);
        }
      }));
    })
  );
  self.clients.claim();

});


self.addEventListener('fetch', (evt) => {
  if (evt.request.mode !== 'navigate') {
    return;
  }
  evt.respondWith(fetch(evt.request).catch(() => {
      return caches.open(CACHE_NAME).then((cache) => {
        if (evt.request.url.indexOf( '/dist/index.html' ) !== -1 ) {
          return cache.match('/cache/index.html');
      }else if (evt.request.url.indexOf( '/dist/troubleshooting.html' ) !== -1 ) {
        return cache.match('/cache/troubleshooting.html');    
      }else if (evt.request.url.indexOf( '/dist/arch.html' ) !== -1 ) {
        return cache.match('/cache/arch.html');    
      }else if (evt.request.url.indexOf( '/dist/tables.html' ) !== -1 ) {
        return cache.match('/cache/tables.html');    
      }
      });
    })
  );
});




