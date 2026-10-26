// The local launcher adds this script; plain runs and check fixtures omit it.
(() => {
  const script = document.currentScript;
  const revision = script.dataset.revision;

  async function checkForSavedChanges() {
    try {
      const response = await fetch(script.dataset.endpoint, { cache: "no-store" });
      // A plain-mode server no longer provides the development endpoint.
      if (response.status === 404) return;
      if (response.ok && (await response.json()).revision !== revision) {
        // Use GET, even after a submitted round: never resubmit the old move.
        window.location.replace(script.dataset.start);
        return;
      }
    } catch {
      // Python edits briefly stop HTTP while the new server process starts.
    }
    window.setTimeout(checkForSavedChanges, 500);
  }

  window.setTimeout(checkForSavedChanges, 500);
})();
