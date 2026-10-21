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
});
