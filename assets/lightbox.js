// Opens a blog screenshot full size in a <dialog> instead of navigating to
// the image. Without JavaScript the link still opens the image itself.
(function () {
  if (typeof HTMLDialogElement !== 'function') return;
  var dialog = null;
  var image = null;

  function open(href, alt) {
    if (!dialog) {
      dialog = document.createElement('dialog');
      dialog.className = 'lightbox';
      dialog.setAttribute('aria-label', 'Screenshot, full size');
      image = document.createElement('img');
      dialog.appendChild(image);
      dialog.addEventListener('click', function () { dialog.close(); });
      document.body.appendChild(dialog);
    }
    image.src = href;
    image.alt = alt || '';
    dialog.showModal();
  }

  document.addEventListener('click', function (event) {
    var link = event.target.closest && event.target.closest('a.shot-frame');
    if (!link || event.metaKey || event.ctrlKey || event.shiftKey || event.button !== 0) return;
    event.preventDefault();
    var img = link.querySelector('img');
    open(link.getAttribute('href'), img ? img.alt : '');
  });
})();
