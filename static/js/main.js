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

  // 5. In-App Standalone Mode & PWA Install Prompt Controller (Permanent until installed)
  let deferredPrompt = null;
  const pwaInstallBanner = document.getElementById('pwaInstallBanner');
  const pwaInstallBtn = document.getElementById('pwaInstallBtn');
  const pwaDismissBtn = document.getElementById('pwaDismissBtn');
  const pwaNavInstallItem = document.getElementById('pwaNavInstallItem');
  const pwaNavInstallBtn = document.getElementById('pwaNavInstallBtn');
  const pwaFloatingFab = document.getElementById('pwaFloatingFab');
  const pwaFabBtn = document.getElementById('pwaFabBtn');
  const pwaDirectTriggerBtn = document.getElementById('pwaDirectTriggerBtn');
  const pwaPromptReadySection = document.getElementById('pwaPromptReadySection');
  const pwaManualGuideSection = document.getElementById('pwaManualGuideSection');

  // Check if app is installed (standalone mode or previous install recorded)
  const isInstalled = window.matchMedia('(display-mode: standalone)').matches ||
                      window.navigator.standalone === true ||
                      localStorage.getItem('pwa_installed') === 'true';

  function hideAllInstallElements() {
    document.body.classList.add('pwa-standalone');
    document.querySelectorAll('.pwa-install-element').forEach(function (el) {
      el.classList.add('d-none');
    });
  }

  if (isInstalled) {
    hideAllInstallElements();
  } else {
    // App is NOT installed -> Ensure persistent controls across all navigation and activities

    // Check banner minimization state
    const isMinimized = sessionStorage.getItem('pwa_banner_minimized') === '1';
    if (isMinimized && pwaInstallBanner && pwaFloatingFab) {
      pwaInstallBanner.classList.add('d-none');
      pwaFloatingFab.classList.remove('d-none');
    } else if (pwaInstallBanner) {
      pwaInstallBanner.classList.remove('d-none');
      if (pwaFloatingFab) pwaFloatingFab.classList.add('d-none');
    }

    // Intercept native browser prompt whenever Chrome triggers it
    window.addEventListener('beforeinstallprompt', function (e) {
      e.preventDefault();
      deferredPrompt = e;

      // Enable direct trigger in guide modal
      if (pwaPromptReadySection && pwaManualGuideSection) {
        pwaPromptReadySection.classList.remove('d-none');
        pwaManualGuideSection.classList.add('d-none');
      }
    });

    // Unified installer trigger
    function triggerInstall() {
      if (deferredPrompt) {
        deferredPrompt.prompt();
        deferredPrompt.userChoice.then(function (choiceResult) {
          if (choiceResult.outcome === 'accepted') {
            localStorage.setItem('pwa_installed', 'true');
            hideAllInstallElements();
          }
          deferredPrompt = null;
        });
      } else {
        // Show universal guided installation modal
        const modalEl = document.getElementById('pwaInstallModal');
        if (modalEl) {
          const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
          modal.show();
        }
      }
    }

    // Attach click listeners to all permanent install buttons
    if (pwaInstallBtn) pwaInstallBtn.addEventListener('click', triggerInstall);
    if (pwaNavInstallBtn) pwaNavInstallBtn.addEventListener('click', triggerInstall);
    if (pwaFabBtn) pwaFabBtn.addEventListener('click', triggerInstall);
    if (pwaDirectTriggerBtn) pwaDirectTriggerBtn.addEventListener('click', triggerInstall);

    // Minimize bottom banner into floating pill button
    if (pwaDismissBtn) {
      pwaDismissBtn.addEventListener('click', function () {
        if (pwaInstallBanner) pwaInstallBanner.classList.add('d-none');
        if (pwaFloatingFab) pwaFloatingFab.classList.remove('d-none');
        sessionStorage.setItem('pwa_banner_minimized', '1');
      });
    }
  }

  // Once installation succeeds, permanently hide all install triggers
  window.addEventListener('appinstalled', function () {
    localStorage.setItem('pwa_installed', 'true');
    hideAllInstallElements();
    deferredPrompt = null;
  });
});
