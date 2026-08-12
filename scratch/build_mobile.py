import os
import re

root_dir = r'c:\Users\PC\Documents\GitHub\testing'
mobile_dir = os.path.join(root_dir, 'mobile')
os.makedirs(mobile_dir, exist_ok=True)

with open(os.path.join(root_dir, 'index.html'), 'r', encoding='utf-8') as f:
    desktop_html = f.read()

# Replace asset and script paths for /mobile subfolder
mobile_html_body = desktop_html.replace('href="styles.css', 'href="../styles.css')
mobile_html_body = mobile_html_body.replace('src="config.js"', 'src="../config.js"')
mobile_html_body = mobile_html_body.replace('src="logo-base64.js"', 'src="../logo-base64.js"')
mobile_html_body = mobile_html_body.replace('src="wassim-template-base64.js"', 'src="../wassim-template-base64.js"')
mobile_html_body = mobile_html_body.replace('src="app.js?v=1001"', 'src="../app.js?v=1001"')
mobile_html_body = mobile_html_body.replace('src="logo.png"', 'src="../logo.png"')

# Completely remove sidebar block (<aside class="sidebar" id="sidebar">...</aside>)
mobile_html_body = re.sub(r'<!-- ============ SIDEBAR ============ -->\s*<aside class="sidebar".*?</aside>', '', mobile_html_body, flags=re.DOTALL)

