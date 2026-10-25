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

  // 4. Register PWA Service Worker immediately for standalone APK-style mode
  if ('serviceWorker' in navigator) {
    const registerSW = function () {
      navigator.serviceWorker.register('/sw.js', { scope: '/' })
        .then(function (registration) {
          // Service worker successfully registered
        })
        .catch(function (err) {
          console.warn('PWA ServiceWorker registration error:', err);
        });
    };

    if (document.readyState === 'complete' || document.readyState === 'interactive') {
      registerSW();
    } else {
      window.addEventListener('load', registerSW);
    }
  }

  // 5. In-App Standalone Mode & PWA Install Prompt Controller (Permanent until installed)
  const pwaInstallBanner = document.getElementById('pwaInstallBanner');
  const pwaInstallBtn = document.getElementById('pwaInstallBtn');
  const pwaDismissBtn = document.getElementById('pwaDismissBtn');
  const pwaNavInstallItem = document.getElementById('pwaNavInstallItem');
  const pwaNavInstallBtn = document.getElementById('pwaNavInstallBtn');
  const pwaFloatingFab = document.getElementById('pwaFloatingFab');
  const pwaFabBtn = document.getElementById('pwaFabBtn');
  const pwaDirectTriggerBtn = document.getElementById('pwaDirectTriggerBtn');
  const pwaOpenInChromeBtn = document.getElementById('pwaOpenInChromeBtn');
  const pwaCopyLinkBtn = document.getElementById('pwaCopyLinkBtn');
  const pwaStatusAlert = document.getElementById('pwaStatusAlert');
  const pwaInstallModalEl = document.getElementById('pwaInstallModal');

  // Detect in-app webviews (e.g. Telegram, WhatsApp, Messenger, Facebook)
  const isInAppBrowser = /FBAN|FBAV|Instagram|Telegram|WhatsApp|Line|Messenger/i.test(navigator.userAgent);

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

    // Configure In-App Browser Action Button
    if (isInAppBrowser && pwaOpenInChromeBtn) {
      pwaOpenInChromeBtn.classList.remove('d-none');
      pwaOpenInChromeBtn.addEventListener('click', function () {
        const fullUrl = window.location.href;
        // Launch Android Chrome directly via intent URI
        const chromeIntent = 'intent://' + window.location.host + window.location.pathname + window.location.search + '#Intent;scheme=https;package=com.android.chrome;end';
        window.location.href = chromeIntent;
      });
    }

    // Configure Copy Link Button
    if (pwaCopyLinkBtn) {
      pwaCopyLinkBtn.addEventListener('click', function () {
        const url = window.location.origin;
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(url).then(function () {
            const span = pwaCopyLinkBtn.querySelector('span');
            if (span) span.textContent = 'Link Copied! Open Chrome & Paste';
            setTimeout(function () {
              if (span) span.textContent = 'Copy Webapp Link';
            }, 3500);
          });
        }
      });
    }

    // Helper to open the modal reliably with bootstrap or pure JS fallback
    function showInstallModal() {
      if (!pwaInstallModalEl) return;

      // Update status guidance based on environment
      if (pwaStatusAlert) {
        pwaStatusAlert.classList.remove('d-none');
        if (isInAppBrowser) {
          pwaStatusAlert.className = 'alert alert-warning py-2 px-3 small rounded-3 mb-3 text-center';
          pwaStatusAlert.innerHTML = '<i class="bi bi-info-circle me-1"></i>You are viewing inside <strong>Telegram / WhatsApp</strong>. Tap <strong>"Open in Google Chrome"</strong> above to install!';
        } else if (window.pwaDeferredPrompt) {
          pwaStatusAlert.className = 'alert alert-success py-2 px-3 small rounded-3 mb-3 text-center';
          pwaStatusAlert.innerHTML = '<i class="bi bi-check-circle me-1"></i>Ready! Tap <strong>"Install Campus Gabaa"</strong> below to confirm.';
        } else {
          pwaStatusAlert.className = 'alert alert-info py-2 px-3 small rounded-3 mb-3 text-center';
          pwaStatusAlert.innerHTML = '<i class="bi bi-phone me-1"></i>Tap <strong>( ⋮ )</strong> in Chrome\'s top-right corner & select <strong>"Install app"</strong>.';
        }
      }

      try {
        if (typeof bootstrap !== 'undefined' && bootstrap.Modal) {
          const modal = bootstrap.Modal.getOrCreateInstance(pwaInstallModalEl);
          modal.show();
          return;
        }
      } catch (err) {
        console.warn('Bootstrap modal error, using fallback:', err);
      }

      // Pure JS fallback
      pwaInstallModalEl.classList.add('show');
      pwaInstallModalEl.style.display = 'block';
      pwaInstallModalEl.removeAttribute('aria-hidden');
      document.body.classList.add('modal-open');

      let backdrop = document.getElementById('pwaModalBackdrop');
      if (!backdrop) {
        backdrop = document.createElement('div');
        backdrop.id = 'pwaModalBackdrop';
        backdrop.className = 'modal-backdrop fade show';
        document.body.appendChild(backdrop);
      }
    }

    function closeInstallModal() {
      if (!pwaInstallModalEl) return;
      try {
        if (typeof bootstrap !== 'undefined' && bootstrap.Modal) {
          const modal = bootstrap.Modal.getInstance(pwaInstallModalEl);
          if (modal) {
            modal.hide();
            return;
          }
        }
      } catch (e) {}

      pwaInstallModalEl.classList.remove('show');
      pwaInstallModalEl.style.display = 'none';
      pwaInstallModalEl.setAttribute('aria-hidden', 'true');
      document.body.classList.remove('modal-open');
      const backdrop = document.getElementById('pwaModalBackdrop');
      if (backdrop) backdrop.remove();
    }

    if (pwaInstallModalEl) {
      pwaInstallModalEl.querySelectorAll('[data-bs-dismiss="modal"]').forEach(function (btn) {
        btn.addEventListener('click', closeInstallModal);
      });
    }

    // Unified installer trigger
    function triggerInstall(e) {
      if (e) {
        e.preventDefault();
        e.stopPropagation();
      }

      // Visual tap response feedback
      const targetBtn = (e && e.currentTarget) || pwaInstallBtn;
      if (targetBtn) {
        targetBtn.classList.add('opacity-75');
        setTimeout(function () {
          targetBtn.classList.remove('opacity-75');
        }, 300);
      }

      const activePrompt = window.pwaDeferredPrompt;
      if (activePrompt) {
        // Hide our bottom banner immediately so it doesn't overlap Chrome's native bottom-sheet
        if (pwaInstallBanner) pwaInstallBanner.classList.add('d-none');
        closeInstallModal();

        try {
          activePrompt.prompt();
          activePrompt.userChoice.then(function (choiceResult) {
            if (choiceResult && choiceResult.outcome === 'accepted') {
              localStorage.setItem('pwa_installed', 'true');
              hideAllInstallElements();
            }
            window.pwaDeferredPrompt = null;
          }).catch(function () {
            window.pwaDeferredPrompt = null;
          });
        } catch (err) {
          console.warn('Prompt error:', err);
          window.pwaDeferredPrompt = null;
          showInstallModal();
        }
      } else {
        // Show interactive installation wizard modal
        showInstallModal();
      }
    }

    // Attach click and touch listeners to all permanent install buttons
    [pwaInstallBtn, pwaNavInstallBtn, pwaFabBtn, pwaDirectTriggerBtn].forEach(function (btn) {
      if (btn) {
        btn.addEventListener('click', triggerInstall);
      }
    });

    // Minimize bottom banner into floating pill button
    if (pwaDismissBtn) {
      pwaDismissBtn.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
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
    window.pwaDeferredPrompt = null;
  });
});
