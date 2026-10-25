/**
 * Campus Gabaa (GabaaHU) Client JavaScript
 * Progressive enhancement for price comparison, language selection, and responsive controls.
 */

document.addEventListener('DOMContentLoaded', function () {
  // 1. Language switcher form auto-submission
  const langSelect = document.getElementById('campusLanguageSelect');
  if (langSelect) {
    langSelect.addEventListener('change', function () {
      const form = document.getElementById('campusLanguageForm');
      if (form) {
        form.submit();
      }
    });
  }

  // 2. Auto-dismiss alerts after 5 seconds
  const autoDismissAlerts = document.querySelectorAll('.alert-dismissible');
  autoDismissAlerts.forEach(function (alert) {
    setTimeout(function () {
      try {
        const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
        bsAlert.close();
      } catch (e) {
        alert.style.display = 'none';
      }
    }, 6000);
  });

  // 3. Confirm dialogs for sensitive actions (e.g. stock toggle or price confirm)
  const confirmActions = document.querySelectorAll('[data-confirm]');
  confirmActions.forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      const message = btn.getAttribute('data-confirm');
      if (!confirm(message)) {
        e.preventDefault();
      }
    });
  });

  // 4. Register PWA Service Worker for standalone APK-style mode
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', function () {
      navigator.serviceWorker.register('/sw.js', { scope: '/' })
        .then(function (registration) {
          // Service worker active
        })
        .catch(function (err) {
          console.warn('PWA ServiceWorker registration error:', err);
        });
    });
  }

  // 5. In-App Standalone Mode & PWA Install Prompt Controller
  let deferredPrompt = null;
  const pwaInstallBanner = document.getElementById('pwaInstallBanner');
  const pwaInstallBtn = document.getElementById('pwaInstallBtn');
  const pwaDismissBtn = document.getElementById('pwaDismissBtn');
  const pwaNavInstallItem = document.getElementById('pwaNavInstallItem');
  const pwaNavInstallBtn = document.getElementById('pwaNavInstallBtn');

  // Check if app is already running in standalone mode (installed)
  const isStandalone = window.matchMedia('(display-mode: standalone)').matches ||
                       window.navigator.standalone === true;

  if (!isStandalone) {
    // Intercept native browser install prompt (Chrome Android, Edge, Desktop Chrome)
    window.addEventListener('beforeinstallprompt', function (e) {
      e.preventDefault();
      deferredPrompt = e;

      // Show banner if not dismissed in current session
      if (pwaInstallBanner && !sessionStorage.getItem('pwa_banner_dismissed')) {
        pwaInstallBanner.classList.remove('d-none');
      }

      // Show navbar install button
      if (pwaNavInstallItem) {
        pwaNavInstallItem.classList.remove('d-none');
      }
    });

    // Handler to execute native install prompt
    function triggerInstall() {
      if (deferredPrompt) {
        deferredPrompt.prompt();
        deferredPrompt.userChoice.then(function (choiceResult) {
          if (choiceResult.outcome === 'accepted') {
            if (pwaInstallBanner) pwaInstallBanner.classList.add('d-none');
            if (pwaNavInstallItem) pwaNavInstallItem.classList.add('d-none');
          }
          deferredPrompt = null;
        });
      } else {
        // Fallback for iOS Safari or browsers without beforeinstallprompt
        const isIos = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
        if (isIos) {
          const iosModalEl = document.getElementById('pwaIosModal');
          if (iosModalEl) {
            const modal = new bootstrap.Modal(iosModalEl);
            modal.show();
          }
        } else {
          alert('To install Campus Gabaa: Tap the browser menu (⋮) in the top-right corner and select "Install app" or "Add to Home screen".');
        }
      }
    }

    if (pwaInstallBtn) {
      pwaInstallBtn.addEventListener('click', triggerInstall);
    }
    if (pwaNavInstallBtn) {
      pwaNavInstallBtn.addEventListener('click', triggerInstall);
    }

    if (pwaDismissBtn) {
      pwaDismissBtn.addEventListener('click', function () {
        if (pwaInstallBanner) {
          pwaInstallBanner.classList.add('d-none');
        }
        sessionStorage.setItem('pwa_banner_dismissed', '1');
      });
    }

    // Always reveal navbar install button on mobile iOS as well
    const isIosMobile = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
    if (isIosMobile && pwaNavInstallItem) {
      pwaNavInstallItem.classList.remove('d-none');
    }
  }

  // Hide install controls once app is installed and launched
  window.addEventListener('appinstalled', function () {
    if (pwaInstallBanner) pwaInstallBanner.classList.add('d-none');
    if (pwaNavInstallItem) pwaNavInstallItem.classList.add('d-none');
    deferredPrompt = null;
  });
});