# Inject Cairo font and PWA meta tags into head
head_insertion = '''  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&family=Outfit:wght@500;600;700;800;900&display=swap" rel="stylesheet" />
  <meta name="apple-mobile-web-app-capable" content="yes" />
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
  <meta name="apple-mobile-web-app-title" content="S1 SPACE" />
  <meta name="mobile-web-app-capable" content="yes" />
  <meta name="theme-color" content="#6366f1" />
  <link rel="apple-touch-icon" sizes="180x180" href="icons/apple-touch-icon.png" />
  <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>⚜️</text></svg>">
  <link rel="manifest" href="app.webmanifest" />

  <style>
  :root {
    --safe-top: env(safe-area-inset-top, 0px);
    --safe-bottom: env(safe-area-inset-bottom, 0px);
    --safe-left: env(safe-area-inset-left, 0px);
    --safe-right: env(safe-area-inset-right, 0px);
    --topbar-h: 56px;
    --bottomnav-h: 62px;
  }
  
  * {
    -webkit-tap-highlight-color: transparent;
  }

  body {
    padding: 0; margin: 0;
    background: var(--bg, #f8fafc);
    font-family: 'Cairo', 'Outfit', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
    -webkit-font-smoothing: antialiased;
    overscroll-behavior-y: none;
  }

  /* Hide sidebar and hamburger completely */
  .sidebar, .hamburger-btn, .sidebar-overlay {
    display: none !important;
  }

  /* Mobile Auth Screen Fix */
  .auth-screen {
    position: fixed;
    inset: 0;
    z-index: 9999;
    background: var(--bg, #f8fafc);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 16px;
  }

  .auth-card {
    border-radius: 20px !important;
    box-shadow: 0 20px 40px rgba(15, 23, 42, 0.08) !important;
    padding: 24px !important;
    width: 100% !important;
    max-width: 400px !important;
  }

  /* Mobile Top Bar */
  .mobile-topbar {
    position: fixed; top: 0; left: 0; right: 0;
    height: calc(var(--topbar-h) + var(--safe-top));
    padding-top: var(--safe-top);
    padding-left: max(16px, var(--safe-left));
    padding-right: max(16px, var(--safe-right));
    background: rgba(255, 255, 255, 0.92);
    backdrop-filter: saturate(180%) blur(20px);
    -webkit-backdrop-filter: saturate(180%) blur(20px);
    border-bottom: 1px solid rgba(0, 0, 0, 0.06);
    z-index: 90;
    display: flex; align-items: center; justify-content: space-between;
  }

  .mobile-topbar-title {
    display: flex; flex-direction: column; text-align: right; flex: 1;
  }
  .mobile-topbar-eyebrow {
    font-size: 10px; font-weight: 800; text-transform: uppercase; letter-spacing: .06em; color: var(--muted, #94a3b8);
  }
  .mobile-topbar-heading {
    font-size: 16.5px; font-weight: 800; color: var(--text, #0f172a); white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  }

  /* Main content & Layout Overrides - Fit to Screen */
  .layout,
  #appRoot.layout {
    display: block !important;
    width: 100% !important;
    max-width: 100% !important;
    min-height: 100vh !important;
    margin: 0 !important;
    padding: 0 !important;
    grid-template-columns: none !important;
  }

  main.content {
    display: block !important;
    width: 100% !important;
    max-width: 100% !important;
    margin: 0 !important;
    padding-top: calc(var(--topbar-h) + var(--safe-top) + 12px) !important;
    padding-bottom: calc(var(--bottomnav-h) + var(--safe-bottom) + 28px) !important;
    padding-left: max(16px, var(--safe-left)) !important;
    padding-right: max(16px, var(--safe-right)) !important;
    box-sizing: border-box !important;
  }

  /* Mobile Panels & Stat Cards */
  .panel, .stat-card {
    border-radius: 16px !important;
    border: 1px solid rgba(0, 0, 0, 0.06) !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02) !important;
    background: #ffffff !important;
    padding: 16px !important;
  }

  /* Responsive Grids for Mobile Screens */
  .stats-grid,
  .stats-cards-row {
    display: grid !important;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)) !important;
    gap: 12px !important;
    width: 100% !important;
    margin-bottom: 20px !important;
  }

  .stats-charts-grid {
    display: grid !important;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)) !important;
    gap: 16px !important;
    width: 100% !important;
  }

  .form-grid,
  .profile-grid {
    display: grid !important;
    grid-template-columns: 1fr !important;
    gap: 14px !important;
    width: 100% !important;
  }

  .span-2 { grid-column: span 1 !important; }

  /* Touch friendly inputs & buttons */
  input[type="text"], input[type="email"], input[type="password"], input[type="number"], input[type="date"], select, textarea {
    min-height: 44px !important;
    font-size: 15px !important;
    border-radius: 10px !important;
    border: 1px solid rgba(0, 0, 0, 0.12) !important;
    padding: 10px 14px !important;
  }

  .primary-btn, .ghost-btn {
    min-height: 46px !important;
    border-radius: 12px !important;
    font-weight: 800 !important;
    font-size: 14px !important;
  }

  .units-tabs, .config-tabs {
    display: flex !important; overflow-x: auto !important; white-space: nowrap !important;
    padding-bottom: 6px !important; scrollbar-width: none !important;
    -webkit-overflow-scrolling: touch !important;
  }
  .units-tabs::-webkit-scrollbar, .config-tabs::-webkit-scrollbar { display: none; }

  .table-wrap {
    overflow-x: auto !important;
    border-radius: 12px !important;
    width: 100% !important;
    -webkit-overflow-scrolling: touch !important;
  }

  /* Toast Notification positioning for mobile */
  .toast-container {
    top: calc(var(--topbar-h) + var(--safe-top) + 8px) !important;
    left: 16px !important;
    right: 16px !important;
    bottom: auto !important;
    width: auto !important;
    z-index: 10000 !important;
  }
  .toast {
    width: 100% !important;
    border-radius: 12px !important;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.12) !important;
  }

  /* Mobile Bottom Navigation Bar */
  .mobile-bottom-nav {
    position: fixed; bottom: 0; left: 0; right: 0;
    height: calc(var(--bottomnav-h) + var(--safe-bottom));
    padding-bottom: var(--safe-bottom);
    background: rgba(255, 255, 255, 0.94);
    backdrop-filter: saturate(180%) blur(20px);
    -webkit-backdrop-filter: saturate(180%) blur(20px);
    border-top: 1px solid rgba(0, 0, 0, 0.08);
    z-index: 90;
    display: flex; align-items: center; justify-content: space-around;
  }

  .mobile-nav-item {
    flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center;
    gap: 3px; height: 100%; color: var(--muted, #94a3b8); font-size: 10.5px; font-weight: 700;
    background: transparent; border: none; cursor: pointer; transition: all 0.15s ease;
  }

  .mobile-nav-item.active {
    color: var(--primary, #6366f1);
    font-weight: 800;
  }
  .mobile-nav-item svg { width: 20px; height: 20px; }

  /* Install PWA Banner */
  .install-banner {
    position: fixed; bottom: calc(var(--bottomnav-h) + var(--safe-bottom) + 12px); left: 12px; right: 12px;
    background: #0f172a; color: #fff; padding: 12px 16px; border-radius: 16px;
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.25); display: flex; align-items: center; gap: 12px; z-index: 95;
  }
  .install-banner img { width: 36px; height: 36px; border-radius: 10px; }
  .install-banner .txt { flex: 1; display: flex; flex-direction: column; }
  .install-banner .txt b { font-size: 13px; font-weight: 800; }
  .install-banner .txt span { font-size: 11px; color: #94a3b8; }
  .install-banner button#installNowBtn {
    background: #6366f1; color: #fff; border: none; padding: 7px 14px; border-radius: 10px; font-size: 12px; font-weight: 800; cursor: pointer;
  }
  .install-banner button.dismiss {
    background: transparent; color: #64748b; border: none; font-size: 16px; cursor: pointer;
  }
  </style>
'''

