// Velo Workspaces — App Store link, in one place.
//
// Every download button on the site points at this one constant. Each
// button also has this same URL baked into the HTML as a static href, so
// it works identically for no-JS visitors and crawlers.
(function () {
  var APP_STORE_URL = "https://apps.apple.com/app/velo-workspaces/id6805509975";

  document.querySelectorAll("[data-app-store-link]").forEach(function (el) {
    el.setAttribute("href", APP_STORE_URL);
  });
})();
