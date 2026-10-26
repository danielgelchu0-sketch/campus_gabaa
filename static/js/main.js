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
          // SW registered and active
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

  // 5. In-App Standalone Mode & Adaptive Progressive Installation Engine
  const pwaInstallBanner = document.getElementById('pwaInstallBanner');
  const pwaInstallBtn = document.getElementById('pwaInstallBtn');
  const pwaInstallBtnText = document.getElementById('pwaInstallBtnText');
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

  const pwaGuideAndroid = document.getElementById('pwaGuideAndroid');
  const pwaAndroidBadge = document.getElementById('pwaAndroidBadge');
  const pwaGuideIos = document.getElementById('pwaGuideIos');
  const pwaIosBadge = document.getElementById('pwaIosBadge');
  const pwaGuideDesktop = document.getElementById('pwaGuideDesktop');

  // Device & Environment Detection
  const isAndroid = /Android/i.test(navigator.userAgent);
  const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
  const isInAppBrowser = /FBAN|FBAV|Instagram|Telegram|WhatsApp|Line|Messenger/i.test(navigator.userAgent);

  // Check if app is installed (standalone display-mode or registered installation)
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
    // App is NOT installed -> Manage adaptive installation lifecycle

    // Check banner minimization state
    const isMinimized = sessionStorage.getItem('pwa_banner_minimized') === '1';
    if (isMinimized && pwaInstallBanner && pwaFloatingFab) {
      pwaInstallBanner.classList.add('d-none');
      pwaFloatingFab.classList.remove('d-none');
    } else if (pwaInstallBanner) {
      pwaInstallBanner.classList.remove('d-none');
      if (pwaFloatingFab) pwaFloatingFab.classList.add('d-none');
    }

    // Modal helpers (Bootstrap 5 modal with pure JS fallback)
    function openModal() {
      if (!pwaInstallModalEl) return;
      try {
        if (typeof bootstrap !== 'undefined' && bootstrap.Modal) {
          const modal = bootstrap.Modal.getOrCreateInstance(pwaInstallModalEl);
          modal.show();
          return;
        }
      } catch (err) {
        console.warn('Bootstrap modal error, using pure JS fallback:', err);
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

    function closeModal() {
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
        btn.addEventListener('click', closeModal);
      });
    }

    // Dynamic UI State Renderer: adapts buttons and modal in real time
    function renderInstallationState() {
      const hasNativePrompt = Boolean(window.pwaDeferredPrompt);

      if (hasNativePrompt) {
        // STATE 1: Native 1-Tap Prompt is Ready
        if (pwaInstallBtnText) pwaInstallBtnText.textContent = 'Install App (1-Tap)';
        if (pwaDirectTriggerBtn) {
          pwaDirectTriggerBtn.classList.remove('d-none');
        }
        if (pwaStatusAlert) {
          pwaStatusAlert.classList.remove('d-none');
          pwaStatusAlert.className = 'alert alert-success py-2 px-3 small rounded-3 mb-3 text-center';
          pwaStatusAlert.innerHTML = '<i class="bi bi-check-circle-fill me-1"></i><strong>Ready to Install!</strong> Tap <strong>"Install Campus Gabaa (1-Tap)"</strong> below.';
        }
      } else {
        // STATE 2: Native Prompt Not Yet Dispatched or Unsupported (iOS, In-App, Cooldown, Firefox)
        if (pwaInstallBtnText) pwaInstallBtnText.textContent = 'Install App';
        if (pwaDirectTriggerBtn) {
          pwaDirectTriggerBtn.classList.add('d-none'); // Hide the dead-end button so users are not trapped
        }

        // Configure environment-specific guidance
        if (isInAppBrowser) {
          if (pwaOpenInChromeBtn) pwaOpenInChromeBtn.classList.remove('d-none');
          if (pwaStatusAlert) {
            pwaStatusAlert.classList.remove('d-none');
            pwaStatusAlert.className = 'alert alert-warning py-2 px-3 small rounded-3 mb-3 text-center';
            pwaStatusAlert.innerHTML = '<i class="bi bi-exclamation-triangle-fill me-1"></i>You are viewing inside an in-app browser (Telegram/WhatsApp). Tap <strong>"Open in Google Chrome App"</strong> below to install!';
          }
        } else if (isIOS) {
          if (pwaGuideIos) {
            pwaGuideIos.classList.add('guide-card-active');
            pwaGuideIos.classList.remove('d-none');
          }
          if (pwaIosBadge) pwaIosBadge.classList.remove('d-none');
          if (pwaGuideAndroid) pwaGuideAndroid.classList.add('d-none');
          if (pwaGuideDesktop) pwaGuideDesktop.classList.add('d-none');
          if (pwaStatusAlert) {
            pwaStatusAlert.classList.remove('d-none');
            pwaStatusAlert.className = 'alert alert-primary py-2 px-3 small rounded-3 mb-3 text-center';
            pwaStatusAlert.innerHTML = '<i class="bi bi-apple me-1"></i>To install on iOS: Follow the 2 steps below using Safari\'s Share button.';
          }
        } else if (isAndroid) {
          if (pwaGuideAndroid) {
            pwaGuideAndroid.classList.add('guide-card-active');
            pwaGuideAndroid.classList.remove('d-none');
          }
          if (pwaAndroidBadge) pwaAndroidBadge.classList.remove('d-none');
          if (pwaGuideIos) pwaGuideIos.classList.add('d-none');
          if (pwaGuideDesktop) pwaGuideDesktop.classList.add('d-none');
          if (pwaStatusAlert) {
            pwaStatusAlert.classList.remove('d-none');
            pwaStatusAlert.className = 'alert alert-info py-2 px-3 small rounded-3 mb-3 text-center';
            pwaStatusAlert.innerHTML = '<i class="bi bi-android2 me-1"></i>Tap Chrome\'s <strong>( ⋮ )</strong> menu at the top-right &rarr; select <strong>"Install app"</strong>.';
          }
        } else {
          // Desktop / PC
          if (pwaGuideDesktop) {
            pwaGuideDesktop.classList.add('guide-card-active');
            pwaGuideDesktop.classList.remove('d-none');
          }
          if (pwaGuideAndroid) pwaGuideAndroid.classList.add('d-none');
          if (pwaGuideIos) pwaGuideIos.classList.add('d-none');
          if (pwaStatusAlert) {
            pwaStatusAlert.classList.remove('d-none');
            pwaStatusAlert.className = 'alert alert-secondary py-2 px-3 small rounded-3 mb-3 text-center';
            pwaStatusAlert.innerHTML = '<i class="bi bi-laptop me-1"></i>Click the <strong>Install</strong> icon in your browser address bar.';
          }
        }
      }
    }

    // Call state renderer immediately on page init
    renderInstallationState();

    // Listen for custom 'pwa-ready' or native 'beforeinstallprompt' to instantly upgrade UI
    window.addEventListener('pwa-ready', renderInstallationState);
    window.addEventListener('beforeinstallprompt', renderInstallationState);

    // Primary action dispatcher: handles clicks on any install button
    function handleInstallTrigger(e) {
      if (e) {
        e.preventDefault();
        e.stopPropagation();
      }

      // Visual tap confirmation feedback
      const targetBtn = (e && e.currentTarget) || pwaInstallBtn;
      if (targetBtn) {
        targetBtn.classList.add('opacity-75');
        setTimeout(function () {
          targetBtn.classList.remove('opacity-75');
        }, 250);
      }

      const activePrompt = window.pwaDeferredPrompt;

      if (activePrompt) {
        // We have the native Chromium BeforeInstallPromptEvent -> Invoke native installer dialog
        try {
          activePrompt.prompt();
          activePrompt.userChoice
            .then(function (choiceResult) {
              if (choiceResult && choiceResult.outcome === 'accepted') {
                localStorage.setItem('pwa_installed', 'true');
                hideAllInstallElements();
                closeModal();
              } else {
                // User clicked 'Cancel' on Chrome's native sheet: gracefully fall back to guided state
                window.pwaDeferredPrompt = null;
                renderInstallationState();
              }
            })
            .catch(function (err) {
              console.warn('Native prompt userChoice error:', err);
              window.pwaDeferredPrompt = null;
              renderInstallationState();
            });
        } catch (err) {
          console.warn('Native prompt execution error:', err);
          window.pwaDeferredPrompt = null;
          renderInstallationState();
          openModal();
        }
      } else {
        // Native prompt is not available -> Open interactive guided walkthrough modal
        openModal();

        // Highlight the active card with a gentle pulse animation to focus attention
        const activeCard = document.querySelector('.guide-card-active');
        if (activeCard) {
          activeCard.classList.remove('pwa-pulse-highlight');
          void activeCard.offsetWidth; // Force reflow
          activeCard.classList.add('pwa-pulse-highlight');
        }
      }
    }

    // Attach listener to all install triggers
    [pwaInstallBtn, pwaNavInstallBtn, pwaFabBtn, pwaDirectTriggerBtn].forEach(function (btn) {
      if (btn) {
        btn.addEventListener('click', handleInstallTrigger);
      }
    });

    // In-App browser launcher: launches real Google Chrome via Android Intent
    if (pwaOpenInChromeBtn) {
      pwaOpenInChromeBtn.addEventListener('click', function () {
        const fullUrl = window.location.href;
        const chromeIntent = 'intent://' + window.location.host + window.location.pathname + window.location.search + '#Intent;scheme=https;package=com.android.chrome;end';
        window.location.href = chromeIntent;
      });
    }

    // Universal Copy Link Button: copies link with responsive visual feedback
    if (pwaCopyLinkBtn) {
      pwaCopyLinkBtn.addEventListener('click', function () {
        const url = window.location.origin;
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(url).then(function () {
            const span = pwaCopyLinkBtn.querySelector('span');
            if (span) span.textContent = '✓ Link Copied! Open Chrome & Paste';
            pwaCopyLinkBtn.classList.replace('btn-light', 'btn-success');
            pwaCopyLinkBtn.classList.remove('text-muted');
            pwaCopyLinkBtn.classList.add('text-white');
            setTimeout(function () {
              if (span) span.textContent = 'Copy Webapp Link';
              pwaCopyLinkBtn.classList.replace('btn-success', 'btn-light');
              pwaCopyLinkBtn.classList.remove('text-white');
              pwaCopyLinkBtn.classList.add('text-muted');
            }, 3500);
          }).catch(function () {
            fallbackPromptCopy(url);
          });
        } else {
          fallbackPromptCopy(url);
        }
      });
    }

    function fallbackPromptCopy(url) {
      prompt('Copy the web app link below, then open Google Chrome and paste:', url);
    }

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