mobile_html_body = mobile_html_body.replace('</head>', head_insertion + '\n</head>')

topbar_html = '''
  <header class="mobile-topbar" id="mobileTopbar">
    <div style="display:flex;align-items:center;gap:8px;">
      <a href="register/" style="font-size:18px;text-decoration:none;" title="Register">📝</a>
      <span id="roleBadge" style="font-size:10.5px; font-weight:800; text-transform:uppercase; padding:4px 8px; border-radius:999px; background:rgba(99,102,241,0.08); color:var(--primary);"></span>
    </div>
    <div class="mobile-topbar-title">
      <div class="mobile-topbar-eyebrow" id="mobileEyebrow">Saida One</div>
      <div class="mobile-topbar-heading" id="mobileHeading">Dashboard</div>
    </div>
    <button type="button" id="logoutBtn" style="padding:6px;background:transparent;border:none;color:var(--danger);cursor:pointer;display:grid;place-items:center;" title="Logout">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
    </button>
  </header>
'''

bottom_nav_html = '''
  <nav class="mobile-bottom-nav" id="mobileBottomNav">
    <button type="button" class="mobile-nav-item active" data-view="dashboard">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>
      <span>Dashboard</span>
    </button>
    <button type="button" class="mobile-nav-item" data-view="units">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
      <span>Units</span>
    </button>
    <button type="button" class="mobile-nav-item" data-view="configuration">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
      <span>Config</span>
    </button>
    <button type="button" class="mobile-nav-item" data-view="payments">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="4" width="22" height="16" rx="2" ry="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>
      <span>Payments</span>
    </button>
    <button type="button" class="mobile-nav-item" data-view="leaderProfile" id="mobileProfileNavBtn">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
      <span>Profile</span>
    </button>
  </nav>
'''

# Place topbar AND bottom_nav INSIDE #appRoot so when logged out they are completely hidden
mobile_html_body = mobile_html_body.replace('<div id="appRoot" class="layout" style="display:none;">', '<div id="appRoot" class="layout" style="display:none;">\n' + topbar_html)
mobile_html_body = mobile_html_body.replace('</main>\n  </div>', '</main>\n' + bottom_nav_html + '\n  </div>')

