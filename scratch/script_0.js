
(function(){
  window.__BUILD_ID__ = 'register-2026-07-14-v12-leaders-support';
  console.log('[Register] build =', window.__BUILD_ID__);
  try {
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.getRegistrations().then(function(regs){
        regs.forEach(function(r){ try{r.unregister();}catch(_){} });
      }).catch(function(){});
    }
    if (window.caches && caches.keys) {
      caches.keys().then(function(keys){
        keys.forEach(function(k){ try{caches.delete(k);}catch(_){} });
      }).catch(function(){});
    }
  } catch(e){ console.warn(e); }
})();
