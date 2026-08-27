// Velo Workspaces — App Store link, in one place.
//
// The app is in App Store review as this site ships, so there is no real
// listing URL yet. Every download button on the site points at this one
// constant (progressively — each button already has a safe static href to
// Apple's App Store homepage baked into the HTML, so it never links
// nowhere for no-JS visitors or crawlers). Once the app is approved, update
// APP_STORE_URL below and every page picks it up — no need to hunt through
// each HTML file.
(function () {
  var APP_STORE_URL = "https://apps.apple.com/app/velo-workspaces"; // TODO: replace with the real App Store URL once approved.

  document.querySelectorAll("[data-app-store-link]").forEach(function (el) {
    el.setAttribute("href", APP_STORE_URL);
  });
})();