mobile_js_script = '''
  <script>
  (function() {
    // 1. Mobile Bottom Nav Active State & View Switcher
    var HEADINGS = {
      dashboard: { eyebrow: 'Saida One', heading: 'Dashboard' },
      units: { eyebrow: 'Saida One', heading: 'Units' },
      configuration: { eyebrow: 'Saida One', heading: 'Configuration' },
      payments: { eyebrow: 'Saida One', heading: 'Payments' },
      memberProfile: { eyebrow: 'Saida One', heading: 'Member Profile' },
      leaderProfile: { eyebrow: 'Saida One', heading: 'Leader Profile' }
    };

    function updateNavUI(viewId) {
      document.querySelectorAll('.mobile-nav-item').forEach(function(item) {
        item.classList.toggle('active', item.getAttribute('data-view') === viewId);
      });
      var info = HEADINGS[viewId] || { eyebrow: 'Saida One', heading: viewId };
      var eb = document.getElementById('mobileEyebrow');
      var hd = document.getElementById('mobileHeading');
      if (eb) eb.textContent = info.eyebrow;
      if (hd) hd.textContent = info.heading;
    }

    document.querySelectorAll('.mobile-nav-item').forEach(function(btn) {
      btn.addEventListener('click', function() {
        var viewId = this.getAttribute('data-view');
        if (!viewId) return;
        if (viewId === 'leaderProfile' && typeof window.openCurrentLeaderProfile === 'function') {
          window.openCurrentLeaderProfile();
        } else if (typeof window.switchView === 'function') {
          window.switchView(viewId);
        } else {
          var views = document.querySelectorAll('.view');
          views.forEach(function(v) { v.classList.remove('active'); });
          var target = document.getElementById(viewId);
          if (target) target.classList.add('active');
        }
        updateNavUI(viewId);
      });
    });

    var main = document.getElementById('main-content');
    if (main) {
      try {
        new MutationObserver(function() {
          var active = document.querySelector('.view.active');
          if (active) updateNavUI(active.id);
        }).observe(main, { subtree: true, attributes: true, attributeFilter: ['class'] });
      } catch(_) {}
    }

    // 2. Service Worker & PWA Install Prompts
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', function() {
        navigator.serviceWorker.register('service-worker.js').catch(function(err) {
          console.warn('[PWA] SW registration failed:', err);
        });
      });
    }

    var deferredPrompt = null;
    window.addEventListener('beforeinstallprompt', function(e) {
      e.preventDefault();
      deferredPrompt = e;
      if (!sessionStorage.getItem('pwaDismissed') && !document.getElementById('installBanner')) {
        var b = document.createElement('div');
        b.id = 'installBanner';
        b.className = 'install-banner';
        b.innerHTML = '<img src="icons/icon-192.png" alt="" /><div class="txt"><b>Add S1 SPACE to Home Screen</b><span>Fast mobile access & offline support</span></div><button id="installNowBtn">Install</button><button class="dismiss" id="dismissPwaBtn">✕</button>';
        document.body.appendChild(b);
        document.getElementById('installNowBtn').addEventListener('click', function() {
          if (deferredPrompt && typeof deferredPrompt.prompt === 'function') {
            deferredPrompt.prompt();
            if (deferredPrompt.userChoice) {
              deferredPrompt.userChoice.then(function() { deferredPrompt = null; }).catch(function(){});
            }
          }
          b.remove();
        });
        document.getElementById('dismissPwaBtn').addEventListener('click', function() {
          sessionStorage.setItem('pwaDismissed', '1');
          b.remove();
        });
      }
    });
  })();
  </script>
'''

mobile_html_body = mobile_html_body.replace('</body>', mobile_js_script + '\n</body>')

with open(os.path.join(mobile_dir, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(mobile_html_body)

print('Rebuilt mobile/index.html with full mobile UI/UX enhancements!')
