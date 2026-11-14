/* Mechalc: офлайн. Версия кэша = версия приложения */
const V='mechalc-v11', FILES=["./", "assets/grain.png", "assets/icon-180.png", "assets/icon-512.png", "assets/icon-orange-180.png", "assets/icon-orange-512.png", "assets/keys/cap1.png", "assets/keys/cap2.png", "assets/keys/cap_tall.png", "assets/sounds/key_down_1.wav", "assets/sounds/key_down_2.wav", "assets/sounds/key_down_3.wav", "assets/sounds/key_up_1.wav", "assets/sounds/key_up_2.wav", "assets/sounds/keycap_insert_1.wav", "assets/sounds/keycap_insert_2.wav", "assets/sounds/keycap_insert_3.wav", "assets/sounds/keycap_pull_1.wav", "assets/sounds/keycap_pull_2.wav", "assets/sounds/keycap_pull_3.wav", "assets/sounds/mech_click.wav", "index.html", "manifest.webmanifest"];
self.addEventListener('install',e=>{ e.waitUntil(caches.open(V).then(c=>c.addAll(FILES)).then(()=>self.skipWaiting())); });
self.addEventListener('activate',e=>{ e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==V).map(k=>caches.delete(k)))).then(()=>self.clients.claim())); });
self.addEventListener('fetch',e=>{
  const r=e.request; if(r.method!=='GET'||new URL(r.url).origin!==location.origin) return;
  e.respondWith(caches.match(r,{ignoreSearch:true}).then(hit=>{
    const net=fetch(r).then(x=>{ if(x.ok){ const c=x.clone(); caches.open(V).then(ch=>ch.put(r,c)); } return x; }).catch(()=>hit||(r.mode==='navigate'?caches.match('index.html'):undefined));
    return hit||net; }));
});
