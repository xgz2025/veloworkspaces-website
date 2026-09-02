// Velo Workspaces — click-to-load YouTube embeds.
//
// Each .yt-facade shows only a static thumbnail (a plain <img>) until
// clicked or activated with Enter/Space. Nothing from YouTube — no script,
// no iframe, no tracking — loads until the visitor actually asks for the
// video. This keeps the page as fast as if the videos weren't there at all
// for anyone who doesn't watch them.
(function () {
  function loadVideo(el) {
    var id = el.getAttribute("data-yt-id");
    if (!id) return;
    var label = el.getAttribute("aria-label") || "YouTube video";
    var iframe = document.createElement("iframe");
    iframe.src = "https://www.youtube-nocookie.com/embed/" + id + "?autoplay=1&rel=0";
    iframe.title = label;
    iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
    iframe.allowFullscreen = true;
    el.innerHTML = "";
    el.appendChild(iframe);
  }

  document.querySelectorAll(".yt-facade[data-yt-id]").forEach(function (el) {
    el.addEventListener("click", function () { loadVideo(el); });
    el.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        loadVideo(el);
      }
    });
  });
})();
